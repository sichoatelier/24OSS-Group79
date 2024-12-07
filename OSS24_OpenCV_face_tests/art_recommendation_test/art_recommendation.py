import cv2
import numpy as np
from deepface import DeepFace
import random
import json

# 외부에서 작품 데이터 불러오기 (예시로 JSON 파일을 사용)
def load_art_data(file_path):
    """작품 데이터 JSON 파일을 불러오는 함수"""
    with open(file_path, 'r', encoding='utf-8') as file:
        art_data = json.load(file)
    return art_data

# 얼굴 분석 함수
def analyze_face(image_path, art_data):
    """이미지 경로를 받아 얼굴을 분석하고 추천된 작품을 반환하는 함수"""
    image = cv2.imread(image_path)
    if image is None:
        print("Unable to load image.")
        return None

    # 얼굴 검출: Haar Cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8, minSize=(50, 50))

    if len(faces) == 0:
        print("No face detected by Haar Cascade.")
        return None

    # DeepFace로 추가 검증
    try:
        deepface_detections = DeepFace.detectFace(image, detector_backend="opencv")
        if deepface_detections is None:
            print("No face detected by DeepFace.")
            return None
    except Exception as e:
        print(f"DeepFace detection error: {e}")
        return None

    recommendations = []
    face_confidence_threshold = 0.9  # 신뢰도 임계값

    for (x, y, w, h) in faces:
        if w * h < 2500:  # 너무 작은 얼굴 영역 무시
            continue

        face_region = image[y:y+h, x:x+w]

        # 피부 톤 분석
        hsv = cv2.cvtColor(face_region, cv2.COLOR_BGR2HSV)
        brightness = np.mean(hsv[:, :, 2])
        skin_tone = "light" if brightness > 128 else "dark"

        # 머리색 추출
        hair_region = image[max(0, y-h//3):y, x:x+w]
        hair_color = cv2.mean(hair_region)[:3]
        hair_color_name = get_color_name(hair_color)

        # 표정(감정) 분석
        try:
            analysis = DeepFace.analyze(face_region, actions=['emotion'], enforce_detection=False)
            emotion = analysis['dominant_emotion'] if analysis else "unknown"
        except Exception as e:
            emotion = "unknown"
            print(f"Emotion analysis failed: {e}")

        # 수염 감지
        beard_presence = detect_beard(face_region)

        # 머리 길이 추정
        hair_length = estimate_hair_length(image, (x, y, w, h))

        # 사용자 특성
        user_features = {
            'skin_tone': skin_tone,
            'emotion': emotion,
            'hair_color': hair_color_name,
            'beard': "beard" if beard_presence else "none",
            'hair_length': hair_length
        }

        # 작품 추천
        recommendations = recommend_art(user_features, art_data)

        # 얼굴 영역에 추천 표시
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        result_text = recommendations
        cv2.putText(image, result_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    # 얼굴 검출 신뢰도 확인
    if len(recommendations) == 0:
        print("Face detected, but confidence below threshold.")
        return "추천 작품이 없습니다."

    return recommendations if recommendations else "추천 작품이 없습니다."


# 유틸리티 함수
def get_color_name(rgb_color):
    """RGB 색상을 이름으로 변환하는 함수"""
    r, g, b = rgb_color
    if r > 200 and g < 100 and b < 100:
        return "red"
    elif r > 200 and g > 200:
        return "yellow"
    elif b > 200 and r < 100:
        return "blue"
    elif r < 100 and g < 100 and b < 100:
        return "black"
    elif r > 200 and g > 200 and b > 200:
        return "white"  # 화이트 추가
    else:
        return "unknown"


def detect_beard(face_region):
    """얼굴에 수염이 있는지 감지하는 함수"""
    gray = cv2.cvtColor(face_region, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    beard_density = np.sum(edges) / (face_region.shape[0] * face_region.shape[1])
    return beard_density > 0.1

def estimate_hair_length(image, face_coordinates):
    """머리 길이를 추정하는 함수"""
    x, y, w, h = face_coordinates
    head_region = image[max(0, y - h // 3):y, x:x + w]
    gray_head = cv2.cvtColor(head_region, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_head, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        head_top = min(largest_contour, key=lambda x: x[0][1])[0][1]
        head_length = y - head_top
        
        if head_length < 50:
            return "short"
        elif head_length < 100:
            return "medium"
        else:
            return "long"
    else:
        return "unknown"

# 추천 로직
def recommend_art(user_features, art_data):
    """사용자의 특성에 맞는 작품을 추천하는 함수"""
    recommendations = []
    
    for artwork in art_data:
        score = 0
        
        # 사용자 특성과 작품 데이터 비교
        if user_features['skin_tone'] == artwork['light/dark']:
            score += 1
        if user_features['emotion'] == artwork['emotion']:
            score += 1
        if user_features['hair_color'] == artwork['color']:
            score += 1
        if user_features['beard'] == artwork['beard']:
            score += 1
        if user_features['hair_length'] == artwork['hair_length']:
            score += 1
        
        if score > 0:
            recommendations.append((artwork['art_name'], score))

    # 점수 기준으로 정렬
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
    
    # 점수가 높은 작품들 중에서 랜덤 선택
    if recommendations:
        max_score = recommendations[0][1]
        top_recommendations = [rec for rec in recommendations if rec[1] == max_score]
        final_recommendation = random.choice(top_recommendations)
    else:
        final_recommendation = random.choice(art_data)
    
    return final_recommendation[0]  # 작품명 반환
