# 02 - Database

PostgreSQL relational architecture for Meridian Business Intelligence.
Three tables. One spine. Every analytical layer in this repo draws
from this schema.

---

## Files

| File | Purpose |
|---|---|
| schema.sql | CREATE TABLE statements with constraints, data types, foreign keys |
| seed.sql | COPY statements loading synthetic CSVs into PostgreSQL |
| ERD.png | Entity relationship diagram - three tables, crow's foot notation |

---

## Relational Logic

One client holds one or more portfolios.
One portfolio generates many transactions over 24 months.
This chain is the backbone of every JOIN query in 03_sql_analysis.

client_id is the universal key. It appears in all three tables
and is the join condition that connects client attributes to
portfolio performance to transaction behavior.

---

## Design Decisions

**Monetary values in USD**
All amounts stored in USD for cross-corridor consistency.
Original currency and FX rate stored separately to enable
FX exposure analysis by corridor and currency pair.

**CHECK constraints at database level**
Valid values for jurisdiction, client_tier, transaction_type,
asset_class, and fee_type are enforced by the database itself.
Bad data cannot enter the system through the seed loader.

**Shariah and co-investment flags on clients table**
Both Boolean flags sit on the clients table and are referenced
by downstream repos. A client flagged here carries that flag
into Monte Carlo risk modeling and Ventures co-investment
allocation without any data transformation.

**Private credit as a distinct asset class**
Private credit is separated from alternatives to reflect
Meridian's product architecture accurately. It carries
different risk, liquidity, and fee characteristics.

---

## Setup

```bash

