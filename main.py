import parser
import os
import pandas as pd

current_path_for_documents = "./documents/"


def main():
    files_to_parse = os.listdir(current_path_for_documents)

    final_df = pd.DataFrame()

    for file in files_to_parse:
        if "sbi" in file:
            df = parser.process_sbi_statement(current_path_for_documents + file)
            final_df = final_df.append(df)
        elif "icici" in file:
            df = parser.process_icici_statement(current_path_for_documents + file)
            final_df = final_df.append(df)

        elif "hdfc" in file:
            df = parser.process_hdfc_statement(current_path_for_documents + file)
            final_df = final_df.append(df)

        else:
            print("Unknown file type")
