import tkinter as tk
import os
from PIL import Image, ImageTk
from tkinter import messagebox
from facial_asymmetry_test.facial_asymmetry_functions import open_camera_window, upload_image_and_save, analyze_face_asymmetry

def show_facial_asymmetry_test(main_frame, return_to_main_gui):
    """뗀석기 (좌우 대칭 판정) 테스트 GUI"""
    
    image_selected = {'status': False}

    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="뗀석기 테스트", font=("Arial", 20)).pack(pady=20)

    test_image_label = tk.Label(main_frame)
    test_image_label.pack(pady=10)

    # 기본 이미지 설정, 표시
    default_image_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'sample_image.png')
    default_image = Image.open(default_image_path)
    default_image = default_image.resize((200, 200))
    default_image = ImageTk.PhotoImage(default_image)
    test_image_label.config(image=default_image)
    test_image_label.image = default_image

    # 버튼
    tk.Button(main_frame, text="카메라 촬영", 
              command=lambda: open_camera_window(main_frame, test_image_label, image_selected, enable_result_button)).pack(side=tk.LEFT, padx=10)
    
    tk.Button(main_frame, text="이미지 선택", 
              command=lambda: upload_image_and_save(test_image_label, image_selected, enable_result_button)).pack(side=tk.LEFT, padx=10)

    result_label = tk.Label(main_frame, text="", font=("Arial", 12), fg="blue")
    result_label.pack(pady=10)
    result_label.config(text="분석 결과 대기 중...")

    result_button = tk.Button(main_frame, text="결과 보기", state=tk.DISABLED, 
                              command=lambda: show_result(result_button, result_label, test_image_label, image_selected))
    result_button.pack(pady=20)

    tk.Button(main_frame, text="돌아가기", command=return_to_main_gui).pack(pady=20)

    def enable_result_button():
        """이미지 선택이나 촬영 후 결과 보기 버튼 활성화"""
        if image_selected['status']:
            result_button.config(state=tk.NORMAL)

def show_result(result_button, result_label, test_image_label, image_selected):
    """결과 보기 버튼 클릭 시 동작 - 결과 텍스트를 업데이트"""
    
    result_button.pack_forget()  # 결과 버튼 숨기기

    image_path = image_selected.get('path')

    if image_path:
        # 얼굴 비대칭도 분석
        asymmetry_score = analyze_face_asymmetry(image_path)
        result_text = f"얼굴 대칭도 점수: {asymmetry_score}점\n(좌우 대칭에 가까울수록 고득점)"

        # 결과 텍스트를 업데이트
        result_label.config(text=result_text)

        # 분석된 이미지를 GUI에 다시 표시
        img = Image.open(image_path)
        img = img.resize((200, 200))
        img = ImageTk.PhotoImage(img)
        test_image_label.config(image=img)
        test_image_label.image = img
    else:
        messagebox.showwarning("경고", "이미지를 선택해 주세요.")
