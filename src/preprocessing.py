
import pandas as pd
import numpy as np

# Ulba River Flood Forecasting
# Data preprocessing for LSTM models

def load_data(file_path):
    """Load daily hydrological and satellite data."""
    df = pd.read_csv(file_path)

    print("Dataset shape:", df.shape)
    print("\nColumns:", df.columns.tolist())

    return df


def check_missing_values(df):
    """Check the number of missing values."""
    print("\nMissing values:")
    print(df.isnull().sum())


def check_data(df):
    """Display basic dataset information."""
    print("\nFirst five rows:")
    print(df.head())

    print("\nDataset information:")
    df.info()

    check_missing_values(df)


def prepare_data(df, date_column="date"):
    """Validate dates and sort observations chronologically."""
    df = df.copy()

    if date_column not in df.columns:
        raise ValueError(
            f"Date column '{date_column}' not found. "
            f"Available columns: {df.columns.tolist()}"
        )

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
