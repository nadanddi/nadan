# Project TODO

## 1. 완료한 작업

- [x] GitHub 저장소 연결 확인
- [x] `PROJECT_SKILLS.md` 생성
- [x] `PROJECT_PLAN.md` 생성
- [x] `PROJECT_CONTEXT.md` 생성
- [x] `PROJECT_TODO.md` 생성
- [x] Superpowers / Skill 기반 작업 체계 구성
- [x] Kaggle/ML 프로젝트 운영 규칙 정리

---

## 2. 진행 중인 작업

현재 진행 중인 핵심 방향:

- 코딩 프로젝트 작업 체계 정리
- 오류 수정 workflow 정리
- ML 실험 관리 구조 정리
- GitHub 기반 프로젝트 문서화

---

## 3. 남은 작업

### 3.1 저장소 구조

- [ ] 실제 코드 디렉토리 구조 추가
- [ ] `src/`, `notebooks/`, `configs/`, `models/` 구조 정의
- [ ] 공통 utility 코드 분리 여부 결정

---

### 3.2 머신러닝 실험 관리

- [ ] train/valid split 규칙 문서화
- [ ] inference pipeline 정리
- [ ] submission 생성 workflow 정리
- [ ] 실험 결과 비교 문서 추가
- [ ] validation/public LB 차이 사례 기록

---

### 3.3 오류 대응 체계

- [ ] 자주 발생한 오류 사례 정리
- [ ] transformers/peft/accelerate 버전 충돌 사례 정리
- [ ] import 오류 대응 체크리스트 추가
- [ ] GPU/CPU fallback 전략 정리

---

### 3.4 테스트 및 QA

- [ ] 최소 실행 테스트 템플릿 추가
- [ ] 데이터 경로 확인 체크리스트 추가
- [ ] 모델 로딩 검증 절차 추가
- [ ] submission 파일 검증 절차 추가

---

## 4. 테스트해야 할 항목

| 항목 | 상태 |
|---|---|
| GitHub 문서 정상 업로드 | 완료 |
| Markdown 렌더링 확인 | 진행 필요 |
| 문서 간 링크 연결 | 진행 필요 |
| README 연결 여부 | 진행 필요 |
| 실제 코드 추가 시 workflow 유지 | 진행 필요 |

---

## 5. 다음 우선순위

현재 가장 우선적으로 진행할 작업:

1. README 작성
2. 저장소 디렉토리 구조 정리
3. 실제 코드 추가
4. ML 실험 기록 구조 추가
5. 오류 해결 사례 축적

---

## 6. 운영 체크리스트

새 작업 시작 전:

- [ ] 목표 확인
- [ ] 수정 범위 확인
- [ ] 영향 범위 분석
- [ ] 기존 구조 확인

코드 수정 후:

- [ ] 문법 오류 확인
- [ ] import 오류 확인
- [ ] 타입 오류 확인
- [ ] 경로 오류 확인
- [ ] 예외 처리 확인
- [ ] 테스트 수행
- [ ] 수정 기록 작성

---

## 7. 장기 목표

- 반복 가능한 ML 실험 환경 구축
- 오류 재현 및 해결 속도 향상
- 코드 품질 자동 점검 체계 구축
- 프로젝트 문서화 자동화
- AI coding workflow 최적화
