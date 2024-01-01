import pandas as pd
import sys
from datetime import datetime as dt
import numpy as np

sys.path.append("..")

from utils import logger

log = logger.get_module_logger(__name__)

TABLE_START_TAG = "S No."
MAP_COLUMN = {
    "Unnamed: 0": "Placeholder 0",
    "Unnamed: 1": "S No.",
    "Unnamed: 2": "Date",
    "Unnamed: 3": "Value Date",
    "Unnamed: 4": "Placeholder 4",
    "Unnamed: 5": "Description",
    "Unnamed: 6": "Debit",
    "Unnamed: 7": "Credit",
    "Unnamed: 8": "Balance",
}


def extract_transactions_from_df(df):
    table_start_index = 0
    table_end_index = 0

    for index, row in df.iterrows():
        if row["Unnamed: 1"] == TABLE_START_TAG:
            table_start_index = index + 1

        if table_start_index != 0:
            if not isinstance(row["Unnamed: 1"], float):
                if row["Unnamed: 1"].isnumeric():
                    table_end_index = index + 1

    df = df[table_start_index:table_end_index].copy()
    df = df.rename(columns=MAP_COLUMN).reset_index(drop=True)

    return df


def post_process(df):
    # parse date:
    df = df.dropna(subset=["Date"])
    df["Date"] = df["Date"].apply(lambda x: dt.strptime(x, "%d,%m,%Y"))

    # remove zeros from credit and make them float
    df["Credit"] = pd.to_numeric(df["Credit"])
    df["Credit"] = df["Credit"].apply(lambda x: np.nan if x == "0.0" else x)

    df["Debit"] = pd.to_numeric(df["Debit"])
    df["Debit"] = df["Debit"].apply(lambda x: np.nan if x == "0.0" else x)

    return df


def process_icici_statement(file_path):
    log.info(f"Processing statement: {file_path}")
    df = pd.read_excel(file_path)
    df = extract_transactions_from_df(df)
    df = post_process(df)
    df["Source"] = "ICICI"

    df = df[["Date", "Description", "Debit", "Credit", "Source"]]
    log.info(f"Number of transactions: {len(df)}")

    return df
