"""
Data Extraction Module
SQL-based data extraction and transformation.
Author: Boyinapalli Phani Shankar
"""
import pandas as pd


def load_csv(path: str) -> pd.DataFrame:
    """Load dataset from CSV path."""
    return pd.read_csv(path)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transformation rules:
    - Coerce TotalCharges to numeric (impute 11 missing with median)
    - Drop customerID (non-predictive identifier)
    - Create tenure bands, charge bands, service-count feature
    - Contract ordinal encoding
    """
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
    df['TotalCharges'].fillna(df['TotalCharges'].median(), inplace=True)
    df.drop(columns=['customerID'], inplace=True, errors='ignore')

    df['tenure_band'] = pd.cut(
        df['tenure'],
        bins=[-1, 3, 12, 24, 48, 999],
        labels=['0-3 mo', '4-12 mo', '13-24 mo', '25-48 mo', '49+ mo']
    )

    df['charge_band'] = pd.cut(
        df['MonthlyCharges'],
        bins=[0, 35, 65, 95, 999],
        labels=['Low', 'Medium', 'High', 'Very High']
    )

    service_cols = [
        'PhoneService', 'MultipleLines', 'InternetService',
        'OnlineSecurity', 'OnlineBackup', 'DeviceProtection',
        'TechSupport', 'StreamingTV', 'StreamingMovies'
    ]
    df['service_count'] = df[service_cols].apply(
        lambda row: sum(
            v not in ['No', 'No internet service', 'No phone service']
            for v in row
        ), axis=1
    )

    df['contract_ordinal'] = df['Contract'].map(
        {'Month-to-month': 0, 'One year': 1, 'Two year': 2}
    )
    return df
