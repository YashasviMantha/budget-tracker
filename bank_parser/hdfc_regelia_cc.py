import tabula
import pandas as pd
import sys
from datetime import datetime as dt

sys.path.append("..")
from utils import logger
import s3cret5

log = logger.get_module_logger(__name__)


MAP_COLUMN = {
    "Unnamed: 0": "Date",
    "Unnamed: 1": "Description",
    "Unnamed: 2": "Reward Points",
    "Unnamed: 3": "amount",
}


def read_pdf(file_path):
    passwords = s3cret5.DOCUMENTS_PDF_PASSWORD_REGELIA
    for password in passwords:
        try:
            pages = tabula.read_pdf(file_path, pages="all", stream=True, password=password)
            return pages
        except Exception as e:
            log.warning(f"could not extraxt text with tabula for Regelia, trying next password")
            continue

    log.error("could not extraxt text with tabula for Regelia, might be password issue")


def get_transaction_data_cc(pages):
    df = pd.DataFrame()
    for page in pages[2:-2]:
        df = df.append(page[5:])

    df = df.reset_index(drop=True)
    df = df.rename(columns=MAP_COLUMN)

    df["Debit"] = df["amount"].apply(lambda x: x if (not x.endswith("Cr")) else 0)
    df["Credit"] = df["amount"].apply(lambda x: x if (x.endswith("Cr")) else 0)
    df = df.drop(columns=["Domestic Transactions"])
    return df

def post_process_data(df):
    # parse date correctly
    df["Date"] = df["Date"].apply(lambda x: dt.strptime(x.split(" ")[0], "%d/%m/%Y"))
    
    df['Debit'] = df['Debit'].apply(lambda x: x.replace(",", '') if isinstance(x, str) else x)
    df['Debit'] = pd.to_numeric(df['Debit'])
    # print(df['Debit'].value_counts())
    
    return(df)

def process_hdfc_regelia_cc_statement(file_path):
    log.info(f"Processing statement: {file_path}")
    pages = read_pdf(file_path)
    df = get_transaction_data_cc(pages)
    df = post_process_data(df)
    df["Source"] = "HDFC Regelia CC"

    df = df[["Date", "Description", "Debit", "Credit", "Source", "Reward Points"]]
    log.info(f"Number of transactions: {len(df)}")
    return df
