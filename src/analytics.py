from __future__ import annotations

import pandas as pd

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


def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"필수 컬럼이 없습니다: {sorted(missing)}")

    result = df.copy()
    result["trade_date"] = pd.to_datetime(result["trade_date"]).dt.date
    result["investor_type"] = result["investor_type"].astype(str).str.lower()
    result["market"] = result["market"].astype(str).str.upper()
    result["stock_code"] = result["stock_code"].astype(str).str.zfill(6)

    for col in ["buy_amount", "sell_amount", "net_amount"]:
        result[col] = pd.to_numeric(result[col], errors="coerce").fillna(0).astype(float)

    return result.sort_values(["trade_date", "stock_code", "investor_type"])


def get_top5(df: pd.DataFrame, investor_type: str, side: str) -> pd.DataFrame:
    latest_date = df["trade_date"].max()
    latest = df[(df["trade_date"] == latest_date) & (df["investor_type"] == investor_type)].copy()

    sort_col = "buy_amount" if side == "buy" else "sell_amount"
    cols = ["stock_name", "stock_code", "market", "buy_amount", "sell_amount", "net_amount"]
    return latest.sort_values(sort_col, ascending=False).head(5)[cols]


def calculate_streaks(
    df: pd.DataFrame,
    investor_type: str,
    direction: str,
    min_days: int = 4,
) -> pd.DataFrame:
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
