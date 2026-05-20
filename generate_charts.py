# Meridian Business Intelligence
# Dashboard Chart Generator
# Three-page dashboard: Executive Overview, Client Analytics,
# Transaction Intelligence
#
# Input:  03_sql_analysis/outputs/
# Output: 05_visualization/outputs/
#         page_1_executive_overview.png
#         page_2_client_analytics.png
#         page_3_transaction_intelligence.png

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import numpy as np
import os

os.makedirs("05_visualization/outputs", exist_ok=True)

NAVY     = '#1E3A5F'
GOLD     = '#B8962E'
CREAM    = '#F5F0E8'
RED      = '#B71C1C'
GREEN    = '#2E7D32'
AMBER    = '#F9A825'
GREY     = '#9E9E9E'
DARKGREY = '#424242'

def fmt_usd(val):
    if val >= 1_000_000_000:
        return f"${val/1_000_000_000:.1f}B"
    elif val >= 1_000_000:
        return f"${val/1_000_000:.1f}M"
    elif val >= 1_000:
        return f"${val/1_000:.0f}K"
    return f"${val:.0f}"

BASE = "03_sql_analysis/outputs"

tier_dist    = pd.read_csv(f"{BASE}/01_exploratory/client_count_by_tier.csv")
juris_dist   = pd.read_csv(f"{BASE}/01_exploratory/client_count_by_jurisdiction.csv")
active_dist  = pd.read_csv(f"{BASE}/01_exploratory/active_vs_inactive.csv")
shariah_j    = pd.read_csv(f"{BASE}/01_exploratory/shariah_by_jurisdiction.csv")

corridor     = pd.read_csv(f"{BASE}/02_joins_and_aggregations/corridor_flow.csv")
rm_prod      = pd.read_csv(f"{BASE}/02_joins_and_aggregations/rm_productivity.csv")
fx_exp       = pd.read_csv(f"{BASE}/02_joins_and_aggregations/fx_exposure.csv")
mandate_dist = pd.read_csv(f"{BASE}/02_joins_and_aggregations/mandate_distribution.csv")

monthly      = pd.read_csv(f"{BASE}/03_cte_window_functions/monthly_flows.csv")
ranking      = pd.read_csv(f"{BASE}/03_cte_window_functions/client_aum_ranking.csv")
decile       = pd.read_csv(f"{BASE}/03_cte_window_functions/aum_decile_distribution.csv")

conc_risk    = pd.read_csv(f"{BASE}/04_business_metrics/concentration_risk.csv")
churn        = pd.read_csv(f"{BASE}/04_business_metrics/churn_detection.csv")
fee_decomp   = pd.read_csv(f"{BASE}/04_business_metrics/fee_revenue_decomposition.csv")

clients_raw  = pd.read_csv("01_raw_data/clients.csv")

monthly['month_dt'] = pd.to_datetime(monthly['month'].astype(str))
monthly_sorted = monthly.sort_values('month_dt').reset_index(drop=True)
monthly_sorted['rolling_3m'] = monthly_sorted['net_flow'].rolling(3, min_periods=1).mean()

print("Meridian Business Intelligence - Dashboard Chart Generator")

# PAGE 1 - EXECUTIVE OVERVIEW
print("Generating Page 1: Executive Overview...")

fig = plt.figure(figsize=(20, 14), facecolor=CREAM)
fig.suptitle(
    "MERIDIAN PRIVATE BANK  |  Executive Overview Dashboard",
    fontsize=16, fontweight='bold', color=NAVY, y=0.98
)
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

ax0 = fig.add_subplot(gs[0, 0])
ax0.set_facecolor(NAVY)
total_aum = corridor['total_aum_usd'].sum()
active_count = int(active_dist[active_dist['is_active'] == True]['client_count'].values[0])
ax0.text(0.5, 0.65, fmt_usd(total_aum), ha='center', va='center',
         fontsize=28, fontweight='bold', color=GOLD, transform=ax0.transAxes)
ax0.text(0.5, 0.35, "Total Book AUM", ha='center', va='center',
         fontsize=11, color=CREAM, transform=ax0.transAxes)
