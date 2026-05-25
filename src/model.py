"""
Modelling Module
XGBoost risk segmentation with AUC / F1 evaluation.
Author: Boyinapalli Phani Shankar
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb


def prepare_features(df: pd.DataFrame, target: str = 'Churn'):
    """Encode categoricals, binarise target, return X and y."""
    df = df.copy()
    drop_extra = [c for c in ['tenure_band', 'charge_band'] if c in df.columns]
    for col in df.select_dtypes(include='object').columns:
        if col != target:
            df[col] = LabelEncoder().fit_transform(df[col].astype(str))
    df[target] = (df[target] == 'Yes').astype(int)
    X = df.drop(columns=[target] + drop_extra)
    y = df[target]
    return X, y


def train_all(X, y: pd.Series) -> dict:
    """Train LR, RF, XGBoost; return metrics for each."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest':       RandomForestClassifier(n_estimators=200, random_state=42),
        'XGBoost':             xgb.XGBClassifier(
                                   n_estimators=200, max_depth=5,
                                   use_label_encoder=False,
                                   eval_metric='logloss',
                                   random_state=42),
    }
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        proba = model.predict_proba(X_test)[:, 1]
        preds = model.predict(X_test)
        results[name] = {
            'model':    model,
            'auc':      round(roc_auc_score(y_test, proba), 3),
            'f1':       round(f1_score(y_test, preds, average='weighted'), 3),
            'accuracy': round(accuracy_score(y_test, preds), 3),
            'proba':    proba,
            'y_test':   y_test,
        }
    return results
