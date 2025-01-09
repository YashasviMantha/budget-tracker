import pandas as pd
from datetime import datetime as dt
import tabula
import numpy as np
import sys

sys.path.append("..")
from utils import logger
import s3cret5

log = logger.get_module_logger(__name__)

MAP_COLUMN = {
        "Unnamed: 0": "Misc",
        "Transaction Details": "Description",
        "Amount ( ` )": "Amount",
        "Unnamed: 1": "Type",
        "Date": "Date",
}

def read_pdf(file_path):
    log.warning(file_path)
    passwords = s3cret5.DOCUMENTS_PDF_PASSWORD_SBI_CARD

    for password in passwords:
        try:
            pages = tabula.read_pdf(file_path, pages="all", stream=True, password=password)
            return pages
        except Exception as e:
            log.warning("could not extraxt text with tabula for SBI Card, trying next password")
            continue

    log.error("could not extraxt text with tabula for SBI Card, might be password issue")

def get_transaction_data_cc(pages):

    df = pages[0]
    df = df.rename(columns=MAP_COLUMN)

    # delete first row
    df = df.iloc[1:]
    # drop misc column
    df.drop(columns=["Misc"], inplace=True)


    # drop values with NaN in Amount, Date and Type columns
    df = df.dropna(subset=["Amount", "Date", "Type"])
    df["Amount"] = df["Amount"].astype(str)
    df["Amount"] = df["Amount"] + df["Type"]

    df["Debit"] = df["Amount"].apply(
        lambda x: (x[:-1].replace(",", "")) if (x.endswith("D")) else 0
    )
    df["Credit"] = df["Amount"].apply(
        lambda x: (x[:-1]).replace(",", "") if (x.endswith("C")) else 0
    )

    df["Debit"] = df["Debit"].astype(float)
    df["Credit"] = df["Credit"].astype(float)

    df.drop(columns=["Amount", "Type"], inplace=True)

    return df

def post_process_data(df):
    df["Date"] = df["Date"].apply(lambda x: dt.strptime(x, "%d %b %y"))

    
    return(df)

def process_sbi_cashback_cc_statement(file_path):
    log.info(f"Processing statement: {file_path}")
    pages = read_pdf(file_path)
    df = get_transaction_data_cc(pages)
    df = post_process_data(df)
    df["Source"] = "SBI Cashback CC"

    df = df[["Date", "Description", "Debit", "Credit", "Source"]]
    log.info(f"Number of transactions: {len(df)}")
    return df
