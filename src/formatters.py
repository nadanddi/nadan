from __future__ import annotations

import pandas as pd



def format_won(value: float) -> str:
    abs_value = abs(value)

    if abs_value >= 100_000_000:
        return f"{value / 100_000_000:,.1f}억"

    if abs_value >= 10_000:
        return f"{value / 10_000:,.0f}만"

    return f"{value:,.0f}원"



def display_money_columns(df: pd.DataFrame) -> pd.DataFrame:
    result = df.copy()

    for col in [
        "buy_amount",
        "sell_amount",
        "net_amount",
        "cumulative_amount",
    ]:
        if col in result.columns:
            result[col] = result[col].apply(format_won)

    return result
