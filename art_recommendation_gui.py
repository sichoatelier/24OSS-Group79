import os
import tkinter as tk
from PIL import Image, ImageTk
from art_recommendation_test.art_recommendation_functions import take_photo_and_save, upload_image_and_save
from art_recommendation_test.art_recommendation import load_art_data, analyze_face

# art.json 파일 경로 설정
data_path = os.path.join(os.path.dirname(__file__), "art.json")

# art.json 파일 경로 설정

# art.json 데이터 로드
if not os.path.exists(data_path):
    raise FileNotFoundError(f"art.json 파일을 찾을 수 없습니다: {data_path}")
else:
    print(f"art.json 파일이 존재합니다: {data_path}")
art_data = load_art_data(data_path)


def show_art_recommendation_test(main_frame, return_to_main_gui):
    """내가 작품이라면 (얼굴 종합 판정) 테스트 GUI"""
    
    image_selected = {'status': False}

    def restart_test():
        for widget in main_frame.winfo_children():
            widget.destroy()
        show_art_recommendation_test(main_frame, return_to_main_gui)

    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="내가 작품이라면?", font=("Arial", 20)).pack(pady=20)

    test_image_label = tk.Label(main_frame)
    test_image_label.pack(pady=10)
    default_image_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'sample_image.png')
    default_image = Image.open(default_image_path)
    default_image = default_image.resize((200, 200))
    default_image = ImageTk.PhotoImage(default_image)
    test_image_label.config(image=default_image)
    test_image_label.image = default_image

    tk.Button(main_frame, text="카메라 촬영", command=lambda: take_photo_and_save(test_image_label, image_selected, enable_result_button)).pack(side=tk.LEFT, padx=10)
    tk.Button(main_frame, text="이미지 선택", command=lambda: upload_image_and_save(test_image_label, image_selected, enable_result_button)).pack(side=tk.LEFT, padx=10)

    result_label = tk.Label(main_frame, text="", font=("Arial", 12), fg="blue")
    result_label.pack(pady=10)
    result_label.config(text="분석 결과 대기 중...")

    artwork_info_label = tk.Label(main_frame, text="", font=("Arial", 14), fg="black")
    artwork_info_label.pack(pady=10)

    result_button = tk.Button(main_frame, text="결과 보기", state=tk.DISABLED, command=lambda: show_result(result_label, artwork_info_label, test_image_label, return_to_main_gui, restart_test))
    result_button.pack(pady=20)

    back_button = tk.Button(main_frame, text="돌아가기", command=return_to_main_gui)
    back_button.pack(pady=20)

    def enable_result_button():
        if image_selected['status']:
            result_button.config(state=tk.NORMAL)


def show_result(result_label, artwork_info_label, test_image_label, return_to_main_gui, restart_test):
    """결과 보기 버튼 클릭 시 동작 - 분석 결과를 GUI에 표시"""
    
    result_label.config(text="분석 중입니다. 잠시만 기다려주세요...", fg="blue")
    result_label.update_idletasks()

    image_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'uploaded_image.png')

    recommendations = analyze_face(image_path, art_data)

    if recommendations in ["얼굴을 감지할 수 없습니다.", "이미지 로드 실패"] or recommendations is None or not recommendations:
        result_label.config(text="얼굴을 인식할 수 없습니다.", fg="red")
        artwork_info_label.config(text="")
        test_image_label.config(image="")  # 이미지 제거

        # 결과보기 버튼을 비활성화하고 돌아가기 버튼만 남기기
        for widget in result_label.master.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget('text') == "결과 보기":
                widget.pack_forget()

        # 다시하기 버튼 추가
        retry_button = tk.Button(result_label.master, text="다시하기", command=restart_test)
        retry_button.pack(pady=10)
        return  # 추천 중단

    recommended_art = next(
        (art for art in art_data if art['art_name'] == recommendations), None
    )

    if recommended_art:
        result_label.config(text="추천 작품이 분석되었습니다.", fg="black")
        artwork_info = f"{recommended_art['art_name']} (by {recommended_art['artist']})"
        artwork_info_label.config(text=artwork_info)

        base_path = os.path.dirname(__file__)
        art_image_path = os.path.join(base_path, "art_img", recommended_art["image_path"])

        print(f"이미지 경로: {art_image_path}")

        if os.path.exists(art_image_path):
            img = Image.open(art_image_path)
            img = img.resize((200, 200))
            img = ImageTk.PhotoImage(img)
            test_image_label.config(image=img)
            test_image_label.image = img  # 참조를 유지해야 이미지가 정상 표시됨
        else:
            result_label.config(text="이미지 파일을 찾을 수 없습니다.", fg="red")
            artwork_info_label.config(text="")
            test_image_label.config(image="")  # 이미지 제거
    else:
        result_label.config(text="추천 작품을 찾을 수 없습니다.", fg="red")
        artwork_info_label.config(text="")
        test_image_label.config(image="")  # 이미지 제거

    # "결과 보기" 버튼 제거
    for widget in result_label.master.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget('text') == "결과 보기":
            widget.pack_forget()

    # "다시하기" 버튼 추가
    retry_button = tk.Button(result_label.master, text="다시하기", command=restart_test)
    retry_button.pack(pady=10)