ax0.text(0.5, 0.15, f"{active_count} Active Clients", ha='center', va='center',
         fontsize=9, color=GREY, transform=ax0.transAxes)
ax0.axis('off')
ax0.set_title("Book AUM", color=NAVY, fontsize=10, pad=8)

ax1 = fig.add_subplot(gs[0, 1])
conc_pct = float(conc_risk['top_10pct_concentration'].values[0])
gauge_color = RED if conc_pct > 40 else AMBER if conc_pct > 30 else GREEN
label = "ELEVATED" if conc_pct > 40 else "MONITOR" if conc_pct > 30 else "ACCEPTABLE"
theta = np.linspace(0, np.pi, 100)
ax1.plot(np.cos(theta), np.sin(theta), color=GREY, linewidth=8, alpha=0.3)
fill_theta = np.linspace(0, np.pi * min(conc_pct / 100, 1.0), 100)
ax1.plot(np.cos(fill_theta), np.sin(fill_theta), color=gauge_color, linewidth=8)
ax1.text(0, 0.3, f"{conc_pct:.1f}%", ha='center', va='center',
         fontsize=18, fontweight='bold', color=gauge_color)
ax1.text(0, 0.05, label, ha='center', va='center',
         fontsize=10, fontweight='bold', color=gauge_color)
ax1.text(0, -0.2, "Top 10% Client Concentration", ha='center', va='center',
         fontsize=8, color=DARKGREY)
ax1.set_xlim(-1.3, 1.3)
ax1.set_ylim(-0.5, 1.3)
ax1.axis('off')
ax1.set_facecolor(CREAM)
ax1.set_title("Concentration Risk", color=NAVY, fontsize=10, pad=8)

ax2 = fig.add_subplot(gs[0, 2])
tier_aum = mandate_dist.groupby('client_tier')['total_aum_usd'].sum().reset_index()
tier_order = ['UHNW', 'VHNW', 'HNW']
tier_aum = tier_aum[tier_aum['client_tier'].isin(tier_order)].copy()
tier_aum['client_tier'] = pd.Categorical(tier_aum['client_tier'], categories=tier_order, ordered=True)
tier_aum = tier_aum.sort_values('client_tier')
bars = ax2.barh(tier_aum['client_tier'], tier_aum['total_aum_usd'],
                color=[GOLD, NAVY, GREY], edgecolor='none', height=0.5)
for bar, val in zip(bars, tier_aum['total_aum_usd']):
    ax2.text(bar.get_width() * 1.02, bar.get_y() + bar.get_height() / 2,
             fmt_usd(val), va='center', fontsize=9, color=DARKGREY)
ax2.set_facecolor(CREAM)
ax2.spines[['top', 'right', 'left']].set_visible(False)
ax2.xaxis.set_visible(False)
ax2.set_title("AUM by Client Tier", color=NAVY, fontsize=10, pad=8)
ax2.tick_params(axis='y', colors=NAVY)

ax3 = fig.add_subplot(gs[1, :2])
cum_aum = monthly_sorted['net_flow'].cumsum()
x = range(len(cum_aum))
ax3.fill_between(x, cum_aum, alpha=0.15, color=NAVY)
ax3.plot(x, cum_aum, color=NAVY, linewidth=2.5)
ax3.axhline(0, color=GREY, linewidth=0.8, linestyle='--')
tick_step = max(1, len(monthly_sorted) // 8)
ax3.set_xticks(list(range(0, len(monthly_sorted), tick_step)))
ax3.set_xticklabels(
    [str(m)[:7] for m in monthly_sorted['month_dt'].iloc[::tick_step]],
    rotation=30, ha='right', fontsize=8
)
ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: fmt_usd(v)))
ax3.set_facecolor(CREAM)
ax3.spines[['top', 'right']].set_visible(False)
ax3.set_title("Cumulative AUM Growth Trend", color=NAVY, fontsize=10, pad=8)
ax3.tick_params(colors=DARKGREY)

