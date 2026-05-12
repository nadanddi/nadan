from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd

DB_DIR = Path("data")
DB_PATH = DB_DIR / "investor_flow.db"
TABLE_NAME = "investor_flow"


CREATE_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
    trade_date TEXT NOT NULL,
    market TEXT NOT NULL,
    stock_code TEXT NOT NULL,
    stock_name TEXT NOT NULL,
    investor_type TEXT NOT NULL,
    buy_amount REAL NOT NULL,
    sell_amount REAL NOT NULL,
    net_amount REAL NOT NULL
)
"""


REQUIRED_COLUMNS = [
    "trade_date",
    "market",
    "stock_code",
    "stock_name",
    "investor_type",
    "buy_amount",
    "sell_amount",
    "net_amount",
]


class InvestorFlowStorage:
    def __init__(self, db_path: Path | str = DB_PATH):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _initialize(self):
        with self._connect() as conn:
            conn.execute(CREATE_TABLE_SQL)
            conn.commit()

    def save_dataframe(self, df: pd.DataFrame, replace: bool = False):
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise ValueError(f"필수 컬럼 누락: {missing}")

        with self._connect() as conn:
            if replace:
                conn.execute(f"DELETE FROM {TABLE_NAME}")

            df[REQUIRED_COLUMNS].to_sql(
                TABLE_NAME,
                conn,
                if_exists="append",
                index=False,
            )
            conn.commit()

    def load_dataframe(self) -> pd.DataFrame:
        with self._connect() as conn:
            query = f"SELECT * FROM {TABLE_NAME}"
            df = pd.read_sql_query(query, conn)

        return df

    def has_data(self) -> bool:
        with self._connect() as conn:
            query = f"SELECT COUNT(*) as cnt FROM {TABLE_NAME}"
            result = pd.read_sql_query(query, conn)

        return int(result.iloc[0]["cnt"]) > 0
