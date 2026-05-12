# 📈 Investor Flow Tracker

기관 및 외국인의 매수·매도 흐름을 빠르게 확인하기 위한 Streamlit 기반 대시보드.

## 주요 기능

- 기관 매수 Top 5
- 기관 매도 Top 5
- 외국인 매수 Top 5
- 외국인 매도 Top 5
- 4일 이상 연속 순매수 종목
- 4일 이상 연속 순매도 종목
- 연속 순매수 누적금액 Top 5
- 연속 순매도 누적금액 Top 5
- KOSPI / KOSDAQ 필터
- iPhone Safari 대응 반응형 UI

---

## 기술 스택

| 영역 | 기술 |
|---|---|
| Frontend | Streamlit |
| Data Processing | pandas |
| Language | Python |
| Storage | CSV 기반 MVP |

---

## 실행 방법

### 1. 저장소 클론

```bash
git clone https://github.com/nadanddi/nadan.git
cd nadan
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. 앱 실행

```bash
streamlit run app.py
```

---

## CSV 형식

```csv
trade_date,market,stock_code,stock_name,investor_type,buy_amount,sell_amount,net_amount
2026-05-13,KOSPI,005930,삼성전자,institution,1000000000,500000000,500000000
```

---

## investor_type

지원 값:

```text
institution
foreign
```

---

## 연속 수급 규칙

### 연속 순매수

```text
net_amount > 0
```

### 연속 순매도

```text
net_amount < 0
```

기본 기준:

```text
4거래일 이상 연속
```

---

## 향후 계획

- 네이버 금융 데이터 자동 수집
- KRX 보조 데이터 연결
- SQLite 저장
- 자동 갱신 스케줄러
- 연기금/투신 확장
- 모바일 UI 개선
- 실시간 데이터 대응
- 알림 기능

---

## 현재 상태

현재 버전은 MVP이며:

- 샘플 데이터 또는 업로드 CSV 기반으로 실행 가능
- LG Gram 노트북 및 iPhone Safari 환경 대응
- Streamlit 기반 반응형 웹앱
