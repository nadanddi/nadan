from __future__ import annotations

"""
네이버 금융 수집기.

주의:
- 네이버 금융은 공식 고정 API가 아니므로 HTML 구조가 바뀌면 수집이 실패할 수 있다.
- 실패해도 앱 전체가 중단되지 않도록 FetchResult로 안전하게 반환한다.
- 현재 구현은 후보 URL의 HTML table을 읽고, 투자자별 수급 데이터로 해석 가능한 표만 표준 스키마로 변환한다.
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional
from urllib.request import Request, urlopen

import pandas as pd

STANDARD_COLUMNS = [
    "trade_date",
    "market",
    "stock_code",
    "stock_name",
    "investor_type",
    "buy_amount",
    "sell_amount",
    "net_amount",
]


@dataclass
class FetchResult:
    success: bool
    message: str
    dataframe: Optional[pd.DataFrame] = None


class NaverFinanceCollector:
    def __init__(self):
        self.source_name = "Naver Finance"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

    def fetch_daily_investor_flow(self) -> FetchResult:
        """후보 URL에서 기관/외국인 수급 데이터를 수집한다.

        현재는 네이버 금융 HTML table 구조에 의존한다. 구조가 맞는 표를 찾지 못하면 실패 결과를 반환한다.
        """
        candidate_urls = [
            # 네이버 금융 투자자별 매매동향 계열 후보 URL.
            # 페이지 구조 변경 가능성이 있어 여러 후보를 순회한다.
            "https://finance.naver.com/sise/sise_deal_rank.naver?sosok=0",
            "https://finance.naver.com/sise/sise_deal_rank.naver?sosok=1",
            "https://finance.naver.com/sise/investorDealTrendDay.naver",
        ]

        errors: list[str] = []

        for url in candidate_urls:
            try:
                html = self._download_html(url)
                tables = pd.read_html(html)
            except Exception as exc:
                errors.append(f"{url}: {exc}")
                continue

            parsed = self._parse_tables(tables)
            if parsed is not None and not parsed.empty:
                return FetchResult(
                    success=True,
                    message=f"네이버 금융 데이터를 수집했습니다: {url}",
                    dataframe=parsed,
                )

            errors.append(f"{url}: 해석 가능한 표를 찾지 못했습니다.")

        return FetchResult(
            success=False,
            message=(
                "네이버 금융 데이터 수집에 실패했습니다. "
                "페이지 구조 변경 또는 네트워크 제한 가능성이 있습니다. "
                f"상세: {' | '.join(errors[:3])}"
            ),
            dataframe=None,
        )

    def _download_html(self, url: str) -> str:
        request = Request(url, headers=self.headers)
        with urlopen(request, timeout=10) as response:
            raw = response.read()

        return raw.decode("euc-kr", errors="ignore")

    def _parse_tables(self, tables: list[pd.DataFrame]) -> Optional[pd.DataFrame]:
        frames: list[pd.DataFrame] = []

        for table in tables:
            cleaned = self._clean_table(table)
            if cleaned is None or cleaned.empty:
                continue

            frames.append(cleaned)

        if not frames:
            return None

        result = pd.concat(frames, ignore_index=True)
        result = result.drop_duplicates(subset=["trade_date", "stock_code", "investor_type"])
        return result[STANDARD_COLUMNS]

    def _clean_table(self, table: pd.DataFrame) -> Optional[pd.DataFrame]:
        df = table.copy()
        df = df.dropna(how="all")

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ["_".join([str(part) for part in col if str(part) != "nan"]) for col in df.columns]
        else:
            df.columns = [str(col) for col in df.columns]

        # 네이버 표는 종목명/현재가/등락률/기관/외국인 등 컬럼명이 페이지마다 다르게 나올 수 있다.
        stock_col = self._find_column(df, ["종목명", "종목"])
        foreign_col = self._find_column(df, ["외국인", "외국계"])
        institution_col = self._find_column(df, ["기관"])

        if stock_col is None or (foreign_col is None and institution_col is None):
            return None

        stock_code_col = self._find_column(df, ["종목코드", "코드"])
        market = "UNKNOWN"
        today = date.today().isoformat()

        rows: list[dict] = []

        for _, row in df.iterrows():
            stock_name = str(row.get(stock_col, "")).strip()
            if not stock_name or stock_name == "nan" or stock_name in {"종목명", "합계"}:
                continue

            stock_code = ""
            if stock_code_col is not None:
                stock_code = str(row.get(stock_code_col, "")).split(".")[0].zfill(6)

            if foreign_col is not None:
                net_amount = self._parse_number(row.get(foreign_col))
                rows.append(self._build_row(today, market, stock_code, stock_name, "foreign", net_amount))

            if institution_col is not None:
                net_amount = self._parse_number(row.get(institution_col))
                rows.append(self._build_row(today, market, stock_code, stock_name, "institution", net_amount))

        if not rows:
            return None

        return pd.DataFrame(rows)

    def _build_row(
        self,
        trade_date: str,
        market: str,
        stock_code: str,
        stock_name: str,
        investor_type: str,
        net_amount: float,
    ) -> dict:
        buy_amount = max(net_amount, 0.0)
        sell_amount = abs(min(net_amount, 0.0))

        return {
            "trade_date": trade_date,
            "market": market,
            "stock_code": stock_code,
            "stock_name": stock_name,
            "investor_type": investor_type,
            "buy_amount": buy_amount,
            "sell_amount": sell_amount,
            "net_amount": net_amount,
        }

    @staticmethod
    def _find_column(df: pd.DataFrame, keywords: list[str]) -> Optional[str]:
        for col in df.columns:
            col_text = str(col)
            if any(keyword in col_text for keyword in keywords):
                return col
        return None

    @staticmethod
    def _parse_number(value) -> float:
        if pd.isna(value):
            return 0.0

        text = str(value).replace(",", "").replace("+", "").strip()
        text = text.replace("억", "00000000").replace("만", "0000")

        try:
            return float(text)
        except ValueError:
            return 0.0
