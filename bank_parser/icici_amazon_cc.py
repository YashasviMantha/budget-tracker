import tabula
import pandas as pd
import sys
from datetime import datetime as dt

sys.path.append("..")
from utils import logger
import s3cret5

log = logger.get_module_logger(__name__)

MAP_COLUMN = {
    "STATEMENT SUMMARY": "Description",
    "Unnamed: 4": "Reward Points",
    "Unnamed: 6": "Amount",
}


def read_pdf(file_path):
    pages = tabula.read_pdf(
        file_path,
        pages="all",
        stream=True,
        password=s3cret5.DOCUMENTS_PDF_PASSWORD_ICICI_AMAZON,
    )
    return pages


def get_transaction_data_cc(pages):
    df = pages[1]
    df = (
        df[
            [
                "STATEMENT SUMMARY",
                "Unnamed: 4",
                "Unnamed: 6",
            ]
        ][14:]
        .rename(columns=MAP_COLUMN)
        .reset_index(drop=True)
    )
    return df


def post_process_data(df):
    df["Date"] = df["Description"].apply(
        lambda x: dt.strptime(x.split(" ")[0], "%d/%m/%Y")
    )

    df["Debit"] = df["Amount"].apply(
        lambda x: "-" + x.replace(" CR", "") if ("CR" in x) else x
    )
    df["Debit"] = pd.to_numeric(df["Debit"].apply(lambda x: x.replace(",", "")))
    


def process_icici_amazon_statement(file_path):
    log.info(f"Processing statement: {file_path}")
    pages = read_pdf(file_path)
    df = get_transaction_data_cc(pages)
    df = post_process_data(df)
    df["Source"] = "ICICI Amazon CC"

    df = df[["Date", "Description", "Debit", "Credit", "Source", "Reward Points"]]
    log.info(f"Number of transactions: {len(df)}")
    return df
