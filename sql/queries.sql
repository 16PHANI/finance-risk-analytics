-- Finance Risk Analytics: SQL Queries
-- Dataset: 7,043 customer records
-- Author: Boyinapalli Phani Shankar

-- Q1: Overall risk rate
SELECT COUNT(*) AS total_customers,
       SUM(CASE WHEN churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
       ROUND(100.0 * SUM(CASE WHEN churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct
FROM customers;

-- Q2: High-risk cohort (short-tenure, month-to-month)
SELECT contract, tenure,
       COUNT(*) AS customers,
       ROUND(100.0*SUM(CASE WHEN churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct
FROM customers
WHERE contract='Month-to-month' AND tenure<=3
GROUP BY contract, tenure ORDER BY churn_rate_pct DESC;

-- Q3: Churn rate by contract type
SELECT contract, COUNT(*) AS total,
       ROUND(100.0*SUM(CASE WHEN churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct
FROM customers GROUP BY contract ORDER BY churn_rate_pct DESC;

-- Q4: Churn rate by tenure band
SELECT CASE WHEN tenure BETWEEN 0 AND 3 THEN '0-3 mo'
            WHEN tenure BETWEEN 4 AND 12 THEN '4-12 mo'
            WHEN tenure BETWEEN 13 AND 24 THEN '13-24 mo'
            ELSE '25+ mo' END AS tenure_band,
       COUNT(*) AS total,
       ROUND(100.0*SUM(CASE WHEN churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct
FROM customers GROUP BY tenure_band ORDER BY churn_rate_pct DESC;

-- Q5: Churn rate by payment method
SELECT payment_method, COUNT(*) AS total,
       ROUND(100.0*SUM(CASE WHEN churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct
FROM customers GROUP BY payment_method ORDER BY churn_rate_pct DESC;

-- Q6: Revenue at risk by contract type
SELECT contract,
       ROUND(SUM(CASE WHEN churn='Yes' THEN monthly_charges ELSE 0 END),2) AS revenue_at_risk,
       ROUND(100.0*SUM(CASE WHEN churn='Yes' THEN monthly_charges ELSE 0 END)/SUM(monthly_charges),2) AS risk_pct
FROM customers GROUP BY contract ORDER BY revenue_at_risk DESC;

-- Q7: Avg charges by churn status
SELECT churn, ROUND(AVG(monthly_charges),2) AS avg_monthly,
       ROUND(AVG(tenure),2) AS avg_tenure FROM customers GROUP BY churn;

-- Q8: Internet service vs churn
SELECT internet_service, COUNT(*) AS total,
       ROUND(100.0*SUM(CASE WHEN churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct
FROM customers GROUP BY internet_service ORDER BY churn_rate_pct DESC;

-- Q9: Data quality validation check
SELECT SUM(CASE WHEN total_charges IS NULL THEN 1 ELSE 0 END) AS null_charges,
       SUM(CASE WHEN monthly_charges<=0 THEN 1 ELSE 0 END) AS invalid_charges,
       SUM(CASE WHEN tenure<0 THEN 1 ELSE 0 END) AS invalid_tenure,
       COUNT(*) AS total_records FROM customers;

-- Q10: Service bundle impact on churn
SELECT tech_support, online_security, COUNT(*) AS total,
       ROUND(100.0*SUM(CASE WHEN churn='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS churn_rate_pct
FROM customers WHERE internet_service!='No'
GROUP BY tech_support, online_security ORDER BY churn_rate_pct DESC;

-- Q11: High-risk segment for regulatory reporting
SELECT 'High Risk Segment' AS label, COUNT(*) AS count,
       ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM customers),2) AS pct_of_total,
       ROUND(SUM(monthly_charges),2) AS monthly_revenue_at_risk
FROM customers WHERE contract='Month-to-month' AND tenure<=3 AND churn='Yes';
