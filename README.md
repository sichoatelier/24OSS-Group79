# Face Visual Tests With OpenCV
This repository is term project of Group 79 of 'Open Source Software Course' at Gachon University. It consists of three parts and each part consists of a skin tone test, facial asymmetry test, and art recommendation test.

In skin tone test, we deal with ~

In facial asymmetry test, we deal with ~

In art recommendation test, we deal with ~

## Team Member
|Student Number|Name|Github Profile|Email|
|--------------|----|--------------|-----|
|2024XXXXX|황다현(조장)|(github link)|(email)|
|202434662|전조영|(github link)|(email)|
|2024XXXXX|조은하|(github link)|(email)|


## Project Structure
The directory structure for this repository is as follows:
```
main_program/
│
├── skin_tone_test/             # 피부톤 판정 테스트 관련 모듈
│   ├── __init__.py             # 패키지 초기화 파일
│   ├── skin_tone_gui.py        # GUI 코드 (피부톤 판정 테스트 창)
│   └── skin_tone_functions.py  # 피부톤 판정 함수들
│
├── facial_asymmetry_test/      # 얼굴 비대칭 정도 테스트 관련 모듈
│   ├── __init__.py             # 패키지 초기화 파일
│   ├── facial_asymmetry_gui.py # GUI 코드 
│                               (얼굴 비대칭 정도 테스트 창)
│   └── facial_asymmetry_functions.py # 얼굴 비대칭 함수들
│
├── art_recommendation_test/    # 예술 작품 추천 관련 모듈
│   ├── __init__.py             # 패키지 초기화 파일
│   ├── art_recommendation_gui.py # GUI 코드 (예술 작품 추천 창)
│   └── art_recommendation_functions.py # 예술 작품 추천 함수들
│
├── __init__.py                 # 패키지 초기화 파일
├── main.py                     # 메인 프로그램 파일 
│                               (모든 프로그램을 관리)
└── README.md            # 인원, 라이브러리, 라이선스를 포함한 내용
```


## Requirements: (with versions we tested on)
OpenCV (4.5.1) – for facial detection and image processing.

DeepFace (0.0.75) – for facial emotion analysis.

numpy (1.21.2) – for handling numerical data.

random – part of Python's standard library for generating random numbers.

json – part of Python's standard library for reading and parsing JSON files.

Tkinter (8.6)

Tcl (8.6)

## How to run
1. Start the program by running the main.py file.

2. Select one of the options to start the corresponding test.(The user is presented with three options in the GUI: Skin Tone Test, Facial Asymmetry Test, and Art Recommendation.)

For Skin Tone Test, the user can either take a photo or upload an image.

For Facial Asymmetry Test, the user can upload an image of their face for analysis.

For Art Recommendation, the program analyzes the user's facial expression to suggest suitable artwork.

## Results
(results of this repository after running)


## References
(references)

## limitation
1. Face Detection Accuracy: The CascadeClassifier from OpenCV may not perform well under poor lighting or certain angles.

2. DeepFace Performance: Emotion analysis by DeepFace may be inaccurate if the face is unclear or poorly detected.

3. Artwork Recommendation Accuracy: The recommendation system may be limited to the input data and may not fully reflect personal preferences.

4. Real-Time Performance: This program may experience performance issues when processing large amounts of data in real-time.

5. Beard and Hair Length Detection: Accurate detection of beard presence and hair length is difficult. 
