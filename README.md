# PoseGuard

## AI 기반 자세 분석 및 거북목 방지 시스템

### 프로젝트 소개

PoseGuard는 웹캠과 MediaPipe를 활용하여 사용자의 자세를 분석하고, 거북목 및 라운드숄더 여부를 판단하여 교정 코멘트를 제공하는 Python 기반 자세 분석 프로그램입니다.

사용자는 먼저 기준 자세(Baseline)를 저장한 뒤 측정 자세와 비교하여 자세 상태를 확인할 수 있으며, Google Gemini API를 통해 맞춤형 자세 교정 코멘트를 받을 수 있습니다. 또한 측정 결과는 Firebase Firestore에 저장되어 향후 자세 기록 관리 기능으로 확장할 수 있습니다.

---

## 주요 기능

### 자세 인식

* OpenCV를 이용한 웹캠 영상 입력
* MediaPipe Pose 기반 신체 랜드마크 추출
* 귀(Ear) 및 어깨(Shoulder) 좌표 인식
* 랜드마크 시각화

### 자세 분석

* 기준 자세(Baseline) 저장
* 측정 종료 시 마지막 자세 데이터 분석
* 거북목(Forward Head Posture) 감지
* 라운드숄더(Rounded Shoulder) 감지
* 자세 이상 여부 판별

### 자세 피드백

* 잘못된 자세 감지 시 경고 메시지 출력
* 자세 상태에 따른 교정 코멘트 제공
* 정상 자세 유지 시 긍정 피드백 제공

### AI 건강 코멘트

* Google Gemini API 활용
* 자세 분석 결과 기반 맞춤형 코멘트 생성
* Gemini API 실패 시 기본 교정 문구 제공

### Firebase 연동

* Firebase Firestore 활용
* 자세 점수(Posture Score) 저장
* 경고 횟수(Warning Count) 저장
* 세션 데이터 기록

---

## 시스템 구조

```text
OpenCV
   ↓
MediaPipe Pose
   ↓
Posture Analysis Logic
   ↓
Gemini AI Comment
   ↓
Firebase Firestore
```

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
├── docs
│   ├── PoseGuard_사용자가이드.docx
│   ├── PoseGuard_개발자가이드.docx
│   ├── workflow.md
│   ├── data_format.md
│   ├── api_structure.md
│   └── firebase_structure.md
│
├── requirements.txt
└── README.md
```

---

## 실행 환경

### Tested Environment

* Python 3.12.9 / 3.12.10
* MediaPipe 0.10.21

> Python 3.13 이상에서는 MediaPipe가 정상 동작하지 않을 수 있습니다.

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

## 문서

* [사용자 가이드](docs/PoseGuard_사용자가이드.docx)
* [개발자 가이드](docs/PoseGuard_개발자가이드.docx)

---

## 팀원 역할

| 이름       | 역할                                 |
| -------- | ---------------------------------- |
| 최우혁 (팀장) | 시스템 통합, Firebase 연동, Gemini API 연동 |
| 최준수      | MediaPipe 기반 자세 인식 및 영상 처리         |
| 원준혁      | 자세 분석 로직 구현                        |
| 한지수      | UI 설계 및 사용자 인터페이스 구현               |

---

## 기대 효과

* 거북목 예방
* 라운드숄더 예방
* 올바른 자세 습관 형성
* 장시간 학습 및 업무 환경 개선
* AI 기반 개인 맞춤형 자세 피드백 제공

---

## 참고 자료

* MediaPipe
* OpenCV
* Firebase Firestore
* Google Gemini API