ax4 = fig.add_subplot(gs[1, 2])
rm_top = rm_prod.head(8).sort_values('total_aum_usd')
bar_colors = [GOLD if v >= 200_000_000 else NAVY for v in rm_top['total_aum_usd']]
ax4.barh(rm_top['assigned_rm'], rm_top['total_aum_usd'],
         color=bar_colors, edgecolor='none', height=0.6)
ax4.axvline(200_000_000, color=GOLD, linewidth=1.5, linestyle='--', alpha=0.7, label='$200M benchmark')
ax4.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: fmt_usd(v)))
ax4.set_facecolor(CREAM)
ax4.spines[['top', 'right']].set_visible(False)
ax4.set_title("RM Productivity (AUM)", color=NAVY, fontsize=10, pad=8)
ax4.tick_params(axis='y', labelsize=7, colors=DARKGREY)
ax4.tick_params(axis='x', labelsize=7)
ax4.legend(fontsize=7)

plt.savefig("05_visualization/outputs/page_1_executive_overview.png",
            dpi=150, bbox_inches='tight', facecolor=CREAM)
plt.close()
print("  Page 1 saved.")

# PAGE 2 - CLIENT ANALYTICS
print("Generating Page 2: Client Analytics...")

fig = plt.figure(figsize=(20, 14), facecolor=CREAM)
fig.suptitle(
    "MERIDIAN PRIVATE BANK  |  Client Analytics Dashboard",
    fontsize=16, fontweight='bold', color=NAVY, y=0.98
)
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

ax0 = fig.add_subplot(gs[0, 0])
corr_sorted = corridor.sort_values('total_aum_usd', ascending=True)
j_colors = [GOLD if j == 'China' else NAVY for j in corr_sorted['jurisdiction']]
ax0.barh(corr_sorted['jurisdiction'], corr_sorted['total_aum_usd'],
         color=j_colors, edgecolor='none', height=0.5)
for i, val in enumerate(corr_sorted['total_aum_usd']):
    ax0.text(val * 1.02, i, fmt_usd(val), va='center', fontsize=8, color=DARKGREY)
ax0.set_facecolor(CREAM)
ax0.spines[['top', 'right', 'left']].set_visible(False)
ax0.xaxis.set_visible(False)
ax0.set_title("AUM by Corridor", color=NAVY, fontsize=10, pad=8)
ax0.tick_params(axis='y', colors=NAVY)

ax1 = fig.add_subplot(gs[0, 1])
risk_dist = clients_raw['risk_appetite'].value_counts()
pie_colors = [NAVY, GOLD, RED][:len(risk_dist)]
wedges, texts, autotexts = ax1.pie(
    risk_dist.values, labels=risk_dist.index, colors=pie_colors,
    autopct='%1.1f%%', startangle=90,
    wedgeprops={'edgecolor': CREAM, 'linewidth': 2}
)
for t in texts:
    t.set_color(DARKGREY)
    t.set_fontsize(9)
for at in autotexts:
    at.set_color('white')
    at.set_fontsize(9)
    at.set_fontweight('bold')
ax1.set_facecolor(CREAM)
ax1.set_title("Risk Profile Distribution", color=NAVY, fontsize=10, pad=8)

ax2 = fig.add_subplot(gs[0, 2])
shariah_focus = shariah_j[shariah_j['jurisdiction'].isin(['Indonesia', 'Brunei', 'Macau'])].copy()
x = np.arange(len(shariah_focus))
w = 0.35
ax2.bar(x - w/2, shariah_focus['total_clients'], w, label='Total', color=NAVY, edgecolor='none')
ax2.bar(x + w/2, shariah_focus['shariah_clients'], w, label='Shariah', color=GOLD, edgecolor='none')
ax2.set_xticks(x)
ax2.set_xticklabels(shariah_focus['jurisdiction'], fontsize=9)
ax2.set_facecolor(CREAM)
ax2.spines[['top', 'right']].set_visible(False)
ax2.legend(fontsize=8)
ax2.set_title("Shariah Clients by Corridor", color=NAVY, fontsize=10, pad=8)
ax2.tick_params(colors=DARKGREY)

