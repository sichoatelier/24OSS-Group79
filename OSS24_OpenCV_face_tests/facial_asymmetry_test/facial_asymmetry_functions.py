import cv2
import os
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import numpy as np

def start_camera_stream(video_label):
    """실시간 카메라 스트리밍을 시작하고 GUI에 표시하는 함수."""
    cap = cv2.VideoCapture(0)

    def update_frame():
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = Image.fromarray(frame_rgb)
            frame_image = ImageTk.PhotoImage(frame_image)
            video_label.config(image=frame_image)
            video_label.image = frame_image
            video_label.current_frame = frame
        
        video_label.after(10, update_frame)

    update_frame()

    def release_camera():
        if cap.isOpened():
            cap.release()

    video_label.release_camera = release_camera

def open_camera_window(main_frame, test_image_label, image_selected, enable_result_button):
    """실시간 카메라 스트리밍 창 열기"""
    camera_window = tk.Toplevel(main_frame)
    camera_window.title("실시간 카메라")

    video_label = tk.Label(camera_window)
    video_label.pack()

    start_camera_stream(video_label)

    tk.Button(camera_window, text="촬영", command=lambda: save_captured_image(camera_window, video_label, test_image_label, image_selected, enable_result_button)).pack(pady=10)

def capture_photo(video_label, save_path):
    """현재 카메라 프레임을 캡처하여 저장하는 함수."""
    frame = getattr(video_label, 'current_frame', None)
    if frame is not None:
        cv2.imwrite(save_path, frame)
        print(f"Image saved at {save_path}")
    else:
        messagebox.showwarning("경고", "캡처할 프레임이 없습니다!")

def save_captured_image(camera_window, video_label, test_image_label, image_selected, enable_result_button):
    """카메라로 캡처한 이미지를 저장하고 GUI에 반영"""
    save_path = os.path.join(os.path.dirname(__file__), "..", "images", "captured_image.png")
    capture_photo(video_label, save_path)

    # 카메라 리소스 해제
    video_label.release_camera()

    camera_window.destroy()
    image_selected['path'] = save_path
    show_image_in_gui(test_image_label, save_path)
    image_selected["status"] = True
    enable_result_button()

def upload_image_and_save(test_image_label, image_selected, enable_result_button):
    """파일 탐색기로 이미지를 선택하고, 선택된 이미지를 GUI에 띄우는 함수."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Image files", "*.jpg *.jpeg *.png")]
    )
    if file_path:
        # 선택한 이미지를 로컬에 저장 (복사)
        save_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'uploaded_image.png')
        img = Image.open(file_path)
        img.save(save_path)
        print(f"Image uploaded and saved at {save_path}")

        show_image_in_gui(test_image_label, save_path)

        image_selected['path'] = save_path  # 이미지 경로 저장
        image_selected['status'] = True
        enable_result_button()

def show_image_in_gui(image_label, image_path):
    """GUI 이미지 라벨에 이미지를 표시하는 함수."""
    img = Image.open(image_path)
    img = img.resize((200, 200))
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img

def analyze_face_asymmetry(image_path):
    """얼굴 비대칭도 분석"""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) > 0:
        x, y, w, h = faces[0]
        face_img = img[y:y+h, x:x+w]
        left_side = face_img[:, :w//2]
        right_side = face_img[:, w//2:]

        left_avg = np.mean(left_side)
        right_avg = np.mean(right_side)
        asymmetry_score = 100 - int(abs(left_avg - right_avg) / 255 * 100)

        return asymmetry_score
    else:
        return 50  # 얼굴을 찾을 수 없으면 중간값인 50점
