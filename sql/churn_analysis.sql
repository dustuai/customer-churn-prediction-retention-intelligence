CREATE DATABASE customer_churn;

use customer_churn;

CREATE TABLE telco_churn (
    customerID VARCHAR(50) PRIMARY KEY,
    gender VARCHAR(10),
    SeniorCitizen INT,
    Partner VARCHAR(5),
    Dependents VARCHAR(5),
    tenure INT,
    PhoneService VARCHAR(5),
    MultipleLines VARCHAR(25),
    InternetService VARCHAR(25),
    OnlineSecurity VARCHAR(25),
    OnlineBackup VARCHAR(25),
    DeviceProtection VARCHAR(25),
    TechSupport VARCHAR(25),
    StreamingTV VARCHAR(25),
    StreamingMovies VARCHAR(25),
    Contract VARCHAR(25),
    PaperlessBilling VARCHAR(5),
    PaymentMethod VARCHAR(50),
    MonthlyCharges DECIMAL(10, 2),
    TotalCharges DECIMAL(10, 2),
    Churn INT
);



SHOW GLOBAL VARIABLES LIKE 'local_infile';
SET GLOBAL local_infile = ON;


LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/telco_churn_clean.csv'
INTO TABLE telco_churn
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(
    customerID,
    gender,
    SeniorCitizen,
    Partner,
    Dependents,
    tenure,
    PhoneService,
    MultipleLines,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport,
    StreamingTV,
    StreamingMovies,
    Contract,
    PaperlessBilling,
    PaymentMethod,
    MonthlyCharges,
    @TotalCharges,
    Churn
)
SET TotalCharges = NULLIF(TRIM(@TotalCharges), '');





/*LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/telco_churn_clean.csv'
INTO TABLE telco_churn
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;*/



SELECT COUNT(*) AS total_customers,
       SUM(Churn) AS churned_customers,
       ROUND(100.0 * AVG(Churn), 2) AS churn_rate_pct
FROM telco_churn;



SELECT Contract, COUNT(*) AS customers, SUM(Churn) AS churned_customers,
       ROUND(100.0 * AVG(Churn), 2) AS churn_rate_pct
FROM telco_churn
GROUP BY Contract
ORDER BY churn_rate_pct DESC;



SELECT InternetService, COUNT(*) AS customers,
       ROUND(100.0 * AVG(Churn), 2) AS churn_rate_pct
FROM telco_churn
GROUP BY InternetService
ORDER BY churn_rate_pct DESC;



SELECT PaymentMethod, COUNT(*) AS customers,
       ROUND(100.0 * AVG(Churn), 2) AS churn_rate_pct
FROM telco_churn
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;



SELECT CASE
         WHEN tenure <= 12 THEN '0-12'
         WHEN tenure <= 24 THEN '13-24'
         WHEN tenure <= 48 THEN '25-48'
         ELSE '49+'
       END AS tenure_group,
       COUNT(*) AS customers,
       ROUND(100.0 * AVG(Churn), 2) AS churn_rate_pct
FROM telco_churn
GROUP BY tenure_group
ORDER BY churn_rate_pct DESC;



SELECT customerID, tenure, Contract, MonthlyCharges, TotalCharges
FROM telco_churn
WHERE Churn = 1
ORDER BY MonthlyCharges DESC
LIMIT 25;
