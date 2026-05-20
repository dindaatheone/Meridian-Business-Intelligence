# Meridian Business Intelligence
# Synthetic Data Generator
# Generates clients, portfolios, and transactions CSVs
# aligned with schema.sql constraints
#
# Output: 01_raw_data/clients.csv
#         01_raw_data/portfolios.csv
#         01_raw_data/transactions.csv

import numpy as np
import pandas as pd
from faker import Faker
import random
from datetime import date, timedelta
import os

fake = Faker()
np.random.seed(42)
random.seed(42)

OUTPUT_DIR = "01_raw_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Configuration ─────────────────────────────────────────────
N_CLIENTS      = 200
START_DATE     = date(2018, 1, 1)
END_DATE       = date(2025, 12, 31)

# Corridor weights: CN 40 / SG 25 / ID 20 / MO 10 / BN 5
JURISDICTIONS  = ['China', 'Singapore', 'Indonesia', 'Macau', 'Brunei']
JURIS_WEIGHTS  = [0.40, 0.25, 0.20, 0.10, 0.05]

CURRENCY_MAP   = {
    'China':     'CNY',
    'Singapore': 'SGD',
    'Indonesia': 'IDR',
    'Macau':     'USD',
    'Brunei':    'BND',
}

# AUM ranges by tier (USD)
TIER_CONFIG = {
    'HNW':  {'aum_range': (1_000_000,   5_000_000),  'weight': 0.50},
    'VHNW': {'aum_range': (5_000_000,  30_000_000),  'weight': 0.35},
    'UHNW': {'aum_range': (30_000_000, 200_000_000), 'weight': 0.15},
}

MANDATES       = ['Discretionary', 'Advisory', 'Execution-Only']
MANDATE_W      = [0.45, 0.40, 0.15]

RISK_APPETITES = ['Conservative', 'Moderate', 'Aggressive']
RISK_W         = [0.35, 0.45, 0.20]

RM_POOL = [
    'James Tan', 'Priya Menon', 'Wei Zhang', 'Sofia Lim',
    'Ahmad Rizal', 'Chen Jing', 'David Ng', 'Mei Lin',
    'Rajan Pillai', 'Isabella Cruz'
]

ASSET_CLASSES  = [
    'Equities', 'Fixed Income', 'Alternatives',
    'Cash', 'Structured Products', 'Private Credit'
]

TXN_TYPES      = ['Inflow', 'Outflow', 'Fee', 'Dividend',
                  'Interest', 'Rebalance', 'FX-Conversion']
TXN_WEIGHTS    = [0.25, 0.15, 0.20, 0.15, 0.10, 0.10, 0.05]

FEE_TYPES      = ['Management Fee', 'Performance Fee',
                  'Advisory Fee', 'Transaction Fee']

def random_date(start, end):
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))

def random_alloc():
    """Generate portfolio allocation that sums to 100."""
    weights = np.random.dirichlet(np.ones(6) * 2)
    weights = np.round(weights * 100, 2)
    weights[-1] = round(100 - weights[:-1].sum(), 2)
    return weights

# ── Generate Clients ──────────────────────────────────────────
print("Generating clients...")
clients = []
for i in range(1, N_CLIENTS + 1):
    jurisdiction = random.choices(JURISDICTIONS, weights=JURIS_WEIGHTS)[0]
    tier         = random.choices(
                       list(TIER_CONFIG.keys()),
                       weights=[v['weight'] for v in TIER_CONFIG.values()]
                   )[0]
    aum_min, aum_max = TIER_CONFIG[tier]['aum_range']
    aum          = round(random.uniform(aum_min, aum_max), 2)
    mandate      = random.choices(MANDATES, weights=MANDATE_W)[0]
    risk         = random.choices(RISK_APPETITES, weights=RISK_W)[0]
    onboarding   = random_date(START_DATE, END_DATE)
    dob          = date(
                       random.randint(1950, 1985),
                       random.randint(1, 12),
                       random.randint(1, 28)
                   )
    tenure       = (END_DATE - onboarding).days // 30
    is_active    = random.random() > 0.08
    exit_dt      = None if is_active else random_date(onboarding, END_DATE)
    co_inv       = tier in ['VHNW', 'UHNW'] and random.random() > 0.40
    shariah      = jurisdiction in ['Indonesia', 'Brunei'] and random.random() > 0.60
    last_reb     = random_date(onboarding, END_DATE) if random.random() > 0.20 else None

    clients.append({
        'client_id':                   i,
        'full_name':                   fake.name(),
        'jurisdiction':                jurisdiction,
        'date_of_birth':               dob,
        'onboarding_date':             onboarding,
        'client_tier':                 tier,
        'investable_aum_usd':          aum,
        'primary_currency':            CURRENCY_MAP[jurisdiction],
        'product_mandate_type':        mandate,
        'risk_appetite':               risk,
        'shariah_compliant_flag':      shariah,
        'relationship_tenure_months':  tenure,
        'assigned_rm':                 random.choice(RM_POOL),
        'co_investment_eligible_flag': co_inv,
        'last_rebalancing_date':       last_reb,
        'annual_income_usd':           round(aum * random.uniform(0.04, 0.12), 2),
        'total_debt_usd':              round(aum * random.uniform(0.0, 0.30), 2),
        'is_active':                   is_active,
        'exit_date':                   exit_dt,
    })

