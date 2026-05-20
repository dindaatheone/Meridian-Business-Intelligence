content = open('generate_charts.py').read()
content = content.replace(
    "monthly_sorted['rolling_3m_avg'].fillna(0)",
    "monthly_sorted['net_flow'].rolling(3, min_periods=1).mean().fillna(0)"
)
open('generate_charts.py', 'w').write(content)
print('Done')
