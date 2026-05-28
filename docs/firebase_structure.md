# Firebase Structure

## users collection

사용자 계정 및 개인 설정 저장

### fields
- uid
- email
- baseline_coords
- created_at


## sessions collection

학습 세션 결과 저장

### fields
- uid
- posture_score
- warning_count
- created_at


## logs collection

자세 이상 감지 기록 저장

### fields
- session_id
- type
- timestamp