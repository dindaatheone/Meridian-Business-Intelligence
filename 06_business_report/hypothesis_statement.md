# Hypothesis Statement - Meridian Business Intelligence

## Business Problem

Private banks generate relationship intelligence continuously
through client transactions, portfolio rebalancing events,
fee accruals, and inflow and outflow patterns. Most institutions
cannot capture this intelligence systematically. The result
is AUM attrition that could have been detected weeks before
formal exit, concentration risk that accumulates invisibly
until a major client departure creates a revenue shock, and
CLV that is systematically underestimated because fee revenue
is tracked but relationship depth is not.

Meridian Business Intelligence is built to close that gap.
This report documents what the 24-month synthetic data
universe reveals about the health of a private banking book
when interrogated at institutional depth.

---

## The Four Hypotheses

### H1 - AUM Concentration Risk is Elevated

The top 10% of clients hold more than 40% of total AUM.

This threshold matters because at 40% concentration, a single
large client exit creates a revenue shock that the remaining
book cannot absorb without a meaningful decline in total fee
income. Private banks at this concentration level are running
an implicit key-man risk on their largest relationships.

Confirmation means: RM accountability for top-decile clients
must be elevated to senior level. Relationship review frequency
must increase. Succession planning for each top-decile
relationship must be documented.

Rejection means: the book is well-diversified and concentration
risk management resources can be allocated to other priorities.

---

### H2 - Churn Signals are Detectable Before Formal Exit

Clients who exit the relationship show detectable inflow
cessation patterns more than 180 days before formal exit.

This matters because if the signal exists in the transaction
data, it can be acted on. A client who stops making inflows
is not yet churned. They are at risk. The intervention window
is between first inflow cessation and formal exit. If that
window is 180 days or longer, Meridian has time to act.

Confirmation means: implement a systematic churn signal
monitoring query running weekly against the transactions
table. Route flagged clients to RM for relationship review
within five business days of the 180-day threshold being hit.

Rejection means: churn in this book is abrupt and signal-free.
Prevention focus shifts from early detection to onboarding
quality and product-market fit at relationship initiation.

---

### H3 - CLV Varies Significantly by Jurisdiction and Tier

UHNW clients from China and Singapore generate
disproportionately higher lifetime fee revenue than
clients from other corridors at equivalent tier.

This matters for RM resource allocation. If CLV is
significantly higher in the China and Singapore corridors,
senior RM time should be weighted toward those relationships.
If CLV is surprisingly high in Brunei despite low client
count, the Brunei corridor is underinvested relative to
its revenue contribution per client.

Confirmation means: restructure RM assignments to weight
senior capacity toward highest CLV corridors. Adjust
onboarding investment accordingly.

Rejection means: CLV is corridor-neutral and RM allocation
should be driven by AUM size and relationship complexity
rather than geographic origin.

---

### H4 - Credit Risk is Unevenly Distributed

A meaningful subset of active clients carry DTI above 0.50,
creating concentrated credit exposure in the lending book.

This matters because private banking credit facilities,
particularly Lombard loans secured against portfolio assets,
carry correlated risk during market drawdowns. A client with
DTI above 0.50 who also holds a Lombard loan against an
equity portfolio faces simultaneous income pressure and
collateral value decline during a risk-off event.

Confirmation means: implement enhanced monitoring for
clients in credit risk tiers C and D. Restrict new credit
facility extensions for tier D clients. Require quarterly
review of existing facilities for tier C clients.

Rejection means: the credit book is conservatively
structured and credit risk monitoring resources can be
maintained at current levels.