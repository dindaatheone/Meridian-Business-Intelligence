# Client Tiers - Meridian Private Bank

## Tier Definitions

| Tier | AUM Range (USD) | Mandate Access | RM Model |
|---|---|---|---|
| HNW | USD 1M to 5M | Advisory primary | Dedicated RM |
| VHNW | USD 5M to 30M | Discretionary and Advisory | Dedicated RM plus Specialist |
| UHNW | USD 30M and above | Full product access | Senior RM plus Team |

## Product Access by Tier

| Product | HNW | VHNW | UHNW |
|---|---|---|---|
| Advisory Mandate | Yes | Yes | Yes |
| Discretionary Mandate | No | Yes | Yes |
| Structured Products | Limited | Yes | Yes |
| Private Credit | No | Yes | Yes |
| PE Co-Investment | No | Yes | Yes |
| Real Estate Advisory | No | Yes | Yes |
| Succession Structuring | No | Limited | Yes |
| Shariah-Compliant Sleeve | Yes | Yes | Yes |

## Special Client Flags

### Shariah-Compliant Flag

Boolean field in the client entity schema. Activates Islamic finance
structuring across all mandates for eligible clients. Applies
primarily to clients from Brunei and Indonesia. This flag is
consistent across all three Meridian repos: BI, Monte Carlo,
and Ventures. A client flagged here carries that flag into
co-investment allocation and risk modeling.

### Co-Investment Eligibility Flag

Boolean field in the client entity schema. Activated at VHNW
and UHNW tiers. Triggers access to Meridian Ventures deal flow.
Every venture exit for an eligible client converts into an AUM
growth event for the wealth management side. This is the
integration mechanism between the Ventures repo and this repo.

## Client Profile by Corridor

| Corridor | Typical Tier | Primary Need | Special Flag |
|---|---|---|---|
| China | VHNW to UHNW | Cross-border structuring, succession planning | None |
| Singapore | HNW to UHNW | Portfolio management, family office services | None |
| Indonesia | HNW to VHNW | Succession, Islamic finance structuring | Shariah |
| Macau | VHNW to UHNW | Discretionary management, holding restructuring | None |
| Brunei | UHNW | Full succession, Islamic finance, legacy planning | Shariah |

## Six Core Private Banking KPIs

These six metrics drive every SQL query and Python model in this repo.
They are what a private bank board monitors, not academic constructs.

| KPI | Formula | What It Signals |
|---|---|---|
| AUM Growth Rate | (AUM_end - AUM_start) / AUM_start x 100 | Whether the institution is growing or contracting its revenue base |
| Concentration Risk | Top 10% client AUM / Total AUM | Revenue fragility - above 40% is elevated risk |
| Client Lifetime Value | Avg annual fee revenue x expected tenure years | True economic value of each client relationship |
| Churn Rate | Clients lost / clients at start x 100 | Silent attrition detectable in transaction patterns before formal exit |
| DTI Ratio | Total debt / gross annual income | Client credit risk - above 0.50 signals stress |
| DTC Ratio | Total debt / total investable assets | Leverage risk - above 0.50 is critical threshold |

## AUM per RM Benchmark

Private banking RM productivity is measured by AUM per relationship
manager. Industry benchmark for boutique Asia-Pacific manage