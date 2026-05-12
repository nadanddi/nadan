from __future__ import annotations

import numpy as np
import pandas as pd



def generate_sample_data() -> pd.DataFrame:
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
    rows = []

    for date in dates:
        for stock_code, stock_name, market in stocks:
            for investor_type in investors:
                buy_amount = int(rng.integers(100, 3500)) * 1_000_000
                sell_amount = int(rng.integers(100, 3500)) * 1_000_000

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
