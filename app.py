from __future__ import annotations

import pandas as pd
import streamlit as st

from src.analytics import calculate_streaks, get_top5, normalize_data
from src.formatters import display_money_columns
from src.naver_finance import NaverFinanceCollector
from src.sample_data import generate_sample_data
from src.storage import InvestorFlowStorage

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
    return generate_sample_data()


@st.cache_resource
def get_storage() -> InvestorFlowStorage:
    return InvestorFlowStorage()


def load_database_data(storage: InvestorFlowStorage) -> pd.DataFrame:
    if not storage.has_data():
        return pd.DataFrame()

    return storage.load_dataframe()


def render_top5_section(df: pd.DataFrame, investor_type: str) -> None:
    label = INVESTOR_LABELS[investor_type]
    st.markdown(f"## {label}")
    buy_tab, sell_tab = st.tabs(["매수 Top 5", "매도 Top 5"])

    with buy_tab:
        st.dataframe(
            display_money_columns(get_top5(df, investor_type, "buy")),
            use_container_width=True,
            hide_index=True,
        )

    with sell_tab:
        st.dataframe(
            display_money_columns(get_top5(df, investor_type, "sell")),
            use_container_width=True,
            hide_index=True,
        )


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
            st.dataframe(display_money_columns(simple), use_container_width=True, hide_index=True)

    with amount_buy_tab:
        if buy_streak.empty:
            st.info(f"{min_days}일 이상 연속 순매수 종목이 없습니다.")
        else:
            st.dataframe(display_money_columns(buy_streak.head(5)), use_container_width=True, hide_index=True)

    with simple_sell_tab:
        if sell_streak.empty:
            st.info(f"{min_days}일 이상 연속 순매도 종목이 없습니다.")
        else:
            simple = sell_streak.sort_values(["streak_days", "last_date"], ascending=False)
            st.dataframe(display_money_columns(simple), use_container_width=True, hide_index=True)

    with amount_sell_tab:
        if sell_streak.empty:
            st.info(f"{min_days}일 이상 연속 순매도 종목이 없습니다.")
        else:
            st.dataframe(display_money_columns(sell_streak.head(5)), use_container_width=True, hide_index=True)


st.title("📈 Investor Flow Tracker")
st.caption("기관 및 외국인 매수·매도 흐름을 빠르게 확인하는 대시보드")

storage = get_storage()

with st.sidebar:
    st.header("설정")

    data_source = st.radio(
        "데이터 소스",
        ["샘플 데이터", "CSV 업로드", "SQLite DB"],
        index=0,
    )

    uploaded_file = None
    if data_source == "CSV 업로드":
        uploaded_file = st.file_uploader("CSV 업로드", type=["csv"])

    market_option = st.selectbox("시장", ["전체", "KOSPI", "KOSDAQ"])
    min_days = st.number_input("연속 수급 기준일", min_value=2, max_value=20, value=4, step=1)

    st.divider()
    st.subheader("데이터 관리")

    if st.button("샘플 데이터를 DB에 저장", use_container_width=True):
        sample_df = normalize_data(load_sample_data())
        storage.save_dataframe(sample_df, replace=True)
        st.success("샘플 데이터를 SQLite DB에 저장했습니다.")
        st.cache_data.clear()

    if uploaded_file is not None and st.button("업로드 CSV를 DB에 저장", use_container_width=True):
        uploaded_df = normalize_data(pd.read_csv(uploaded_file))
        storage.save_dataframe(uploaded_df, replace=True)
        st.success("업로드 CSV를 SQLite DB에 저장했습니다.")
        st.cache_data.clear()

    if st.button("네이버 금융 수집 시도", use_container_width=True):
        collector = NaverFinanceCollector()
        result = collector.fetch_daily_investor_flow()

        if result.success and result.dataframe is not None:
            fetched_df = normalize_data(result.dataframe)
            storage.save_dataframe(fetched_df, replace=False)
            st.success("네이버 금융 데이터를 DB에 저장했습니다.")
            st.cache_data.clear()
        else:
            st.warning(result.message)

try:
    if data_source == "CSV 업로드":
        if uploaded_file is None:
            st.info("CSV 파일을 업로드하면 분석을 시작합니다. 현재는 샘플 데이터를 표시합니다.")
            raw_df = load_sample_data()
        else:
            raw_df = pd.read_csv(uploaded_file)
    elif data_source == "SQLite DB":
        raw_df = load_database_data(storage)
        if raw_df.empty:
            st.info("SQLite DB에 데이터가 없습니다. 샘플 데이터를 표시합니다.")
            raw_df = load_sample_data()
    else:
        raw_df = load_sample_data()

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
st.info(f"최신 데이터 기준일: {latest_date} · 데이터 소스: {data_source}")

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
