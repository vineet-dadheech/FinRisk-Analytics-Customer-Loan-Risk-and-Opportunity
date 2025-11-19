import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Set a random seed for reproducibility
np.random.seed(42)

# --- Configuration ---
N_CUSTOMERS = 500
START_DATE = datetime(2025, 5, 16) # 6 months ago from 'today'
END_DATE = datetime(2025, 11, 16)   # 'Today'

# --- Lists for random choices ---
REGIONS = ['North', 'South', 'East', 'West']
GENDERS = ['Male', 'Female']
TRANSACTION_TYPES = ['Deposit', 'Withdrawal', 'Payment', 'Transfer', 'Received']
PAYMENT_MODES = ['UPI', 'Credit Card', 'Debit Card', 'Net Banking']

# ==============================================================================
# 1. GENERATE `account_holders` TABLE
# ==============================================================================
print("Generating `account_holders` table...")

def create_customer_profiles(n):
    """
    Creates distinct customer profiles to ensure data has realistic segments
    (e.g., high risk, prime customers, new customers).
    """
    data = []
    
    # We will create 4 distinct profiles
    n_profile_1 = int(n * 0.10) # 10% - High Risk (Defaulted)
    n_profile_2 = int(n * 0.30) # 30% - Good (Paid Off)
    n_profile_3 = int(n * 0.35) # 35% - Prime Prospect (No Loan, High Wealth)
    n_profile_4 = n - n_profile_1 - n_profile_2 - n_profile_3 # 25% - New/Avg Prospect (No Loan)
    
    account_id_counter = 1001

    # Profile 1: High Risk (Defaulted)
    for _ in range(n_profile_1):
        has_fd = np.random.choice([True, False], p=[0.1, 0.9])
        data.append({
            'account_id': f'ACC{account_id_counter}',
            'profile': 'High-Risk',
            'loan_status': 'Defaulted',
            'cibil_score': np.random.randint(300, 680),
            'current_balance': np.random.randint(500, 15000),
            'has_fd': has_fd,
            'total_fd_amount': np.random.randint(5000, 20000) if has_fd else 0,
            'has_credit_card': np.random.choice([True, False], p=[0.5, 0.5]),
            'age': np.random.randint(28, 55),
            'account_open_date': pd.to_datetime(END_DATE) - timedelta(days=np.random.randint(730, 2000))
        })
        account_id_counter += 1

    # Profile 2: Good Customer (Paid Off)
    for _ in range(n_profile_2):
        has_fd = np.random.choice([True, False], p=[0.6, 0.4])
        data.append({
            'account_id': f'ACC{account_id_counter}',
            'profile': 'Good-Customer',
            'loan_status': 'Paid Off',
            'cibil_score': np.random.randint(680, 850),
            'current_balance': np.random.randint(15000, 150000),
            'has_fd': has_fd,
            'total_fd_amount': np.random.randint(50000, 300000) if has_fd else 0,
            'has_credit_card': np.random.choice([True, False], p=[0.8, 0.2]),
            'age': np.random.randint(30, 65),
            'account_open_date': pd.to_datetime(END_DATE) - timedelta(days=np.random.randint(1095, 3650))
        })
        account_id_counter += 1
        
    # Profile 3: Prime Prospect (No Loan, High Wealth)
    for _ in range(n_profile_3):
        has_fd = np.random.choice([True, False], p=[0.7, 0.3])
        # Includes the "big FDs" request
        fd_amount = np.random.choice([np.random.randint(100000, 500000), np.random.randint(500001, 2000000)], p=[0.8, 0.2])
        data.append({
            'account_id': f'ACC{account_id_counter}',
            'profile': 'Prime-Prospect',
            'loan_status': 'No Loan',
            'cibil_score': np.random.randint(750, 900),
            'current_balance': np.random.randint(50000, 300000),
            'has_fd': has_fd,
            'total_fd_amount': fd_amount if has_fd else 0,
            'has_credit_card': np.random.choice([True, False], p=[0.6, 0.4]),
            'age': np.random.randint(35, 70),
            'account_open_date': pd.to_datetime(END_DATE) - timedelta(days=np.random.randint(1825, 4000))
        })
        account_id_counter += 1
        
    # Profile 4: New/Average Prospect (No Loan)
    for _ in range(n_profile_4):
        has_fd = np.random.choice([True, False], p=[0.2, 0.8])
        data.append({
            'account_id': f'ACC{account_id_counter}',
            'profile': 'New-Prospect',
            'loan_status': 'No Loan',
            'cibil_score': np.random.randint(600, 750),
            'current_balance': np.random.randint(2000, 40000),
            'has_fd': has_fd,
            'total_fd_amount': np.random.randint(10000, 50000) if has_fd else 0,
            'has_credit_card': np.random.choice([True, False], p=[0.7, 0.3]),
            'age': np.random.randint(22, 35),
            'account_open_date': pd.to_datetime(END_DATE) - timedelta(days=np.random.randint(365, 1095))
        })
        account_id_counter += 1

    df = pd.DataFrame(data)
    
    # Add remaining generic columns
    df['region'] = np.random.choice(REGIONS, size=n)
    df['gender'] = np.random.choice(GENDERS, size=n, p=[0.55, 0.45])
    
    # Reorder and remove profile helper column
    cols = ['account_id', 'region', 'age', 'gender', 'current_balance', 'has_fd', 
            'total_fd_amount', 'has_credit_card', 'cibil_score', 'account_open_date', 
            'loan_status', 'profile'] # Keep profile for transaction generation
    return df[cols]

