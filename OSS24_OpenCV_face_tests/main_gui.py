from PIL import Image, ImageTk
import os
import tkinter as tk

def show_main_gui(main_frame, show_skin_tone_test, show_facial_asymmetry_test, show_art_recommendation_test):
    """Main base GUI to be shown initially and after returning from tests."""
    for widget in main_frame.winfo_children():
        widget.destroy()

    tk.Label(main_frame, text="얼굴로 하는 테스트", font=("Arial", 20)).grid(row=0, column=0, columnspan=3, pady=20)

    # 이미지 파일 경로
    skin_tone_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images', 'skin_tone_image.png'))
    facial_asymmetry_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images', 'facial_asymmetry_image.png'))
    art_recommendation_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'images', 'art_recommendation_image.png'))
    
    # 이미지 변수 초기화
    skin_tone_image = None
    facial_asymmetry_image = None
    art_recommendation_image = None

    # 이미지 로드
    try:
        skin_tone_image = Image.open(skin_tone_image_path)
        skin_tone_image = skin_tone_image.resize((150, 150))
        skin_tone_image = ImageTk.PhotoImage(skin_tone_image)
    except Exception as e:
        print(f"Error loading skin_tone_image: {e}")

    try:
        facial_asymmetry_image = Image.open(facial_asymmetry_image_path)
        facial_asymmetry_image = facial_asymmetry_image.resize((150, 150))
        facial_asymmetry_image = ImageTk.PhotoImage(facial_asymmetry_image)
    except Exception as e:
        print(f"Error loading facial_asymmetry_image: {e}")

    try:
        art_recommendation_image = Image.open(art_recommendation_image_path)
        art_recommendation_image = art_recommendation_image.resize((150, 150))
        art_recommendation_image = ImageTk.PhotoImage(art_recommendation_image)
    except Exception as e:
        print(f"Error loading art_recommendation_image: {e}")
    
    # 이미지가 로드되지 않으면 기본 이미지 사용 (예: 빈 이미지를 넣거나 기본 이미지 경로로 대체)
    if skin_tone_image is None:
        skin_tone_image = ImageTk.PhotoImage(file='images/sample_image.png')
    if facial_asymmetry_image is None:
        facial_asymmetry_image = ImageTk.PhotoImage(file='images/sample_image.png')
    if art_recommendation_image is None:
        art_recommendation_image = ImageTk.PhotoImage(file='images/sample_image.png')

    # 이미지를 각 버튼 위에 배치
    tk.Label(main_frame, image=skin_tone_image).grid(row=1, column=0, padx=10, pady=(80, 10))
    tk.Label(main_frame, image=facial_asymmetry_image).grid(row=1, column=1, padx=10, pady=(80, 10))
    tk.Label(main_frame, image=art_recommendation_image).grid(row=1, column=2, padx=10, pady=(80, 10))

    # 버튼만 텍스트로 추가
    skin_tone_button = tk.Button(main_frame, text="백설공주 테스트", command=show_skin_tone_test)
    skin_tone_button.grid(row=2, column=0, padx=20, pady=10)

    facial_asymmetry_button = tk.Button(main_frame, text="뗀석기 테스트", command=show_facial_asymmetry_test)
    facial_asymmetry_button.grid(row=2, column=1, padx=20, pady=10)

    art_recommendation_button = tk.Button(main_frame, text="내가 작품이라면?", command=show_art_recommendation_test)
    art_recommendation_button.grid(row=2, column=2, padx=20, pady=10)
    
    # 이미지가 메모리에서 삭제되지 않도록 유지
    skin_tone_image.label = skin_tone_image
    facial_asymmetry_image.label = facial_asymmetry_image
    art_recommendation_image.label = art_recommendation_image

    # 이미지가 가로로 나란히 보이도록 처리
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=1)
