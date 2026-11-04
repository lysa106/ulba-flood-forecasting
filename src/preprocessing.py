
import pandas as pd
import numpy as np

def load_data(file_path):
    df = pd.read_csv(file_path)
    print("Dataset shape:", df.shape)
    print("Columns:", df.columns.tolist())
    return df


def check_missing_values(df):
    print("\nMissing values:")
    print(df.isnull().sum())


def check_data(df):
    print("\nFirst five rows:")
    print(df.head())

    print("\nDataset information:")
    df.info()

    check_missing_values(df)


def prepare_data(df, date_column="date"):
    df = df.copy()

    df[date_column] = pd.to_datetime(
        df[date_column], errors="raise"
    )

    if df[date_column].isna().any():
        raise ValueError("Missing dates found.")

    if df[date_column].duplicated().any():
        raise ValueError("Duplicate dates found.")

    df = df.sort_values(date_column).reset_index(drop=True)

    print("\nStart date:", df[date_column].min())
    print("End date:", df[date_column].max())
    print("Total observations:", len(df))

    return df