account_holders = create_customer_profiles(N_CUSTOMERS)

# ==============================================================================
# 2. GENERATE `transactions` TABLE
# ==============================================================================
print("Generating `transactions` table (this may take a moment)...")

all_transactions = []
transaction_id_counter = 100001

# Base day range for 6 months
total_days = (END_DATE - START_DATE).days

for _, row in account_holders.iterrows():
    account_id = row['account_id']
    profile = row['profile']
    
    # Define transaction behavior based on profile
    if profile == 'High-Risk':
        num_transactions = np.random.randint(20, 50)
        type_weights = [0.2, 0.35, 0.35, 0.1] # Low Deposit, High Withdrawal/Payment
        mode_weights = [0.4, 0.1, 0.4, 0.1]  # High UPI/Debit, Low CC/Net
        amount_range_in = (500, 2000)
        amount_range_out = (100, 1500)
        
    elif profile == 'Good-Customer':
        num_transactions = np.random.randint(30, 60)
        type_weights = [0.3, 0.2, 0.3, 0.2]  # Balanced
        mode_weights = [0.3, 0.3, 0.2, 0.2]  # Balanced, good CC use
        amount_range_in = (1000, 15000) # Salary deposits
        amount_range_out = (100, 3000)
        
    elif profile == 'Prime-Prospect':
        num_transactions = np.random.randint(15, 40)
        type_weights = [0.4, 0.1, 0.2, 0.3]  # High Deposit/Received, High Transfer (to FDs)
        mode_weights = [0.2, 0.2, 0.2, 0.4]  # High Net Banking for big transfers
        amount_range_in = (5000, 50000) # Big inflows
        amount_range_out = (500, 10000) # Big transfers
        
    else: # New-Prospect
        num_transactions = np.random.randint(50, 100) # Very active
        type_weights = [0.25, 0.25, 0.3, 0.2] # Lots of small payments
        mode_weights = [0.6, 0.2, 0.2, 0.0]   # Extremely High UPI
        amount_range_in = (100, 1000)
        amount_range_out = (10, 500) # Lots of small txns

    # Generate this customer's transactions
    for _ in range(num_transactions):
        # Choose type (Inflow vs Outflow)
        trans_type = np.random.choice(['Deposit', 'Withdrawal', 'Payment', 'Received', 'Transfer'], 
                                      p=[type_weights[0]/2, type_weights[1], type_weights[2], type_weights[0]/2, type_weights[3]]) # Split Deposit/Received
        
        if trans_type in ['Deposit', 'Received']:
            amount = np.random.randint(*amount_range_in)
        else:
            amount = np.random.randint(*amount_range_out)
        
        # Add the requested "big payments"
        if trans_type == 'Payment' and np.random.rand() < 0.03: # 3% chance of a big payment
            amount = np.random.randint(10000, 50000) 
            
        all_transactions.append({
            'transaction_id': f'TXN{transaction_id_counter}',
            'account_id': account_id,
            'transaction_date': START_DATE + timedelta(days=np.random.randint(0, total_days)),
            'transaction_type': trans_type,
            'transaction_amount': round(amount, 2),
            'payment_mode': np.random.choice(PAYMENT_MODES, p=mode_weights)
        })
        transaction_id_counter += 1

transactions = pd.DataFrame(all_transactions)
# Sort by date for realism
transactions = transactions.sort_values(by=['account_id', 'transaction_date']).reset_index(drop=True)

# Clean up the account_holders table by dropping the helper 'profile' column
account_holders = account_holders.drop(columns=['profile'])

# ==============================================================================
# 3. SAVE TO CSV
# ==============================================================================
print(f"\nSaving `account_holders.csv`... ({len(account_holders)} rows)")
account_holders.to_csv('account_holders.csv', index=False)

print(f"Saving `transactions.csv`... ({len(transactions)} rows)")
transactions.to_csv('transactions.csv', index=False)

print("\n--- Generation Complete! ---")
print("\n`account_holders.csv` sample:")
print(account_holders.head())
print(f"\n{account_holders.info()}")

print("\n`transactions.csv` sample:")
print(transactions.head())
print(f"\n{transactions.info()}")