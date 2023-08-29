import tabula
import pandas as pd

MAP_COLUMN = {
    "Unnamed: 0": "date",
    "Unnamed: 1": "description",
    "Unnamed: 2": "reward_points",
    "Unnamed: 3": "amount",
}


def read_pdf(file_path):
    pages = tabula.read_pdf(file_path, pages="all", stream=True)
    return pages


def get_transaction_data_cc(pages):
    df = pd.DataFrame()
    for page in pages[2:-2]:
        df = df.append(page[5:])

    df = df.reset_index(drop=True)
    df = df.rename(
        columns={
            "Unnamed: 0": "date",
            "Unnamed: 1": "description",
            "Unnamed: 2": "reward_points",
            "Unnamed: 3": "amount",
        }
    )

    df["debit"] = df["amount"].apply(lambda x: x if (not x.endswith("Cr")) else 0)
    df["credit"] = df["amount"].apply(lambda x: x if (x.endswith("Cr")) else 0)
    df = df.drop(columns=["Domestic Transactions"])
    return df
