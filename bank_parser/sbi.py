import pandas as pd
import numpy as np
from datetime import datetime as dt
import datetime
import sys

sys.path.append("..")
from utils import logger

log = logger.get_module_logger(__name__)

TABLE_START_TAG = "Txn Date"

MAP_COLUMN = {
    0: "Date",
    1: "Value Date",
    2: "Description",
    3: "Ref No./Cheque No.",
    4: "Debit",
    5: "Credit",
    6: "Balance",
}


def extract_transactions_from_df(df):
    table_start_index = 0
    table_end_index = 0

    for index, row in df.iterrows():
        if row[0] == TABLE_START_TAG:
            table_start_index = index + 1

        if table_start_index != 0 and isinstance(row[0], datetime.datetime):
            table_end_index = index + 1

    df = df[table_start_index:table_end_index].copy()
    df = df.rename(columns=MAP_COLUMN).reset_index(drop=True)

    return df


def post_process(df):
    df["Debit"] = df["Debit"].apply(lambda x: np.nan if x == " " else x)

    return df


def process_sbi_statement(file_path):
    log.info(f"Processing statement: {file_path}")
    df = pd.read_excel(file_path, header=None, engine="openpyxl")
    df = extract_transactions_from_df(df)
    df = post_process(df)
    df["Source"] = "SBI"

    df = df[["Date", "Description", "Debit", "Credit", "Source"]]
    log.info(f"Number of transactions: {len(df)}")
    return df
