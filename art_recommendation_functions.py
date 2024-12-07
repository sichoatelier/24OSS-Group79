import cv2
import os
from tkinter import filedialog
from PIL import Image, ImageTk
import json

def take_photo_and_save(test_image_label, image_selected, enable_result_button):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    ret, frame = cap.read()
    if ret:
        save_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'captured_image.png')
        cv2.imwrite(save_path, frame)
        print(f"Image saved at {save_path}")
        show_image_in_gui(test_image_label, save_path)
        image_selected['status'] = True
        enable_result_button()

    cap.release()
    cv2.destroyAllWindows()

def upload_image_and_save(test_image_label, image_selected, enable_result_button):
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        save_path = os.path.join(os.path.dirname(__file__), '..', 'images', 'uploaded_image.png')
        img = Image.open(file_path)
        img.save(save_path)
        print(f"Image uploaded and saved at {save_path}")
        show_image_in_gui(test_image_label, save_path)
        image_selected['status'] = True
        enable_result_button()

def show_image_in_gui(image_label, image_path):
    img = Image.open(image_path)
    img = img.resize((200, 200))
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img

def load_recommended_image_path(recommended_image_name):
    json_file_path = os.path.join(os.path.dirname(__file__), 'art_recommendation_test', 'art.json')
    with open(json_file_path, 'r', encoding='utf-8') as file:
        art_data = json.load(file)
    
    for artwork in art_data:
        if artwork['art_name'] == recommended_image_name:
            image_path = artwork['image_path']
            break
    else:
        print("Error: Recommended artwork not found.")
        return None
    
    full_image_path = os.path.join(os.path.dirname(__file__), 'art_recommendation_test', 'art_img', image_path)
    print(f"Recommended image path: {full_image_path}")
    
    if not os.path.exists(full_image_path):
        print("Error: Image file does not exist.")
        return None
    
    return full_image_path

def show_result_with_recommended_image(test_image_label, image_path, recommended_image_name):
    # 추천된 이미지 경로 불러오기
    recommended_image_path = load_recommended_image_path(recommended_image_name)
    
    if recommended_image_path:
        recommended_img = Image.open(recommended_image_path)
        recommended_img = recommended_img.resize((200, 200))
        recommended_img = ImageTk.PhotoImage(recommended_img)
        test_image_label.config(image=recommended_img)
        test_image_label.image = recommended_img
    else:
        print("Error: Recommended image could not be loaded.")
