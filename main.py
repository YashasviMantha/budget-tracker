from bank_parser import icici, sbi, hdfc_regelia_cc, hdfc_neu_cc
import os
import pandas as pd
from utils import logger, post_process

log = logger.get_module_logger(__name__)


def main(current_path_for_documents):
    log.info(f"Seaching for bank statements: {current_path_for_documents}")
    files_to_parse = os.listdir(current_path_for_documents)
    files_to_parse = [x.lower() for x in files_to_parse]

    final_df = pd.DataFrame(
        columns=["Date", "Description", "Debit", "Credit", "Source", "Reward Points"]
    )
    log.info(f"Found {len(files_to_parse)} files to parse")
    for file in files_to_parse:
        try:
            if "sbi" in file:
                df = sbi.process_sbi_statement(current_path_for_documents + file)
                final_df = pd.concat([final_df, df], ignore_index=True)

            elif "icici" in file:
                log.info(f"Found ICICI statement: {file}")
                df = icici.process_icici_statement(current_path_for_documents + file)
                final_df = pd.concat([final_df, df], ignore_index=True)

            elif "regelia" in file:
                log.info(f"Found HDFC statement: {file}")
                df = hdfc_regelia_cc.process_hdfc_regelia_cc_statement(
                    current_path_for_documents + file
                )
                final_df = pd.concat([final_df, df], ignore_index=True)

            elif "neu" in file:
                log.info(f"Found HDFC - Tata Neu statement: {file}")
                df = hdfc_neu_cc.process_hdfc_neu_cc_statement(
                    current_path_for_documents + file
                )
                final_df = pd.concat([final_df, df], ignore_index=True)

            else:
                log.error(f"{file} - Unknown file type")
        except Exception as e:
            log.error(f"Failed to Process {file} -- Skipping")
    log.debug(f"Final DF: {(len(final_df))}")
    if post_process.check_df(final_df):
        log.debug("Post Process Check passed")
        final_df = post_process.run_all_post_processes(final_df)

    return final_df