ax3 = fig.add_subplot(gs[1, :2])
top10 = ranking[ranking['rank_overall'] <= 10].sort_values('total_aum')
bar_colors_top = [GOLD if t == 'UHNW' else NAVY if t == 'VHNW' else GREY
                  for t in top10['client_tier']]
ax3.barh(top10['full_name'], top10['total_aum'],
         color=bar_colors_top, edgecolor='none', height=0.6)
for i, (val, tier) in enumerate(zip(top10['total_aum'], top10['client_tier'])):
    ax3.text(val * 1.01, i, f"{fmt_usd(val)} | {tier}",
             va='center', fontsize=8, color=DARKGREY)
ax3.set_facecolor(CREAM)
ax3.spines[['top', 'right', 'left']].set_visible(False)
ax3.xaxis.set_visible(False)
ax3.set_title("Top 10 Clients by AUM", color=NAVY, fontsize=10, pad=8)
ax3.tick_params(axis='y', labelsize=8, colors=DARKGREY)
ax3.legend(handles=[
    mpatches.Patch(color=GOLD, label='UHNW'),
    mpatches.Patch(color=NAVY, label='VHNW'),
    mpatches.Patch(color=GREY, label='HNW'),
], fontsize=8, loc='lower right')

ax4 = fig.add_subplot(gs[1, 2])
dec_colors = [RED if d == 1 else GOLD if d <= 3 else NAVY for d in decile['decile']]
ax4.bar(decile['decile'], decile['pct_of_total_aum'],
        color=dec_colors, edgecolor=CREAM, linewidth=0.5)
ax4.set_xlabel("Decile (1 = Top)", fontsize=8, color=DARKGREY)
ax4.set_ylabel("% of Total AUM", fontsize=8, color=DARKGREY)
ax4.set_facecolor(CREAM)
ax4.spines[['top', 'right']].set_visible(False)
ax4.set_title("AUM Concentration by Decile", color=NAVY, fontsize=10, pad=8)
ax4.tick_params(colors=DARKGREY)
ax4.set_xticks(decile['decile'])

plt.savefig("05_visualization/outputs/page_2_client_analytics.png",
            dpi=150, bbox_inches='tight', facecolor=CREAM)
plt.close()
print("  Page 2 saved.")

# PAGE 3 - TRANSACTION INTELLIGENCE
print("Generating Page 3: Transaction Intelligence...")

fig = plt.figure(figsize=(20, 14), facecolor=CREAM)
fig.suptitle(
    "MERIDIAN PRIVATE BANK  |  Transaction Intelligence Dashboard",
    fontsize=16, fontweight='bold', color=NAVY, y=0.98
)
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

ax0 = fig.add_subplot(gs[0, :2])
x = np.arange(len(monthly_sorted))
w = 0.35
ax0.bar(x - w/2, monthly_sorted['inflows'], w, label='Inflows', color=GREEN, alpha=0.8, edgecolor='none')
ax0.bar(x + w/2, monthly_sorted['outflows'], w, label='Outflows', color=RED, alpha=0.8, edgecolor='none')
ax0.plot(x, monthly_sorted['rolling_3m'], color=GOLD, linewidth=2, label='3M Rolling Net Flow', zorder=5)
tick_step = max(1, len(monthly_sorted) // 10)
ax0.set_xticks(x[::tick_step])
ax0.set_xticklabels(
    monthly_sorted['month_dt'].dt.strftime('%Y-%m').iloc[::tick_step],
    rotation=30, ha='right', fontsize=8
)
ax0.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: fmt_usd(v)))
ax0.set_facecolor(CREAM)
ax0.spines[['top', 'right']].set_visible(False)
ax0.legend(fontsize=8)
ax0.set_title("Monthly Inflow vs Outflow", color=NAVY, fontsize=10, pad=8)
ax0.tick_params(colors=DARKGREY)

ax1 = fig.add_subplot(gs[0, 2])
fee_sorted = fee_decomp.sort_values('total_fee_revenue', ascending=True)
fee_colors = [GOLD, NAVY, GREY, RED][:len(fee_sorted)]
ax1.barh(fee_sorted['fee_type'], fee_sorted['total_fee_revenue'],
         color=fee_colors, edgecolor='none', height=0.5)
