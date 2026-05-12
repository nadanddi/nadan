from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

REQUIRED_COLUMNS = {
    "trade_date",
    "market",
    "stock_code",
    "stock_name",
    "investor_type",
    "buy_amount",
    "sell_amount",
    "net_amount",
}

INVESTOR_LABELS = {
    "institution": "기관",
    "foreign": "외국인",
}


st.set_page_config(
    page_title="Investor Flow Tracker",
    page_icon="📈",
    layout="wide",
)


@st.cache_data
def load_sample_data() -> pd.DataFrame:
    dates = pd.bdate_range(end=pd.Timestamp.today().normalize(), periods=10)
    stocks = [
        ("005930", "삼성전자", "KOSPI"),
        ("000660", "SK하이닉스", "KOSPI"),
        ("035420", "NAVER", "KOSPI"),
        ("005380", "현대차", "KOSPI"),
        ("051910", "LG화학", "KOSPI"),
        ("068270", "셀트리온", "KOSPI"),
        ("035720", "카카오", "KOSPI"),
        ("247540", "에코프로비엠", "KOSDAQ"),
        ("086520", "에코프로", "KOSDAQ"),
        ("196170", "알테오젠", "KOSDAQ"),
    ]
    investors = ["institution", "foreign"]

    rng = np.random.default_rng(42)
    rows: list[dict] = []

    for date in dates:
        for stock_code, stock_name, market in stocks:
            for investor_type in investors:
                buy_amount = int(rng.integers(100, 3500)) * 1_000_000
                sell_amount = int(rng.integers(100, 3500)) * 1_000_000

                # 샘플 데이터에서 연속 순매수/순매도 패턴이 보이도록 일부 종목에 bias를 준다.
                if stock_name == "삼성전자" and investor_type == "institution":
                    buy_amount += 4_000_000_000
                if stock_name == "SK하이닉스" and investor_type == "foreign":
                    buy_amount += 3_000_000_000
                if stock_name == "카카오" and investor_type == "institution":
                    sell_amount += 2_500_000_000
                if stock_name == "에코프로" and investor_type == "foreign":
                    sell_amount += 2_000_000_000

                rows.append(
                    {
                        "trade_date": date.date().isoformat(),
                        "market": market,
                        "stock_code": stock_code,
                        "stock_name": stock_name,
                        "investor_type": investor_type,
                        "buy_amount": buy_amount,
                        "sell_amount": sell_amount,
                        "net_amount": buy_amount - sell_amount,
                    }
                )

    return pd.DataFrame(rows)


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"필수 컬럼이 없습니다: {sorted(missing)}")

    result = df.copy()
    result["trade_date"] = pd.to_datetime(result["trade_date"]).dt.date
    result["investor_type"] = result["investor_type"].astype(str).str.lower()

    for col in ["buy_amount", "sell_amount", "net_amount"]:
        result[col] = pd.to_numeric(result[col], errors="coerce").fillna(0).astype(float)

    return result.sort_values(["trade_date", "stock_code", "investor_type"])


def format_won(value: float) -> str:
    abs_value = abs(value)
    if abs_value >= 100_000_000:
        return f"{value / 100_000_000:,.1f}억"
    if abs_value >= 10_000:
        return f"{value / 10_000:,.0f}만"
    return f"{value:,.0f}원"


def display_money_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()
    for col in ["buy_amount", "sell_amount", "net_amount", "cumulative_amount"]:
        if col in result.columns:
            result[col] = result[col].apply(format_won)
    return result


def get_top5(df: pd.DataFrame, investor_type: str, side: str) -> pd.DataFrame:
    latest_date = df["trade_date"].max()
    latest = df[(df["trade_date"] == latest_date) & (df["investor_type"] == investor_type)].copy()

    sort_col = "buy_amount" if side == "buy" else "sell_amount"
    cols = ["stock_name", "stock_code", "market", "buy_amount", "sell_amount", "net_amount"]
    return latest.sort_values(sort_col, ascending=False).head(5)[cols]


