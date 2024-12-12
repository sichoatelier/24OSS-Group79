import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from PIL import Image, ImageTk

# 실시간 스트리밍 처리
def start_camera_stream(video_label, capture_callback):
    """
    실시간 카메라 스트리밍을 시작하고 GUI에 표시하는 함수.
    
    입력:
    - video_label: Tkinter 라벨로, 실시간 비디오를 표시.
    - capture_callback: 촬영 시 호출되는 함수.
    """

    # 기본 카메라로 초기화
    cap = cv2.VideoCapture(0)

    # 재귀적 호출로 실시간 스트리밍
    def update_frame():
        ret, frame = cap.read()
        if ret:
            # OpenCV 프레임을 Tkinter 이미지로 변환
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = Image.fromarray(frame_rgb)
            frame_image = ImageTk.PhotoImage(frame_image)

            # 라벨 업데이트
            video_label.config(image=frame_image)
            video_label.image = frame_image

            # 현재 프레임을 콜백에 전달
            video_label.current_frame = frame
        
        # 프레임 갱신
        video_label.after(10, update_frame)

    # 스트리밍 시작
    update_frame()

    # 카메라 자원 해제
    def release_camera():
        if cap.isOpened():
            cap.release()

    video_label.release_camera = release_camera

def save_captured_image(camera_window, video_label, test_image_label, image_selected, enable_result_button):
    """카메라로 캡처한 이미지를 저장하고 GUI에 반영"""
    save_path = os.path.join(os.path.dirname(__file__), "..", "images", "captured_image.png")
    capture_photo(video_label, save_path)

    # GUI 업데이트
    camera_window.destroy()
    
    # 이미지 경로 저장
    image_selected['path'] = save_path

    # GUI 라벨에 이미지를 즉시 표시
    show_image_in_gui(test_image_label, save_path)
    
    # 이미지가 선택되었음을 기록하고 결과 버튼 활성화
    image_selected["status"] = True
    enable_result_button()

def capture_photo(video_label, save_path):
    """
    현재 카메라 프레임을 캡처하여 저장하는 함수.
    
    입력:
    - video_label: 현재 프레임이 저장된 Tkinter 라벨 객체.
    - save_path: 저장할 파일 경로.
    """
    frame = getattr(video_label, 'current_frame', None)
    if frame is not None:
        cv2.imwrite(save_path, frame)
        print(f"Image saved at {save_path}")
    else:
        messagebox.showwarning("경고", "캡처할 프레임이 없습니다!")

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

        # 이미지 경로 저장
        image_selected['path'] = save_path

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
    image_path = image_selected.get('path')

    # 이미지 로드 및 얼굴 인식 준비
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 얼굴 인식용 Cascade Classifier 로드 (미리 다운로드한 파일을 사용)하고 얼굴 검출
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
     # 얼굴 감지 후 밝기 계산
    if len(faces) > 0:
        total_brightness = 0
        for (x, y, w, h) in faces:
            # 얼굴 영역 자르기
            face_roi = img[y:y+h, x:x+w]
            
            # 얼굴의 회색조 이미지로 변환
            gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
            
            # 얼굴 영역의 밝기 계산 (픽셀 값 평균)
            brightness = np.mean(gray_face)
            total_brightness += brightness
            # 얼굴 영역에 사각형 그리기 (선택적)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # 평균 밝기 계산
        avg_brightness = total_brightness / len(faces)

        # 얼굴 밝기에 따른 결과 텍스트 작성
        if avg_brightness > 140:
            result_text = f"얼굴 밝기: {avg_brightness:.2f}\n당신은 전생에 백설공주였습니다!"
        elif avg_brightness > 120:
            result_text = f"얼굴 밝기: {avg_brightness:.2f}\n당신은 전생에 하녀였습니다.."
        elif avg_brightness > 100:
            result_text = f"얼굴 밝기: {avg_brightness:.2f}\n당신은 전생에 평민이었습니다.."
        else:
            result_text = f"얼굴 밝기: {avg_brightness:.2f}\n당신은 전생에 거지였습니다..저런.."

    else:
        result_text = "얼굴을 감지할 수 없습니다."

    # 여기까지가 그 코드
    
    # 결과 텍스트를 GUI에 표시
    result_text_label.config(text=result_text, fg="black")

    # 분석이 끝난 이미지를 GUI에 표시
    show_image_in_gui(test_image_label, image_path)

    # 결과 버튼 활성화
    enable_result_button()