for i, (val, pct) in enumerate(zip(fee_sorted['total_fee_revenue'], fee_sorted['pct_of_total_fees'])):
    ax1.text(val * 1.02, i, f"{fmt_usd(val)} ({pct:.1f}%)",
             va='center', fontsize=8, color=DARKGREY)
ax1.set_facecolor(CREAM)
ax1.spines[['top', 'right', 'left']].set_visible(False)
ax1.xaxis.set_visible(False)
ax1.set_title("Fee Revenue by Type", color=NAVY, fontsize=10, pad=8)
ax1.tick_params(axis='y', labelsize=8, colors=DARKGREY)

ax2 = fig.add_subplot(gs[1, 0])
corr_flow = corridor.sort_values('net_flow')
flow_colors = [GREEN if v >= 0 else RED for v in corr_flow['net_flow']]
ax2.barh(corr_flow['jurisdiction'], corr_flow['net_flow'],
         color=flow_colors, edgecolor='none', height=0.5)
ax2.axvline(0, color=DARKGREY, linewidth=0.8)
ax2.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: fmt_usd(v)))
ax2.set_facecolor(CREAM)
ax2.spines[['top', 'right']].set_visible(False)
ax2.set_title("Net Flow by Corridor", color=NAVY, fontsize=10, pad=8)
ax2.tick_params(colors=DARKGREY, labelsize=9)

ax3 = fig.add_subplot(gs[1, 1])
fx_sorted = fx_exp[fx_exp['original_currency'] != 'USD'].sort_values('total_volume_usd', ascending=True)
fx_colors = [RED if c in ['CNY', 'IDR'] else NAVY for c in fx_sorted['original_currency']]
ax3.barh(fx_sorted['original_currency'], fx_sorted['total_volume_usd'],
         color=fx_colors, edgecolor='none', height=0.5)
for i, (val, pct) in enumerate(zip(fx_sorted['total_volume_usd'], fx_sorted['pct_of_total'])):
    ax3.text(val * 1.02, i, f"{pct:.1f}%", va='center', fontsize=8, color=DARKGREY)
ax3.set_facecolor(CREAM)
ax3.spines[['top', 'right', 'left']].set_visible(False)
ax3.xaxis.set_visible(False)
ax3.set_title("FX Exposure by Currency", color=NAVY, fontsize=10, pad=8)
ax3.tick_params(axis='y', colors=DARKGREY)
ax3.legend(handles=[
    mpatches.Patch(color=RED,  label='Sovereign risk'),
    mpatches.Patch(color=NAVY, label='Standard corridor'),
], fontsize=7)

ax4 = fig.add_subplot(gs[1, 2])
ax4.set_facecolor(NAVY)
churn_count = len(churn)
churn_aum = churn['current_aum_usd'].sum() if 'current_aum_usd' in churn.columns else 0
ax4.text(0.5, 0.72, str(churn_count), ha='center', va='center',
         fontsize=36, fontweight='bold', color=RED, transform=ax4.transAxes)
ax4.text(0.5, 0.52, "Clients at Churn Risk", ha='center', va='center',
         fontsize=11, color=CREAM, transform=ax4.transAxes)
ax4.text(0.5, 0.35, "No inflow > 180 days", ha='center', va='center',
         fontsize=9, color=GREY, transform=ax4.transAxes)
ax4.text(0.5, 0.18, f"AUM at risk: {fmt_usd(churn_aum)}", ha='center', va='center',
         fontsize=10, color=AMBER, transform=ax4.transAxes)
ax4.axis('off')
ax4.set_title("Churn Early Warning", color=NAVY, fontsize=10, pad=8)

plt.savefig("05_visualization/outputs/page_3_transaction_intelligence.png",
            dpi=150, bbox_inches='tight', facecolor=CREAM)
plt.close()
print("  Page 3 saved.")

print("\nAll charts saved to 05_visualization/outputs/")
print("Done.")
