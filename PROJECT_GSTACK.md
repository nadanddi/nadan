# Project GStack Workflow

## 1. 목적

이 문서는 gstack의 sprint 기반 AI coding workflow를 참고하여, 이 프로젝트에서 코딩 작업을 더 체계적으로 진행하기 위한 운영 방식을 정의한다.

핵심 목적은 다음과 같다.

- 막연한 코딩 요청을 명확한 task로 바꾼다.
- 작업을 Think → Plan → Build → Review → Test → Ship → Reflect 흐름으로 진행한다.
- 각 단계별 역할을 나누어 품질을 높인다.
- 코드 수정 후 반드시 리뷰, 테스트, 문서화를 거친다.
- 반복되는 작업은 reusable skill로 축적한다.

---

## 2. GStack식 Sprint Flow

기본 흐름은 다음과 같다.

```text
Think → Plan → Build → Review → Test → Ship → Reflect
```

| 단계 | 역할 | 이 프로젝트에서의 적용 |
|---|---|---|
| Think | 문제 재정의 | 사용자의 요청을 실제 해결해야 할 문제로 바꾼다. |
| Plan | 구현 계획 수립 | 수정 파일, 영향 범위, 리스크를 정리한다. |
| Build | 코드 작성/수정 | 최소 수정 원칙으로 코드를 작성한다. |
| Review | 코드 리뷰 | 버그, 중복, 과복잡성, 누락을 점검한다. |
| Test | 실행 검증 | 수동 테스트, 단위 테스트, 제출 파일 검증을 수행한다. |
| Ship | 제출/반영 | 실행 가능한 최종 코드와 수정 기록을 남긴다. |
| Reflect | 회고/축적 | 실패 원인과 재사용 가능한 skill을 문서화한다. |

---

## 3. 역할 기반 작업 방식

이 프로젝트에서는 하나의 작업을 다음 역할 관점에서 점검한다.

### 3.1 Product / CEO Review

목적:
- 요청이 실제 목표와 맞는지 확인한다.
- 불필요하게 큰 범위를 줄인다.
- 지금 해야 할 가장 작은 실험 단위를 정한다.

질문:
- 이 작업의 최종 목표는 무엇인가?
- 지금 꼭 필요한 변경인가?
- 더 작은 단위로 쪼갤 수 있는가?
- 성능 개선인지, 오류 수정인지, 제출 안정화인지 구분되었는가?

---

### 3.2 Engineering Review

목적:
- 코드 구조, 데이터 흐름, 의존성, 예외 상황을 점검한다.

질문:
- 어떤 파일을 수정해야 하는가?
- 기존 구조와 충돌하지 않는가?
- import, 경로, 컬럼명, 타입이 맞는가?
- GPU/CPU 환경에서 모두 실행 가능한가?
- 실패했을 때 로그가 충분한가?

---

### 3.3 Design / UX Review

ML/Kaggle 프로젝트에서도 UX는 중요하다. 여기서는 사용자 인터페이스보다 코드 사용성을 의미한다.

질문:
- 초보자가 실행 순서를 이해할 수 있는가?
- 변수명과 경로가 명확한가?
- 출력 로그가 읽기 쉬운가?
- 제출 파일 생성 과정이 실수하기 어렵게 되어 있는가?

---

### 3.4 QA Review

목적:
- 코드가 실제로 실행 가능한지 검증한다.

점검 항목:
- 문법 오류
- import 오류
- 데이터 경로 오류
- 컬럼명 불일치
- 모델 로딩 실패
- submission 형식 오류
- validation metric 계산 오류
- seed 재현성

---

### 3.5 Security / Safety Review

목적:
- 위험한 명령, 비밀키 노출, 파괴적 작업을 방지한다.

점검 항목:
- API key 하드코딩 여부
- 토큰/비밀번호 노출 여부
- `rm -rf`, force push 등 파괴적 명령 여부
- 외부 파일 다운로드 코드의 안전성
- 임의 실행 코드 위험성

---

## 4. 이 프로젝트의 Slash Command식 작업 모드

실제 slash command를 쓰지 않더라도, 다음 모드 이름을 작업 기준으로 사용한다.

| 모드 | 의미 | 사용 시점 |
|---|---|---|
| `/think` | 문제 재정의 | 요청이 모호하거나 범위가 클 때 |
| `/plan` | 구현 계획 | 코드 수정 전 |
| `/build` | 코드 작성 | 실제 코드 생성/수정 시 |
| `/review` | 코드 리뷰 | 수정 후 품질 점검 |
| `/qa` | 실행 테스트 | 제출 전/실행 전 |
| `/ship` | 최종 반영 | 최종 코드 제공/커밋 전 |
| `/retro` | 회고 | 실험 종료 후 |
| `/investigate` | 원인 분석 | 에러 발생 시 |
| `/guard` | 안전 모드 | 파일 삭제, 배포, 강제 변경 가능성이 있을 때 |
| `/learn` | skill 축적 | 반복 가능한 해결 패턴 발견 시 |

