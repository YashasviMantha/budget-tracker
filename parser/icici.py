# Scrip to read icici statement

import pandas as pd

TABLE_START_TAG = "S No."
MAP_COLUMN = {
    "Unnamed: 0": "Placeholder 0",
    "Unnamed: 1": "S No.",
    "Unnamed: 2": "Txn Date",
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

        if table_start_index != 0 and row["Unnamed: 1"].isnumeric():
            table_end_index = index + 1

    df = df[table_start_index:table_end_index].copy()
    df = df.rename(columns=MAP_COLUMN).reset_index(drop=True)

    return df


def process_icici_statement(file_path):
    df = pd.read_excel(file_path, header=None)
    df = extract_transactions_from_df(df)
    return df
