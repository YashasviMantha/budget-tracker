import pandas as pd

KEYWORDS = {
    "FOOD": ["food", "swiggy"],
    "TRAVEL": ["cab", "ride"],
}


def check_df(df):
    columns = df.columns
    assert "date" in columns, "date column not found"
    assert "description" in columns, "description column not found"
    assert "reward_points" in columns, "reward_points column not found"
    assert "debit" in columns, "debit column not found"
    assert "credit" in columns, "credit column not found"
