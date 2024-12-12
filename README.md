# Face Visual Tests With OpenCV
This repository is term project of Group 79 of 'Open Source Software Course' at Gachon University. It consists of three parts and each part consists of a skin tone test, facial asymmetry test, and art recommendation test.

In skin tone test, we deal with ~

In facial asymmetry test, we deal with ~

In the art recommendation test, we use OpenCV to analyze facial features like skin tone, hair color, emotion, beard presence, and hair length, providing personalized artwork suggestions based on these unique traits.

## Team Member
|Student Number|Name|Github Profile|Email|
|--------------|----|--------------|-----|
|2024XXXXX|황다현(조장)|[sichoatelier](https://github.com/sichoatelier)|satcoff28@gmail.com|
|202434662|전조영|[joyong0](https://github.com/joyong0)|wjswhdud1119@naver.com|
|202434671|조은하|[Joeunha](https://github.com/Joeunha)|whdmsgk0831@gachon.ac.kr|


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
├── art_recommendation_test/         # 예술 작품 추천 관련 모듈
│   ├── __init__.py                  # 패키지 초기화 파일
│   ├── art_recommendation.py        # 얼굴 분석 및 메인 함수
│   ├── art_recommendation_functions.py  # 예술 작품 추천 함수들
│   ├── art_recommendation_gui.py    # GUI 코드 (예술 작품 추천 창)
│   ├── art.json                    # 예술 작품 정보 (JSON 파일)
│   └── art_img/                    # 예술 작품 사진 폴더
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

Pillow (8.3.2) - Used for opening and displaying images in the GUI.

Tkinter - Used for creating the GUI elements (e.g., image labels, file dialog).

Tcl (8.6)

## How to run
1. Start the program by running the main.py file.

2. Select one of the options to start the corresponding test.(The user is presented with three options in the GUI: Skin Tone Test, Facial Asymmetry Test, and Art Recommendation.)

For Skin Tone Test, the user can either take a photo or upload an image.

For Facial Asymmetry Test, the user can upload an image of their face for analysis.

For Art Recommendation, upload or capture a face image, then click the "View Results" button to see the analysis results.
## Results
(results of this repository after running)
![face_tone_result_image1](https://github.com/user-attachments/assets/a5843962-7063-441f-9184-b600f99dd4f9)
![face_tone_result_image2](https://github.com/user-attachments/assets/ab1db491-9687-4a2d-bfc0-c137ec2b41f4)

## References
(references)

## limitation
1. Face Detection Accuracy: The CascadeClassifier from OpenCV may not perform well under poor lighting or certain angles.

2. DeepFace Performance: Emotion analysis by DeepFace may be inaccurate if the face is unclear or poorly detected.

3. Artwork Recommendation Accuracy: The recommendation system may be limited to the input data and may not fully reflect personal preferences.

4. Real-Time Performance: This program may experience performance issues when processing large amounts of data in real-time.

5. The face detection process is reliant on two methods: Haar Cascade and DeepFace. While both are powerful, they may not always detect faces accurately, especially under poor lighting conditions, unusual angles, or occlusions (e.g., hats, glasses, etc.).
