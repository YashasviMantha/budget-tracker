import pandas as pd
from . import logger
import numpy as np
from datetime import datetime as dt

import sys
sys.path.append('../')
import s3cret5

log = logger.get_module_logger(__name__)




def check_df(df):
    columns = df.columns
    flag = True
    if "Date" not in columns:
        log.error("Date column not found")
        flag = False
    if "Description" not in columns:
        log.error("Description column not found")
        flag = False
    if "Debit" not in columns:
        log.error("Debit column not found")
        flag = False
    if "Credit" not in columns:
        log.error("Credit column not found")
        flag = False
    if "Source" not in columns:
        log.error("Source column not found")
        flag = False
    if flag:
        log.info("All columns found")
        
    # Check all the row
    for index, row in df.iterrows():
        if(not isinstance(row['Date'], dt)):
            log.error(f'Date not correctly parsed: {row["Source"]}')
            flag=False
    return flag

def convert_dates_to_str(df):
    log.info('Porcessing Dates')
    df['Date'] = df['Date'].apply(lambda x: x.strftime('%d-%m-%Y'))
    
    return(df)
    
def clean_credit_zeros(df):
    for index, row in df.iterrows():
        amount = row["Credit"]

        if(row['Credit'] == 0):
            df.loc[index, 'Credit'] = np.nan

    return(df)

def clean_credit_cr(df):
    for index, row in df.iterrows():
        amount = row["Credit"]
        if isinstance(amount, str):
            amount = amount.lower().strip()
            if len(amount):
                amount = amount.replace(",", "").replace("cr", "")
                df.loc[index, "Credit"] = float(amount)
            else:
                df.loc[index, "Credit"] = np.NaN
        elif isinstance(amount, float) and amount == 0:
            df.loc[index, "Credit"] = np.NaN

    return df


# def convert_debit_as_float(df):
#     df['Debit'] = df['Debit'].apply(lambda x: x.replace(',', '') if isinstance(x, str) else x)
#     df['Debit'] = pd.to_numeric(df['Debit'])
    
#     return(df)

def make_categories(df):
    
    # create category columns
    for key in s3cret5.KEYWORDS.keys():
        df[key] = np.nan

    # assign category to each transaction
    for index, row in df.iterrows():
        for key, value in s3cret5.KEYWORDS.items():
            for word in value:
                try:
                    if word in row["Description"].lower():
                        df.loc[index, key] = row['Debit']
                        df.loc[index, 'Debit'] = np.nan
                        break
                except AttributeError as e:
                    continue



    return df

def reorder_df(df):
    columns = list(df.columns)
    order_list = [
        "Date",
        "Description",
        "Source",
        "Reward Points",
        "Debit",
        "Credit",
        "Personal",
        "Health",
        "Gift",
        "Travel",
        "Food",
        "Investment",
    ]
    to_del = set(columns) - set(order_list)
    if(to_del):
        log.critical(f"Deleting Columns: {to_del}")
    df = df[order_list]
    return df

def make_credit_as_negative(df):
    df["Credit"] = df["Credit"].apply(lambda x: -x if isinstance(x, float)and x>0 else x)
    return df

def run_all_post_processes(df):
    log.debug('Making Categories')
    df = make_categories(df)
    log.debug('Normalizing Dates')
    df = convert_dates_to_str(df)
    # log.debug("Cleaning credits zeros")
    # df = clean_credit_zeros(df)
    log.debug("Cleaning credits cr")
    df = clean_credit_cr(df).copy()
    log.debug("Making credits negative")
    df = make_credit_as_negative(df)
    log.debug("Reordering  DF")
    df = reorder_df(df)
    # log.debug('Normalizing Debits')
    # df = convert_debit_as_float(df)
    
    return df

