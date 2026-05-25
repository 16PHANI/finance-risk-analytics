"""
Validation Module
Rule-based data quality checks and anomaly detection.
Author: Boyinapalli Phani Shankar
"""
import pandas as pd

VALIDATION_RULES = {
    'MonthlyCharges': (0, 200),
    'TotalCharges':   (0, 15000),
    'tenure':         (0, 120),
}


def validate(df: pd.DataFrame) -> pd.DataFrame:
    """Apply validation rules and flag anomalies."""
    df['anomaly_flag'] = False
    for col, (lo, hi) in VALIDATION_RULES.items():
        if col in df.columns:
            mask = (df[col] < lo) | (df[col] > hi)
            df.loc[mask, 'anomaly_flag'] = True
    return df


def data_quality_report(df: pd.DataFrame) -> dict:
    """Return data quality summary for documentation and audit."""
    return {
        'total_records':    len(df),
        'null_count':       int(df.isnull().sum().sum()),
        'anomaly_count':    int(df.get('anomaly_flag', pd.Series([False] * len(df))).sum()),
        'completeness_pct': round(100 * (1 - df.isnull().sum().sum() / df.size), 2),
    }


def flag_high_risk(df: pd.DataFrame, col: str = 'churn_proba',
                   threshold: float = 0.5) -> pd.DataFrame:
    """Flag records above risk threshold for business review."""
    if col in df.columns:
        df['high_risk'] = df[col] >= threshold
    return df
