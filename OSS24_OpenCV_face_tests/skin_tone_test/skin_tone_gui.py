import tkinter as tk
import os
from PIL import Image, ImageTk
import cv2
from skin_tone_test.skin_tone_functions import upload_image_and_save, analyze_image_and_display_result, start_camera_stream, save_captured_image

def show_skin_tone_test(main_frame, return_to_main_gui):
    """백설공주 (피부톤 판정) 테스트 GUI"""
    
    # 이미지가 선택되거나 촬영되었는지 확인하는 플래그
    image_selected = {'status': False}

    # 프레임 초기화
    for widget in main_frame.winfo_children():
        widget.destroy()

    # 타이틀 추가
    tk.Label(main_frame, text="백설공주 테스트", font=("Arial", 20)).pack(pady=20)

    # 이미지 표시
    test_image_label = tk.Label(main_frame)
    test_image_label.pack(pady=10)
    default_image_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'skin_tone_gui_image.png')
    default_image = Image.open(default_image_path)
    default_image = default_image.resize((200, 200))
    default_image = ImageTk.PhotoImage(default_image)
    test_image_label.config(image=default_image)
    test_image_label.image = default_image

    # 버튼 추가
    tk.Button(main_frame, text="카메라 촬영", command=lambda: open_camera_window(main_frame, test_image_label, image_selected, enable_result_button)).pack(side=tk.LEFT, padx=10)
    tk.Button(main_frame, text="이미지 선택", command=lambda: upload_image_and_save(test_image_label, image_selected, enable_result_button)).pack(side=tk.LEFT, padx=10)


    # 결과 추가
    result_label = tk.Label(main_frame, text="", font=("Arial", 12), fg="blue")
    result_label.pack(pady=10)

    # 디버그용 초기 상태
    result_label.config(text="분석 결과 대기 중...")

    # 결과보기 버튼
    result_button = tk.Button(main_frame, text="결과 보기", state=tk.DISABLED, 
                              command=lambda: show_result(result_button, result_label, test_image_label, image_selected))
    result_button.pack(pady=20)

    # 돌아가기 버튼
    tk.Button(main_frame, text="돌아가기", command=return_to_main_gui).pack(pady=20)

    def enable_result_button():
        """이미지 선택이나 촬영 후 결과 보기 버튼 활성화"""
        if image_selected['status']:
            result_button.config(state=tk.NORMAL)

# 실시간 카메라 창 열기
def open_camera_window(main_frame, test_image_label, image_selected, enable_result_button):
    """실시간 카메라 스트리밍 창 열기"""
    camera_window = tk.Toplevel(main_frame)
    camera_window.title("실시간 카메라")
    
    # 영상 표시 라벨 생생, 실시간 화면 업데이트 
    video_label = tk.Label(camera_window)
    video_label.pack()

    # 실시간 스트리밍 시작
    start_camera_stream(video_label, None)

    # 촬영 버튼
    tk.Button(camera_window, text="촬영", command=lambda: save_captured_image(camera_window, video_label, test_image_label, image_selected, enable_result_button)).pack(pady=10)

# 여기에 결과 띄우는 내용 적기
def show_result(result_button, result_label, test_image_label, image_selected):
    """결과 보기 버튼 클릭 시 동작 - 결과 텍스트를 업데이트"""
    
    # 결과 버튼을 숨기기
    result_button.pack_forget()

    # 이미지 경로 설정
    image_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'uploaded_image.png')
    
    # 이미지 분석
    result_text = analyze_image_and_display_result(test_image_label, image_selected, result_button, result_label)

    # 결과 텍스트를 업데이트
    result_label.config(text=result_text, fg="black")

    # 분석된 이미지를 GUI에 다시 표시
    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    img = img.resize((200, 200))
    img = ImageTk.PhotoImage(img)
    test_image_label.config(image=img)
    test_image_label.image = img
