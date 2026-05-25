# Finance Risk Analytics: Data Extraction, Validation & Reporting

**Dataset:** 7,043 records | **Language:** Python | **Author:** Boyinapalli Phani Shankar

---

## Results

| Model | ROC-AUC | Weighted F1 | Accuracy |
|---|---|---|---|
| Logistic Regression | ~0.84 | ~0.79 | ~0.78 |
| Random Forest | ~0.85 | ~0.80 | ~0.80 |
| **XGBoost** | **~0.87** | **~0.81** | **~0.81** |

**Key finding:** 38% of high-risk customers were on short-tenure contracts — the single highest-impact intervention target.

---

## What This Project Covers

| Stage | Detail |
|---|---|
| **Data Extraction** | SQL queries (11): cohort risk rates, contract type, payment method, revenue at risk, data quality checks |
| **Transformation** | Coerced types, imputed missing values, tenure/charge bands, service-count feature, ordinal encoding |
| **Validation** | Rule-based anomaly detection, data quality checks, policy compliance flags |
| **Modelling** | Logistic Regression vs Random Forest vs XGBoost with stratified split and 5-fold CV |
| **Reporting** | 11 visualisations + Power BI dashboard for regulatory reporting and stakeholder governance |

---

## Project Structure

```
finance-risk-analytics/
├── notebooks/
│   └── analytics_pipeline.ipynb   # full pipeline: extraction → modelling → reporting
├── src/
│   ├── extract.py                  # SQL data extraction and transformation
│   ├── validate.py                 # validation rules and anomaly detection
│   └── model.py                   # XGBoost training and evaluation
├── sql/
│   └── queries.sql                 # 11 SQL queries for cohort analysis
├── data/                           # dataset (not committed — see setup)
├── outputs/figures/                # 11 generated visualisations
├── requirements.txt
└── README.md
```

---

## Setup

```bash
git clone https://github.com/16PHANI/finance-risk-analytics.git
cd finance-risk-analytics
pip install -r requirements.txt
jupyter notebook notebooks/analytics_pipeline.ipynb
```

Dataset: [Kaggle Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
Place at `data/Telco-Customer-Churn.csv` before running.

---

## Tech Stack

`Python` · `Pandas` · `NumPy` · `SQL (PostgreSQL)` · `scikit-learn` · `XGBoost` · `Matplotlib` · `Seaborn` · `Power BI`

---

## Author

**Boyinapalli Phani Shankar**  
[GitHub](https://github.com/16PHANI) · [LinkedIn](https://linkedin.com/in/phanishankar16)
