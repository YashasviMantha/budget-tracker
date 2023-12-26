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
        if(row['Credit'] == 0):
            df.loc[index, 'Credit'] = np.nan

    return(df)

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
                if word in row["Description"].lower():
                    df.loc[index, key] = row['Debit']
                    df.loc[index, 'Debit'] = np.nan
                    break

    return df

def run_all_post_processes(df):
    log.debug('Making Categories')
    df = make_categories(df)
    log.debug('Normalizing Dates')
    df = convert_dates_to_str(df)
    log.debug('Cleaning zero credits')
    df = clean_credit_zeros(df)
    # log.debug('Normalizing Debits')
    # df = convert_debit_as_float(df)
    
    return df
