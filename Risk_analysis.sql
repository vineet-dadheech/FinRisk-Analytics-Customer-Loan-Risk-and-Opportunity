use Financial_transaction;
select * from transactions;
select * from account_holders;

-- 1. How do the average financial metrics (CIBIL Score, Current Balance, and FD Savings) compare between customers who Defaulted vs. those who Paid Off?
SELECT 
    loan_status,
    COUNT(account_id) AS total_customers,
    ROUND(AVG(cibil_score), 0) AS avg_cibil_score,
    ROUND(AVG(current_balance), 2) AS avg_current_balance,
    ROUND(AVG(total_fd_amount), 2) AS avg_fd_savings,
    CONCAT(ROUND(SUM(CASE WHEN has_credit_card = 'True' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1), '%') AS credit_card_ownership_rate
FROM 
    account_holders
WHERE 
    loan_status IN ('Defaulted', 'Paid Off')
GROUP BY 
    loan_status;


-- 2. Which customers have a negative net cash flow (Outflow > Inflow) over the last 6 months, and what is their loan status?
WITH CashFlow AS (
    SELECT 
        a.account_id,
        a.loan_status,
        SUM(CASE WHEN t.transaction_type IN ('Deposit', 'Received') THEN t.transaction_amount ELSE 0 END) AS total_inflow,
        SUM(CASE WHEN t.transaction_type IN ('Withdrawal', 'Payment', 'Transfer') THEN t.transaction_amount ELSE 0 END) AS total_outflow
    FROM 
        account_holders a
    JOIN 
        transactions t ON a.account_id = t.account_id
    GROUP BY 
        a.account_id, a.loan_status
)
SELECT 
    loan_status,
    COUNT(account_id) AS total_customers,
    COUNT(CASE WHEN total_outflow > total_inflow THEN 1 END) AS cash_negative_customers,
    CONCAT(ROUND(COUNT(CASE WHEN total_outflow > total_inflow THEN 1 END) * 100.0 / COUNT(*), 1), '%') AS '%_of_cash_negative_customers'
FROM 
    CashFlow
GROUP BY 
    loan_status
ORDER BY 
   '%_of_cash_negative_customers' DESC;


-- 3. Which region has the highest default rate, and is it correlated with lower average account balances in that region?
SELECT 
    region,
    COUNT(account_id) AS total_customers,
    SUM(CASE WHEN loan_status = 'Defaulted' THEN 1 ELSE 0 END) AS total_defaults,
    CONCAT(ROUND(SUM(CASE WHEN loan_status = 'Defaulted' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2), '%') AS default_rate,
    ROUND(AVG(current_balance), 2) AS avg_regional_balance
FROM 
    account_holders
WHERE 
    loan_status != 'No Loan'
GROUP BY 
    region
ORDER BY 
    default_rate DESC;

-- 4. How many 'No Loan' customers have a High CIBIL (>750) and substantial savings (Total Wealth > 50,000), making them prime candidates for premium loans?
SELECT 
    account_id,
    age,
    cibil_score,
    (current_balance + total_fd_amount) AS total_wealth,
    region
FROM 
    account_holders
WHERE 
    loan_status = 'No Loan' 
    AND cibil_score >= 750 
    AND (current_balance + total_fd_amount) > 50000
ORDER BY 
    total_wealth DESC

-- 5. Do defaulted customers rely more heavily on Credit Cards vs. Debit/UPI compared to customers who paid off their loans?
SELECT 
    a.loan_status,
    t.payment_mode,
    COUNT(t.transaction_id) AS transaction_count,
    ROUND(SUM(t.transaction_amount), 2) AS total_spend_volume
FROM 
    account_holders a
JOIN 
    transactions t ON a.account_id = t.account_id
WHERE 
    a.loan_status IN ('Defaulted', 'Paid Off') 
    AND t.transaction_type IN ('Payment', 'Transfer') -- Only look at spending
GROUP BY 
    a.loan_status, t.payment_mode
ORDER BY 
    a.loan_status, transaction_count DESC;

-- 6. Group customers by age buckets (18-30, 31-50, 50+) and determine which age group has the highest penetration of Fixed Deposits (FDs).
   SELECT
    COUNT(account_id) as total_customers,
    CASE
        WHEN age BETWEEN 18 AND 30 THEN '18-30'
        WHEN age BETWEEN 31 AND 50 THEN '31-50'
        ELSE '50+'
    END AS age_group,
    SUM(total_fd_amount) as groups_total_fd_amount
   FROM account_holders
   GROUP BY 
        CASE
            WHEN age BETWEEN 18 AND 30 THEN '18-30'
            WHEN age BETWEEN 31 AND 50 THEN '31-50'
            ELSE '50+'
        END

-- 7. Does having a FD effects a customers loan status?
Select
    COUNT(account_id),
    loan_status,
    has_fd
FROM account_holders
WHERE loan_status IN ('Defaulted', 'Paid Off')
GROUP BY loan_status,has_fd

-- 8. People who has a FD and defaulted what was their Cibil Score, net cash flow 
-- so if we target people who haven't applied for loans but have FD as new leads we eliminate the risky ones.

SELECT
  a.account_id,
  a.cibil_score,
  a.current_balance,
  COALESCE(SUM(CASE WHEN t.transaction_type IN ('Deposit','Received') THEN t.transaction_amount ELSE 0 END), 0)
    - COALESCE(SUM(CASE WHEN t.transaction_type IN ('Withdrawal','Payment','Transfer') THEN t.transaction_amount ELSE 0 END), 0)
    AS net_cashflow
FROM dbo.account_holders a
LEFT JOIN dbo.transactions t
  ON t.account_id = a.account_id
WHERE a.has_fd = 1
  AND a.loan_status = 'Defaulted'
GROUP BY
  a.account_id,
  a.cibil_score,
  a.current_balance;

