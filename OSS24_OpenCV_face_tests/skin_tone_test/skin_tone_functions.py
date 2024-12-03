import cv2
import os
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

def take_photo_and_save(test_image_label, image_selected, enable_result_button):
    """
    웹캠을 통해 사진을 찍고, 이미지를 저장하고 GUI에 띄우는 함수.
    
    입력:
    - test_image_label: tkinter의 라벨 객체로, 촬영된 이미지를 표시할 GUI 라벨.
    - image_selected: 이미지가 선택되었음을 추적하는 딕셔너리.
    - enable_result_button: 결과 버튼 활성화 함수.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    ret, frame = cap.read()
    if ret:
        # 이미지 저장
        save_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'captured_image.png')
        cv2.imwrite(save_path, frame)
        print(f"Image saved at {save_path}")

        # GUI에 이미지를 띄우기
        show_image_in_gui(test_image_label, save_path)

        # 이미지가 선택되었음을 기록하고 결과 버튼 활성화
        image_selected['status'] = True
        enable_result_button()

    cap.release()
    cv2.destroyAllWindows()

def upload_image_and_save(test_image_label, image_selected, enable_result_button):
    """
    파일 탐색기로 이미지를 선택하고, 선택된 이미지를 GUI에 띄우는 함수.
    
    입력:
    - test_image_label: tkinter의 라벨 객체로, 선택된 이미지를 표시할 GUI 라벨.
    - image_selected: 이미지가 선택되었음을 추적하는 딕셔너리.
    - enable_result_button: 결과 버튼 활성화 함수.
    """
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    if file_path:
        # 선택한 이미지를 로컬에 저장 (복사)
        save_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'uploaded_image.png')
        img = Image.open(file_path)
        img.save(save_path)
        print(f"Image uploaded and saved at {save_path}")

        # GUI에 이미지를 띄우기
        show_image_in_gui(test_image_label, save_path)

        # 이미지가 선택되었음을 기록하고 결과 버튼 활성화
        image_selected['status'] = True
        enable_result_button()

def show_image_in_gui(image_label, image_path):
    """
    GUI 이미지 라벨에 이미지를 표시하는 함수.
    
    입력:
    - image_label: tkinter의 라벨 객체로, 이미지가 표시될 위치.
    - image_path: 표시할 이미지 파일의 경로.
    
    동작:
    - 이미지를 읽어서 GUI에 표시할 수 있는 크기로 조정.
    - 이미지를 tkinter 라벨에 설정하여 GUI에 표시.
    """
    img = Image.open(image_path)
    img = img.resize((200, 200))  # 이미지 크기 조정
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img  # 참조를 유지해야 이미지가 정상 표시됨


def analyze_image_and_display_result(test_image_label, image_selected, enable_result_button, result_text_label):
    """
    이미지를 분석하고 그 결과에 따라 GUI의 결과 텍스트를 업데이트하는 함수.
    여기서는 얼굴 인식을 예로 들었으며, OpenCV를 사용하여 이미지를 분석함.
    
    입력:
    - test_image_label: tkinter의 라벨 객체로, 분석할 이미지를 표시할 GUI 라벨.
    - image_selected: 이미지가 선택되었음을 추적하는 딕셔너리.
    - enable_result_button: 결과 버튼 활성화 함수.
    - result_text_label: 분석 결과를 표시할 GUI 텍스트 라벨.
    """
    # 이미지가 선택되지 않았으면 리턴
    if not image_selected.get('status', False):
        messagebox.showwarning("경고", "이미지를 선택해주세요!")
        return

    # 이미지 파일 경로
    image_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'uploaded_image.png')

    # 이미지 로드 및 얼굴 인식 준비
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 얼굴 인식용 Cascade Classifier 로드 (미리 다운로드한 파일을 사용)하고 얼굴 검출
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # (임시) 변수 작성을 위해 얼굴이 감지된 경우 그 개수를 분석하는 코드를 작성했음.
    if len(faces) > 0:
        result_text = f"얼굴이 {len(faces)}개 감지되었습니다."
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    else:
        result_text = "얼굴을 감지할 수 없습니다."

    # 여기까지가 그 코드

    # 결과 텍스트를 GUI에 표시
    result_text_label.config(text=result_text)

    # 분석이 끝난 이미지를 GUI에 표시
    show_image_in_gui(test_image_label, image_path)

    # 결과 버튼 활성화
    enable_result_button()