clients_df = pd.DataFrame(clients)
clients_df.to_csv(f"{OUTPUT_DIR}/clients.csv", index=False)
print(f"  {len(clients_df)} clients generated.")

# ── Generate Portfolios ───────────────────────────────────────
print("Generating portfolios...")
portfolios = []
portfolio_id = 1
for _, client in clients_df.iterrows():
    n_ports = 1 if client['client_tier'] == 'HNW' else random.randint(1, 3)
    total_aum = client['investable_aum_usd']
    aum_splits = np.random.dirichlet(np.ones(n_ports))

    for j in range(n_ports):
        alloc    = random_alloc()
        port_aum = round(total_aum * aum_splits[j], 2)
        perf_ytd = round(random.gauss(0.06, 0.12), 4)
        perf_inc = round(random.gauss(0.08, 0.15), 4)
        inception = random_date(
            pd.Timestamp(client['onboarding_date']).date(),
            END_DATE
        )

        benchmarks = {
            'Discretionary':  'MSCI AC Asia Pacific',
            'Advisory':       'MSCI AC Asia Pacific',
            'Execution-Only': 'Cash + 1.5%',
        }

        portfolios.append({
            'portfolio_id':          portfolio_id,
            'client_id':             client['client_id'],
            'portfolio_name':        f"{client['full_name'].split()[0]} {['Core', 'Growth', 'Income', 'Tactical'][j % 4]}",
            'inception_date':        inception,
            'base_currency':         'USD',
            'mandate_type':          client['product_mandate_type'],
            'aum_usd':               port_aum,
            'equity_pct':            alloc[0],
            'fixed_income_pct':      alloc[1],
            'alternatives_pct':      alloc[2],
            'cash_pct':              alloc[3],
            'structured_pct':        alloc[4],
            'private_credit_pct':    alloc[5],
            'benchmark':             benchmarks[client['product_mandate_type']],
            'performance_ytd':       perf_ytd,
            'performance_inception': perf_inc,
            'last_valuation_date':   END_DATE,
        })
        portfolio_id += 1

portfolios_df = pd.DataFrame(portfolios)
portfolios_df.to_csv(f"{OUTPUT_DIR}/portfolios.csv", index=False)
print(f"  {len(portfolios_df)} portfolios generated.")

# ── Generate Transactions ─────────────────────────────────────
print("Generating transactions...")
transactions = []
txn_id = 1

for _, port in portfolios_df.iterrows():
    client   = clients_df[clients_df['client_id'] == port['client_id']].iloc[0]
    n_txns   = random.randint(12, 60)
    port_start = pd.Timestamp(port['inception_date']).date()

    for _ in range(n_txns):
        txn_date = random_date(port_start, END_DATE)
        txn_type = random.choices(TXN_TYPES, weights=TXN_WEIGHTS)[0]
        asset    = random.choice(ASSET_CLASSES)

        if txn_type == 'Inflow':
            amount = round(random.uniform(50_000, port['aum_usd'] * 0.10), 2)
        elif txn_type == 'Outflow':
            amount = -round(random.uniform(50_000, port['aum_usd'] * 0.08), 2)
        elif txn_type == 'Fee':
            amount = -round(port['aum_usd'] * random.uniform(0.0005, 0.002), 2)
        elif txn_type in ['Dividend', 'Interest']:
            amount = round(port['aum_usd'] * random.uniform(0.001, 0.005), 2)
        else:
            amount = round(random.uniform(-100_000, 100_000), 2)

        fee_amt  = None
        fee_type = None
        if txn_type == 'Fee':
            fee_type = random.choice(FEE_TYPES)
            fee_amt  = abs(amount)

        fx_map = {'CNY': 7.24, 'SGD': 1.34, 'IDR': 15800.0, 'USD': 1.0, 'BND': 1.34}
        orig_ccy = client['primary_currency']
        fx_rate  = round(fx_map.get(orig_ccy, 1.0) * random.uniform(0.97, 1.03), 6)

        transactions.append({
            'transaction_id':     txn_id,
            'client_id':          port['client_id'],
            'portfolio_id':       port['portfolio_id'],
            'transaction_date':   txn_date,
            'transaction_type':   txn_type,
            'amount_usd':         amount,
            'original_currency':  orig_ccy,
            'fx_rate_applied':    fx_rate,
            'asset_class':        asset,
            'fee_amount_usd':     fee_amt,
            'fee_type':           fee_type,
            'rm_id':              client['assigned_rm'],
            'notes':              None,
        })
        txn_id += 1

transactions_df = pd.DataFrame(transactions)
transactions_df.to_csv(f"{OUTPUT_DIR}/transactions.csv", index=False)
print(f"  {len(transactions_df)} transactions generated.")

print(f"\nAll data saved to {OUTPUT_DIR}/")
print(f"  clients.csv:      {len(clients_df)} rows")
print(f"  portfolios.csv:   {len(portfolios_df)} rows")
print(f"  transactions.csv: {len(transactions_df)} rows")
