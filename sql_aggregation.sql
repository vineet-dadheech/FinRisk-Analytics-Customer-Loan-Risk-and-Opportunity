CREATE OR ALTER VIEW dbo.AccountFeatures
AS
WITH TransactionSummary AS (
    SELECT
        account_id,
        COUNT(transaction_id) AS total_transactions,
        AVG(transaction_amount) AS avg_transaction_amount,
        SUM(CASE WHEN transaction_type IN ('Deposit', 'Received') THEN transaction_amount ELSE 0 END) AS total_inflow,
        SUM(CASE WHEN transaction_type IN ('Withdrawal', 'Payment', 'Transfer') THEN transaction_amount ELSE 0 END) AS total_outflow,
        COUNT(CASE WHEN payment_mode = 'Credit Card' THEN 1 END) AS credit_card_transactions,
        COUNT(CASE WHEN payment_mode = 'UPI' THEN 1 END) AS upi_transactions,
        COUNT(CASE WHEN transaction_type = 'Withdrawal' THEN 1 END) AS withdrawal_count,
        COUNT(CASE WHEN transaction_type = 'Deposit' THEN 1 END) AS deposit_count
    FROM dbo.transactions
    GROUP BY account_id
)
SELECT
    a.account_id,
    a.region,
    a.age,
    a.gender,
    a.current_balance,
    a.has_fd,
    a.total_fd_amount,
    a.has_credit_card,
    a.cibil_score,
    a.account_open_date,
    a.loan_status,
    COALESCE(t.total_transactions, 0) AS total_transactions,
    COALESCE(t.total_inflow, 0) AS total_inflow,
    COALESCE(t.total_outflow, 0) AS total_outflow,
    (COALESCE(t.total_inflow, 0) - COALESCE(t.total_outflow, 0)) AS net_cash_flow,
    CASE WHEN COALESCE(t.total_inflow, 0) > 0 THEN COALESCE(t.total_outflow, 0) / t.total_inflow ELSE 0 END AS burn_rate,
    COALESCE(t.credit_card_transactions, 0) AS credit_card_transactions,
    COALESCE(t.upi_transactions, 0) AS upi_transactions,
    COALESCE(t.withdrawal_count, 0) AS withdrawal_count,
    COALESCE(t.deposit_count, 0) AS deposit_count
FROM dbo.account_holders a
LEFT JOIN TransactionSummary t
    ON a.account_id = t.account_id;
