import cv2
import os
from tkinter import filedialog
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

def analyze_face_asymmetry(image_path):
    """얼굴 비대칭도 분석"""
    # 이미지 로드
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 얼굴 감지
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        # 얼굴 부분 자르기
        x, y, w, h = faces[0]
        face_img = img[y:y+h, x:x+w]

        # 얼굴을 좌우로 나누어 비대칭 분석
        left_side = face_img[:, :w//2]  # 좌
        right_side = face_img[:, w//2:]  # 우

        # 각 부분의 평균 색상 차이를 계산하여 비대칭도를 평가
        left_avg = np.mean(left_side)
        right_avg = np.mean(right_side)
        asymmetry_score = 100 - int(abs(left_avg - right_avg) / 255 * 100)  # 차이가 클수록 점수가 낮음

        return asymmetry_score
    else:
        return 50  # 얼굴을 찾을 수 없으면 중간값인 50점
