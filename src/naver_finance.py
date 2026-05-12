from __future__ import annotations

"""
네이버 금융 수집기 초안.

현재는 실제 크롤링 대신 인터페이스와 향후 확장 구조만 정의한다.
실제 HTML 구조는 변경 가능성이 높으므로 selector 기반 파싱은 이후 단계에서 추가한다.
"""

from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class FetchResult:
    success: bool
    message: str
    dataframe: Optional[pd.DataFrame] = None


class NaverFinanceCollector:
    def __init__(self):
        self.source_name = "Naver Finance"

    def fetch_daily_investor_flow(self) -> FetchResult:
        return FetchResult(
            success=False,
            message=(
                "실제 네이버 금융 수집기는 아직 구현되지 않았습니다. "
                "현재는 MVP 구조와 데이터 계층만 준비된 상태입니다."
            ),
            dataframe=None,
        )
