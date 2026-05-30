# PoseGuard

AI 기반 실시간 자세 교정 및 거북목 방지 시스템

## 프로젝트 소개

PoseGuard는 웹캠과 MediaPipe를 활용하여 사용자의 자세를 실시간으로 분석하고, 잘못된 자세를 감지하여 경고 및 AI 기반 피드백을 제공하는 자세 교정 프로그램입니다.

장시간 컴퓨터를 사용하는 학생과 직장인의 거북목 및 자세 불균형 문제를 예방하고, 올바른 자세 습관 형성을 돕는 것을 목표로 합니다.

---

## 주요 기능

### 실시간 자세 인식

* OpenCV를 이용한 웹캠 영상 입력
* MediaPipe Pose 기반 신체 랜드마크 추출
* 귀(Ear) 및 어깨(Shoulder) 좌표 인식
* 랜드마크 시각화

### 자세 분석

* 귀와 어깨의 상대적 위치를 이용한 자세 평가
* 거북목 및 잘못된 자세 감지
* 자세 이상 여부 판별

### 자세 경고 시스템

* 잘못된 자세 감지 시 경고 메시지 출력
* 자세 상태에 따른 실시간 피드백 제공

### AI 건강 코멘트

* Google Gemini API 활용
* 자세 분석 결과 기반 맞춤형 코멘트 생성
* 자세 개선 방법 안내

### Firebase 연동

* Firebase Firestore 활용
* 자세 점수 및 경고 횟수 저장
* 세션 데이터 기록

---

## 시스템 구조

OpenCV → MediaPipe → 자세 분석 로직 → Gemini AI 코멘트 → Firebase 저장

---

## 사용 기술

### Language

* Python 3.12

### Vision

* OpenCV
* MediaPipe

### Frontend

* Tkinter

### AI

* Google Gemini API

### Database

* Firebase Firestore

### Library

* NumPy
* Matplotlib
* Pillow
* python-dotenv

---

## 프로젝트 구조

```text
PoseGuard
│
├── backend
│   ├── firebase_service.py
│   ├── firebase_test.py
│   └── firebase_key.json
│
├── frontend
│   └── app.py
│
├── logic
│   ├── posture_logic.py
│   └── gemini_advisor.py
│
├── vision
│   ├── camera.py
│   └── pose_detector.py
│
├── requirements.txt
└── README.md
```

---

## 실행 환경

### Tested Environment

* Python 3.12.9 / 3.12.10
* MediaPipe 0.10.21

※ Python 3.13 이상에서는 MediaPipe가 정상 동작하지 않을 수 있습니다.

---

## 설치 방법

```bash
pip install -r requirements.txt
```

---

## 실행 방법

### 메인 프로그램 실행

```bash
python -m frontend.app
```

### Vision 모듈 테스트

```bash
python -m vision.camera
```

### Firebase 저장 테스트

```bash
python backend/firebase_test.py
```

---

## 팀원 역할

| 이름       | 역할                             |
| -------- | ------------------------------ |
| 최우혁 (팀장) | 시스템 통합, Firebase 연동, Gemini 연동 |
| 최준수      | MediaPipe 기반 자세 인식 및 영상 처리     |
| 원준혁      | 자세 분석 로직 구현                    |
| 한지수      | UI 설계 및 사용자 인터페이스 구현           |

---

## 기대 효과

* 거북목 예방
* 올바른 자세 습관 형성
* 장시간 학습 환경 개선
* AI 기반 개인 맞춤형 피드백 제공

---

## 참고 자료

* MediaPipe
* OpenCV
* Firebase Firestore
* Google Gemini API
* Matplotlib