def calculate_streaks(df: pd.DataFrame, investor_type: str, direction: str, min_days: int = 4) -> pd.DataFrame:
    target = df[df["investor_type"] == investor_type].copy()
    results: list[dict] = []

    for (stock_code, stock_name, market), group in target.groupby(["stock_code", "stock_name", "market"]):
        group = group.sort_values("trade_date")
        current_days = 0
        current_amount = 0.0
        last_date = None

        for _, row in group.iterrows():
            net = float(row["net_amount"])
            is_match = net > 0 if direction == "buy" else net < 0

            if is_match:
                current_days += 1
                current_amount += net if direction == "buy" else abs(net)
                last_date = row["trade_date"]
            else:
                current_days = 0
                current_amount = 0.0
                last_date = None

        if current_days >= min_days:
            results.append(
                {
                    "stock_name": stock_name,
                    "stock_code": stock_code,
                    "market": market,
                    "streak_days": current_days,
                    "cumulative_amount": current_amount,
                    "last_date": last_date,
                }
            )

    result = pd.DataFrame(results)
    if result.empty:
        return result

    return result.sort_values(["cumulative_amount", "streak_days"], ascending=False)


def render_top5_section(df: pd.DataFrame, investor_type: str) -> None:
    label = INVESTOR_LABELS[investor_type]
    st.markdown(f"## {label}")
    buy_tab, sell_tab = st.tabs(["매수 Top 5", "매도 Top 5"])

    with buy_tab:
        st.dataframe(display_money_columns(get_top5(df, investor_type, "buy")), use_container_width=True)

    with sell_tab:
        st.dataframe(display_money_columns(get_top5(df, investor_type, "sell")), use_container_width=True)


def render_streak_section(df: pd.DataFrame, investor_type: str, min_days: int) -> None:
    label = INVESTOR_LABELS[investor_type]
    st.markdown(f"## {label} 연속 수급")

    buy_streak = calculate_streaks(df, investor_type, "buy", min_days)
    sell_streak = calculate_streaks(df, investor_type, "sell", min_days)

    simple_buy_tab, amount_buy_tab, simple_sell_tab, amount_sell_tab = st.tabs(
        ["연속 순매수 종목", "연속 순매수 총량 Top 5", "연속 순매도 종목", "연속 순매도 총량 Top 5"]
    )

    with simple_buy_tab:
        if buy_streak.empty:
            st.info(f"{min_days}일 이상 연속 순매수 종목이 없습니다.")
        else:
            simple = buy_streak.sort_values(["streak_days", "last_date"], ascending=False)
            st.dataframe(display_money_columns(simple), use_container_width=True)

    with amount_buy_tab:
        if buy_streak.empty:
            st.info(f"{min_days}일 이상 연속 순매수 종목이 없습니다.")
        else:
            st.dataframe(display_money_columns(buy_streak.head(5)), use_container_width=True)

    with simple_sell_tab:
        if sell_streak.empty:
            st.info(f"{min_days}일 이상 연속 순매도 종목이 없습니다.")
        else:
            simple = sell_streak.sort_values(["streak_days", "last_date"], ascending=False)
            st.dataframe(display_money_columns(simple), use_container_width=True)

    with amount_sell_tab:
        if sell_streak.empty:
            st.info(f"{min_days}일 이상 연속 순매도 종목이 없습니다.")
        else:
            st.dataframe(display_money_columns(sell_streak.head(5)), use_container_width=True)


st.title("📈 Investor Flow Tracker")
st.caption("기관 및 외국인 매수·매도 흐름을 빠르게 확인하는 대시보드")

with st.sidebar:
    st.header("설정")
    uploaded_file = st.file_uploader("CSV 업로드", type=["csv"])
    market_option = st.selectbox("시장", ["전체", "KOSPI", "KOSDAQ"])
    min_days = st.number_input("연속 수급 기준일", min_value=2, max_value=20, value=4, step=1)

try:
    raw_df = pd.read_csv(uploaded_file) if uploaded_file else load_sample_data()
    df = normalize_data(raw_df)
except Exception as exc:
    st.error(f"데이터를 불러오지 못했습니다: {exc}")
    st.stop()

if market_option != "전체":
    df = df[df["market"] == market_option]

if df.empty:
    st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
    st.stop()

latest_date = df["trade_date"].max()
st.info(f"최신 데이터 기준일: {latest_date} · 데이터 출처: 샘플/업로드 CSV")

st.header("오늘의 매수·매도 Top 5")
col1, col2 = st.columns(2)
with col1:
    render_top5_section(df, "institution")
with col2:
    render_top5_section(df, "foreign")

st.divider()
st.header(f"{min_days}일 이상 연속 수급")
render_streak_section(df, "institution", min_days)
st.divider()
render_streak_section(df, "foreign", min_days)

st.divider()
with st.expander("CSV 컬럼 형식 보기"):
    st.code(
        "trade_date,market,stock_code,stock_name,investor_type,buy_amount,sell_amount,net_amount\n"
        "2026-05-13,KOSPI,005930,삼성전자,institution,1000000000,500000000,500000000",
        language="csv",
    )