---

## 5. 기본 작업 템플릿

새 코딩 작업은 다음 템플릿으로 시작한다.

```md
## Task

### 목표

### 현재 상황

### 수정할 파일

### 예상 영향 범위

### 주의할 점
```

작업 완료 후에는 다음 템플릿으로 마무리한다.

```md
## Result

### 수정 파일

### 변경 내용

### 테스트 결과

### 남은 리스크

### 재사용 가능한 skill
```

---

## 6. Kaggle / ML 전용 Sprint 예시

### 예시 1: 라이브러리 오류 수정

```text
Think: import 오류가 버전 충돌인지 코드 문제인지 구분
Plan: transformers, peft, accelerate 버전 확인
Build: 최소 버전 수정 코드 작성
Review: 다른 import에 영향 없는지 확인
Test: 런타임 재시작 후 import 테스트
Ship: 수정 코드와 실행 순서 제공
Reflect: 오류 해결 skill로 기록
```

---

### 예시 2: 리더보드 점수 개선

```text
Think: public LB와 validation gap 원인 정의
Plan: split, metric, threshold, leakage 점검
Build: 실험 코드 수정
Review: 과적합 위험 확인
Test: validation score와 submission 생성 확인
Ship: 제출 파일 생성
Reflect: 실험 결과와 다음 아이디어 기록
```

---

### 예시 3: 제출 파일 생성 오류

```text
Think: submission 형식 문제인지 prediction 문제인지 분리
Plan: sample_submission 컬럼 확인
Build: ID/generated 또는 ID/target 형식 맞춤
Review: 행 수와 순서 확인
Test: csv 저장 후 다시 읽기
Ship: 최종 submission.csv 생성
Reflect: submission 검증 skill로 기록
```

---

## 7. Parallel Sprint 운영 규칙

여러 작업을 동시에 진행해야 할 때는 작업을 분리한다.

좋은 병렬 작업 예시:

- A: import 오류 해결
- B: submission 생성 검증
- C: validation metric 점검
- D: README 실행 방법 정리

나쁜 병렬 작업 예시:

- 모든 모델 개선
- 전체 코드 리팩토링
- 모든 오류 한 번에 해결

병렬 작업 원칙:

- 각 sprint는 독립적인 목표를 가진다.
- 같은 파일을 동시에 수정하지 않는다.
- 완료 기준을 명확히 한다.
- 작업 결과를 `PROJECT_TODO.md`에 반영한다.

---

## 8. Review Readiness Checklist

작업을 ship하기 전에 아래 항목을 확인한다.

- [ ] 작업 목표가 명확한가?
- [ ] 수정 범위가 최소화되었는가?
- [ ] 코드 실행 순서가 명확한가?
- [ ] import 오류 가능성을 확인했는가?
- [ ] 데이터 경로와 컬럼명을 확인했는가?
- [ ] submission 형식이 맞는가?
- [ ] 테스트 방법을 제공했는가?
- [ ] 남은 리스크를 기록했는가?
- [ ] 반복 가능한 skill로 남길 수 있는가?

---

## 9. Reflect / Learn 규칙

작업이 끝난 뒤 다음 중 하나 이상을 문서에 남긴다.

- 새로 알게 된 오류 패턴
- 재사용 가능한 코드 패턴
- 성능 개선에 효과 있었던 실험
- 실패한 실험과 이유
- 다음에 피해야 할 접근

기록 위치:

| 내용 | 파일 |
|---|---|
| 작업 현황 | `PROJECT_TODO.md` |
| 결정 이유 | `PROJECT_CONTEXT.md` |
| 반복 skill | `PROJECT_COMPOUND.md` |
| sprint workflow | `PROJECT_GSTACK.md` |

---

## 10. 최종 원칙

좋은 AI coding workflow는 코드를 많이 쓰는 것이 아니라, 문제를 잘 정의하고 검증 가능한 작은 단위로 빠르게 ship하는 것이다.

이 프로젝트에서는 항상 다음 순서를 우선한다.

1. 문제를 다시 정의한다.
2. 작게 계획한다.
3. 최소 수정한다.
4. 리뷰한다.
5. 테스트한다.
6. 기록한다.
7. 다음 작업에서 재사용한다.
