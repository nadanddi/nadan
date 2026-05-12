# Project Compound Workflow

## 1. 목적

이 문서는 코딩 프로젝트에서 작업 경험을 일회성 답변으로 끝내지 않고, 반복 가능한 skill과 workflow로 축적하기 위한 compound 과정을 정의한다.

참고 개념:

- 작업을 issue/task 단위로 관리한다.
- 진행 상황과 blocker를 기록한다.
- 해결한 문제를 reusable skill로 남긴다.
- 시간이 지날수록 프로젝트의 문제 해결 능력이 누적되도록 한다.

---

## 2. Compound의 의미

여기서 compound는 단순히 여러 기능을 합친다는 뜻이 아니라, 작업 결과가 다음 작업의 자산으로 누적되는 과정을 의미한다.

예를 들어 한 번 해결한 `transformers`, `peft`, `accelerate` 버전 충돌 문제는 다음에 다시 발생했을 때 처음부터 분석하지 않고, 해결 skill로 재사용한다.

---

## 3. 기본 Compound Loop

모든 작업은 다음 루프를 따른다.

```text
Task → Analyze → Fix → Test → Review → Document → Reuse
```

| 단계 | 설명 | 산출물 |
|---|---|---|
| Task | 해결할 작업 정의 | 작업 목표, 범위 |
| Analyze | 코드/오류/환경 분석 | 원인 후보, 영향 범위 |
| Fix | 최소 수정 적용 | 수정 코드 |
| Test | 실행 및 검증 | 테스트 결과 |
| Review | 품질 점검 | QA 체크리스트 |
| Document | 결정 이유 기록 | context, todo, log |
| Reuse | skill로 재사용 | reusable pattern |

---

## 4. Skill Compounding Rules

### 4.1 오류 해결 skill화

오류를 해결한 뒤 다음 정보를 기록한다.

- 오류 메시지
- 발생 환경
- 직접 원인
- 해결 코드
- 재발 방지 방법
- 다음에 재사용할 조건

예시:

```md
## Skill: Transformers Import Error Fix

### Trigger
`cannot import name 'EncoderDecoderCache' from 'transformers'`

### Context
- transformers와 peft 버전 불일치
- Kaggle Notebook 환경

### Fix Pattern
- transformers/peft/accelerate 버전 조합 확인
- 호환 가능한 버전으로 맞춤
- 런타임 재시작

### Reuse Condition
Hugging Face 계열 import 오류가 발생했을 때 우선 적용
```

---

### 4.2 실험 skill화

ML 실험 후 다음 정보를 기록한다.

- 실험 목적
- 사용 데이터
- 모델명
- 주요 하이퍼파라미터
- validation score
- leaderboard score
- 실패/성공 판단
- 다음 실험 아이디어

---

### 4.3 코드 수정 skill화

반복되는 코드 수정 패턴은 다음 형식으로 기록한다.

- 수정 전 문제
- 수정 위치
- 최소 수정 방법
- 테스트 방법
- 주의할 점

---

## 5. 작업 단위 운영 방식

작업은 가능한 한 작은 단위로 나눈다.

좋은 작업 단위:

- import 오류 해결
- submission 파일 생성 오류 수정
- validation metric 계산 수정
- inference batch size 조정
- README에 실행 방법 추가

나쁜 작업 단위:

- 모델 전체 성능 올리기
- 프로젝트 전체 개선하기
- 모든 오류 고치기

큰 작업은 반드시 작은 task로 분해한다.

---

## 6. Compound 기록 위치

| 기록 내용 | 권장 파일 |
|---|---|
| 전체 목표와 범위 | `PROJECT_PLAN.md` |
| 결정 이유와 맥락 | `PROJECT_CONTEXT.md` |
| 진행 상태 | `PROJECT_TODO.md` |
| 작업 skill 체계 | `PROJECT_SKILLS.md` |
| compound workflow | `PROJECT_COMPOUND.md` |
| 반복 오류 사례 | `docs/error_skills.md` |
| 실험 결과 | `experiments/README.md` |

---

## 7. 에이전트식 작업 흐름

작업자는 다음 방식으로 행동한다.

1. issue/task를 받는다.
2. 현재 코드와 문서를 읽는다.
3. 필요한 최소 변경을 설계한다.
4. 코드를 수정한다.
5. 테스트한다.
6. 결과를 보고한다.
7. 반복 가능한 해결법을 문서화한다.

---

## 8. Blocker 처리 규칙

작업 중 막히는 부분이 있으면 즉시 기록한다.

Blocker 기록 형식:

```md
## Blocker

### 문제

### 확인한 내용

### 가능한 원인

### 필요한 정보

### 임시 대응
```

Blocker는 숨기지 않고 다음 작업자가 바로 이어받을 수 있게 남긴다.

---

## 9. Compound Quality Checklist

작업 완료 후 아래 항목을 확인한다.

- [ ] 해결한 문제가 명확히 기록되었는가?
- [ ] 수정한 파일과 이유가 남아 있는가?
- [ ] 테스트 방법이 기록되었는가?
- [ ] 실패 원인 또는 리스크가 기록되었는가?
- [ ] 다음에 재사용할 수 있는 pattern이 있는가?
- [ ] `PROJECT_TODO.md`가 갱신되었는가?
- [ ] 필요하면 `PROJECT_CONTEXT.md`에 결정 이유가 추가되었는가?

---

## 10. 이 프로젝트의 우선 Compound 대상

현재 이 프로젝트에서 우선적으로 skill화할 대상은 다음과 같다.

1. Kaggle 라이브러리/환경 오류 해결
2. Hugging Face Transformers 버전 충돌 해결
3. PEFT/Accelerate import 오류 해결
4. train/test/submission 경로 검증
5. validation score와 leaderboard score 차이 분석
6. inference 후처리 및 threshold 튜닝
7. GPU 없는 환경에서의 fallback 실행

---

## 11. 최종 원칙

한 번 해결한 문제는 다음번에 더 빠르게 해결되어야 한다.

따라서 모든 작업은 다음 세 가지 중 하나를 남겨야 한다.

1. 더 나은 코드
2. 더 나은 문서
3. 더 재사용 가능한 skill
