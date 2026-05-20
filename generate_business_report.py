# Meridian Business Intelligence
# Business Report PDF Generator
# Executive-ready report combining all findings, charts,
# and strategic recommendations
#
# Input:  06_business_report/findings_summary.md
#         06_business_report/hypothesis_statement.md
#         04_advanced_analysis/outputs/*.png
#         05_visualization/outputs/*.png
#
# Output: 06_business_report/outputs/business_report.pdf

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, Image, HRFlowable
)
from reportlab.platypus import KeepTogether

os.makedirs("06_business_report/outputs", exist_ok=True)

# ── Colors ────────────────────────────────────────────────────
NAVY  = colors.HexColor('#1E3A5F')
GOLD  = colors.HexColor('#B8962E')
CREAM = colors.HexColor('#F5F0E8')
RED   = colors.HexColor('#B71C1C')
GREEN = colors.HexColor('#2E7D32')
LIGHT = colors.HexColor('#E8EEF4')
WHITE = colors.white
BLACK = colors.black
DGREY = colors.HexColor('#424242')

W, H = A4
ML = 20*mm
MR = 20*mm
MT = 20*mm
MB = 20*mm

# ── Styles ────────────────────────────────────────────────────
styles = getSampleStyleSheet()

cover_title = ParagraphStyle('cover_title',
    fontSize=28, fontName='Helvetica-Bold',
    textColor=WHITE, alignment=TA_CENTER, spaceAfter=8)

cover_sub = ParagraphStyle('cover_sub',
    fontSize=13, fontName='Helvetica',
    textColor=CREAM, alignment=TA_CENTER, spaceAfter=6)

cover_meta = ParagraphStyle('cover_meta',
    fontSize=10, fontName='Helvetica',
    textColor=GOLD, alignment=TA_CENTER, spaceAfter=4)

section_head = ParagraphStyle('section_head',
    fontSize=16, fontName='Helvetica-Bold',
    textColor=NAVY, spaceBefore=14, spaceAfter=8)

sub_head = ParagraphStyle('sub_head',
    fontSize=12, fontName='Helvetica-Bold',
    textColor=NAVY, spaceBefore=10, spaceAfter=5)

body = ParagraphStyle('body',
    fontSize=9.5, fontName='Helvetica',
    textColor=DGREY, leading=15, spaceAfter=6)

body_gold = ParagraphStyle('body_gold',
    fontSize=9.5, fontName='Helvetica-Bold',
    textColor=GOLD, leading=15, spaceAfter=4)

caption = ParagraphStyle('caption',
    fontSize=8, fontName='Helvetica',
    textColor=DGREY, alignment=TA_CENTER, spaceAfter=8)

kpi_style = ParagraphStyle('kpi_style',
    fontSize=9, fontName='Helvetica',
    textColor=NAVY, leading=13,
    leftIndent=10, spaceAfter=4)

conf_label = ParagraphStyle('conf',
    fontSize=8, fontName='Helvetica',
    textColor=DGREY, alignment=TA_RIGHT)

def hr(color=NAVY, thickness=1):
    return HRFlowable(width='100%', thickness=thickness,
                      color=color, spaceAfter=6, spaceBefore=2)

def finding_badge(text, confirmed=True):
    color = GREEN if confirmed else RED
    label = 'CONFIRMED' if confirmed else 'REJECTED'
    data = [[Paragraph(f'<b>H{text}: {label}</b>',
                       ParagraphStyle('badge', fontSize=8,
                                      fontName='Helvetica-Bold',
                                      textColor=WHITE))]]
    t = Table(data, colWidths=[60*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    return t

def metric_box(label, value, sub=''):
    data = [
        [Paragraph(f'<b>{value}</b>',
                   ParagraphStyle('mv', fontSize=16, fontName='Helvetica-Bold',
                                  textColor=GOLD, alignment=TA_CENTER))],
        [Paragraph(label,
                   ParagraphStyle('ml', fontSize=8, fontName='Helvetica-Bold',
                                  textColor=WHITE, alignment=TA_CENTER))],
    ]
    if sub:
        data.append([Paragraph(sub,
                    ParagraphStyle('ms', fontSize=7, fontName='Helvetica',
                                   textColor=CREAM, alignment=TA_CENTER))])
    t = Table(data, colWidths=[52*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), NAVY),
        ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('ROUNDEDCORNERS', [3]),
    ]))
    return t

def add_chart(story, path, width_mm=160, caption_text=''):
    if os.path.exists(path):
        img = Image(path, width=width_mm*mm,
                    height=width_mm*mm*0.55)
        story.append(img)
        if caption_text:
            story.append(Paragraph(caption_text, caption))
    else:
        story.append(Paragraph(f'[Chart not found: {path}]', caption))

# ══════════════════════════════════════════════════════════════
# BUILD DOCUMENT
# ══════════════════════════════════════════════════════════════
story = []

doc = SimpleDocTemplate(
    "06_business_report/outputs/business_report.pdf",
    pagesize=A4,
    leftMargin=ML, rightMargin=MR,
    topMargin=MT, bottomMargin=MB,
    title="Meridian Private Bank - Business Intelligence Report",
    author="Meridian Capital Management Pte. Ltd."
)

# ── COVER PAGE ────────────────────────────────────────────────
cover_bg = Table(
    [[Paragraph('MERIDIAN PRIVATE BANK', cover_title)],
     [Paragraph('Business Intelligence Report', cover_sub)],
     [Spacer(1, 6)],
     [Paragraph('Synthetic Portfolio | 24-Month Analysis', cover_meta)],
     [Paragraph('Singapore MAS Jurisdiction | CN-SG-ID-MO-BN Corridor', cover_meta)],
     [Spacer(1, 20)],
     [Paragraph('Prepared by Meridian Capital Management Pte. Ltd.', cover_meta)],
     [Paragraph('Confidential | For Authorized Recipients Only', cover_meta)],
    ],
    colWidths=[W - ML - MR]
)
cover_bg.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), NAVY),
    ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 8),
    ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ('LEFTPADDING',   (0,0), (-1,-1), 16),
    ('RIGHTPADDING',  (0,0), (-1,-1), 16),
]))
story.append(Spacer(1, 40*mm))
story.append(cover_bg)
story.append(Spacer(1, 20*mm))

metrics = Table(
    [[metric_box('Total Book AUM', 'USD 1.3B+', '200 clients'),
      metric_box('Concentration Risk', '58.35%', 'ELEVATED'),
      metric_box('AUM Forecast', 'USD 1.38B', 'Base Case May 2026')]],
    colWidths=[56*mm, 56*mm, 56*mm],
    hAlign='CENTER'
)
story.append(metrics)
story.append(PageBreak())

# ── EXECUTIVE SUMMARY ─────────────────────────────────────────
story.append(Paragraph('Executive Summary', section_head))
story.append(hr())

story.append(Paragraph(
    'Meridian Business Intelligence interrogates 24 months of synthetic private banking '
    'data across the China, Singapore, Indonesia, Macau, and Brunei corridors. '
    'The analysis runs five layers deep: SQL exploratory analysis, SQL business metrics, '
    'statistical analysis, credit risk scoring, and AUM forecasting. '
    'Four business hypotheses were tested. All four were confirmed.',
    body))

story.append(Spacer(1, 4))

summary_data = [
    ['Finding', 'Result', 'Priority Action'],
    ['AUM Concentration Risk', 'H1 Confirmed: 58.35%', 'Elevate top-decile RM accountability'],
    ['Churn Signal Detection', 'H2 Confirmed', 'Weekly churn query, 5-day RM response SLA'],
    ['CLV by Corridor', 'H3 Confirmed with nuance', 'Weight senior RM to SG and BN corridors'],
    ['Credit Risk Distribution', 'H4 Confirmed (model architecture)', 'Apply tier-specific DTI caps in production'],
    ['AUM Trajectory', 'Additional: positive momentum', 'Monitor net flow vs base case monthly'],
]

t = Table(summary_data, colWidths=[55*mm, 60*mm, 55*mm])
t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0), NAVY),
    ('TEXTCOLOR',     (0,0), (-1,0), WHITE),
    ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 8.5),
    ('FONTNAME',      (0,1), (-1,-1), 'Helvetica'),
    ('TEXTCOLOR',     (0,1), (-1,-1), DGREY),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LIGHT]),
    ('ALIGN',         (0,0), (-1,-1), 'LEFT'),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('GRID',          (0,0), (-1,-1), 0.3, colors.HexColor('#CCCCCC')),
]))
story.append(t)
story.append(PageBreak())

# ── BUSINESS PROBLEM ──────────────────────────────────────────
story.append(Paragraph('Business Problem and Hypotheses', section_head))
story.append(hr())

story.append(Paragraph(
    'Private banks generate relationship intelligence continuously through client '
    'transactions, portfolio rebalancing events, fee accruals, and inflow and outflow '
    'patterns. Most institutions cannot capture this intelligence systematically. '
    'The result is AUM attrition that could have been detected weeks before formal exit, '
    'concentration risk that accumulates invisibly until a major client departure creates '
    'a revenue shock, and CLV that is systematically underestimated because fee revenue '
    'is tracked but relationship depth is not.',
    body))

story.append(Paragraph(
    'Meridian Business Intelligence is built to close that gap. This report documents '
    'what the 24-month synthetic data universe reveals about the health of a private '
    'banking book when interrogated at institutional depth.',
    body))

hypo_data = [
    ['Hypothesis', 'Statement', 'Result'],
    ['H1', 'Top 10% of clients hold more than 40% of total AUM', 'CONFIRMED: 58.35%'],
    ['H2', 'Churn signals are detectable before formal exit (180-day threshold)', 'CONFIRMED'],
    ['H3', 'CLV varies significantly by jurisdiction and tier', 'CONFIRMED with nuance'],
    ['H4', 'A meaningful subset carry DTI above 0.50', 'CONFIRMED (model architecture)'],
]
t2 = Table(hypo_data, colWidths=[18*mm, 100*mm, 52*mm])
t2.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0), NAVY),
    ('TEXTCOLOR',     (0,0), (-1,0), WHITE),
    ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 8.5),
    ('FONTNAME',      (0,1), (-1,-1), 'Helvetica'),
    ('TEXTCOLOR',     (0,1), (-1,-1), DGREY),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LIGHT]),
    ('ALIGN',         (0,0), (0,-1), 'CENTER'),
    ('ALIGN',         (1,0), (2,-1), 'LEFT'),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('GRID',          (0,0), (-1,-1), 0.3, colors.HexColor('#CCCCCC')),
]))
story.append(t2)
story.append(PageBreak())

# ── FINDING 1 ─────────────────────────────────────────────────
story.append(Paragraph('Finding 1 - AUM Concentration Risk', section_head))
story.append(hr())
story.append(finding_badge('1', confirmed=True))
story.append(Spacer(1, 6))

story.append(Paragraph(
    'The top 10% of clients hold 58.35% of total book AUM, significantly above '
    'the 40% elevated threshold. At this concentration level, the departure of two '
    'or three top-decile clients in the same quarter creates a revenue shock the '
    'remaining book cannot absorb. The book is running implicit key-man risk on '
    'its largest relationships.',
    body))

story.append(Paragraph(
    'The China corridor drives the concentration. 40% of total AUM originates from '
    'Chinese clients, and within that corridor the UHNW tier is disproportionately '
    'concentrated with a small number of relationships.',
    body))

story.append(Paragraph('Recommendation:', body_gold))
story.append(Paragraph(
    'Elevate RM accountability for every top-decile client to senior level. '
    'Increase review frequency to monthly for the top 20 relationships by AUM. '
    'Begin deliberate mid-market acquisition in Singapore and Indonesia to dilute '
    'concentration over 18 months.',
    body))

story.append(Paragraph('KPI:', body_gold))
story.append(Paragraph(
    'Top decile concentration ratio reviewed monthly. Target: below 45% within '
    '12 months, below 35% within 24 months.',
    kpi_style))

story.append(Spacer(1, 4))
add_chart(story,
          '05_visualization/outputs/page_1_executive_overview.png',
          caption_text='Executive Overview: AUM concentration, growth trend, and RM productivity')
story.append(PageBreak())

# ── FINDING 2 ─────────────────────────────────────────────────
story.append(Paragraph('Finding 2 - Churn Signal Detection', section_head))
story.append(hr())
story.append(finding_badge('2', confirmed=True))
story.append(Spacer(1, 6))

story.append(Paragraph(
    'The churn detection query identifies active clients with no inflow recorded '
    'in the last 180 days. Every flagged client represents a relationship that has '
    'gone silent without formal exit. The 180-day window is conservative. In practice '
    'the intervention window opens earlier, around 90 days of inflow cessation, '
    'before the relationship fully disengages.',
    body))

story.append(Paragraph(
    'The RM accountability structure matters. Each flagged client has an assigned RM. '
    'If that RM has not made contact within the last 30 days, the flag is a governance '
    'failure as much as a relationship risk.',
    body))

story.append(Paragraph('Recommendation:', body_gold))
story.append(Paragraph(
    'Run the churn detection query weekly as an operational report. Route every newly '
    'flagged client to the assigned RM within five business days. Document the '
    'intervention and outcome in the relationship record.',
    body))

story.append(Paragraph('KPI:', body_gold))
story.append(Paragraph(
    'Churn signal response rate. Target: 100% of flagged clients contacted within '
    'five business days. Secondary: reduction in formal churn rate over 12 months.',
    kpi_style))

story.append(Spacer(1, 4))
add_chart(story,
          '05_visualization/outputs/page_2_client_analytics.png',
          caption_text='Client Analytics: corridor distribution, risk profiles, churn signals, AUM concentration by decile')
story.append(PageBreak())

# ── FINDING 3 ─────────────────────────────────────────────────
story.append(Paragraph('Finding 3 - Client Lifetime Value by Corridor', section_head))
story.append(hr())
story.append(finding_badge('3', confirmed=True))
story.append(Spacer(1, 6))

story.append(Paragraph(
    'CLV varies significantly by tier as expected. UHNW clients generate '
    'disproportionately higher estimated 10-year fee revenue at every corridor. '
    'The corridor dimension produces a less intuitive result.',
    body))

story.append(Paragraph(
    'Singapore UHNW clients show higher average CLV than China UHNW clients in '
    'several RM books, driven by longer average tenure and higher management fee '
    'consistency. China UHNW clients carry larger AUM but show more volatility due '
    'to mandate migration patterns and periodic large outflow events.',
    body))

story.append(Paragraph(
    'Brunei, despite representing 5% of client count, produces CLV per client '
    'competitive with Singapore at the VHNW tier. The corridor is underinvested '
    'relative to its revenue contribution per relationship.',
    body))

story.append(Paragraph('Recommendation:', body_gold))
story.append(Paragraph(
    'Weight senior RM capacity toward Singapore and Brunei for VHNW and UHNW '
    'segments. Review China UHNW mandate structures to reduce outflow volatility '
    'and improve fee revenue predictability.',
    body))

story.append(Paragraph('KPI:', body_gold))
story.append(Paragraph(
    'Revenue per RM by corridor reviewed quarterly. Target: Singapore and Brunei '
    'corridors achieve 40% above mean revenue per client within 18 months.',
    kpi_style))
story.append(PageBreak())

# ── FINDING 4 ─────────────────────────────────────────────────
story.append(Paragraph('Finding 4 - Credit Risk Distribution', section_head))
story.append(hr())
story.append(finding_badge('4', confirmed=True))
story.append(Spacer(1, 6))

story.append(Paragraph(
    'The credit risk scoring model assigns clients to four tiers based on '
    'debt-to-income and debt-to-capital ratios.',
    body))

risk_data = [
    ['Risk Tier', 'Client Count', 'Share of Book'],
    ['A - Low',       '25',  '9%'],
    ['B - Moderate',  '21',  '8%'],
    ['C - High',      '10',  '4%'],
    ['D - Critical',  '215', '79%'],
    ['Total Active',  '271', '100%'],
]
t3 = Table(risk_data, colWidths=[80*mm, 50*mm, 40*mm])
t3.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0), NAVY),
    ('TEXTCOLOR',     (0,0), (-1,0), WHITE),
    ('FONTNAME',      (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE',      (0,0), (-1,-1), 9),
    ('FONTNAME',      (0,1), (-1,-1), 'Helvetica'),
    ('TEXTCOLOR',     (0,1), (0,1), GREEN),
    ('TEXTCOLOR',     (0,2), (0,2), colors.HexColor('#B8962E')),
    ('TEXTCOLOR',     (0,3), (0,3), colors.HexColor('#E65100')),
    ('TEXTCOLOR',     (0,4), (0,4), RED),
    ('FONTNAME',      (0,1), (-1,-1), 'Helvetica'),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, LIGHT, WHITE, LIGHT, WHITE]),
    ('ALIGN',         (1,0), (2,-1), 'CENTER'),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0), (-1,-1), 5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ('GRID',          (0,0), (-1,-1), 0.3, colors.HexColor('#CCCCCC')),
    ('FONTNAME',      (0,5), (-1,5), 'Helvetica-Bold'),
    ('BACKGROUND',    (0,5), (-1,5), LIGHT),
]))
story.append(t3)
story.append(Spacer(1, 6))

story.append(Paragraph(
    'Note: The D Critical concentration at 79% reflects a synthetic data generation '
    'artifact. The generator applied debt parameters uniformly without tier-based '
    'constraints. In a real private banking book, UHNW clients typically carry '
    'conservative leverage relative to their asset base. The model architecture, '
    'DTI and DTC thresholds, and four-tier classification are correct and production-ready.',
    body))

story.append(Paragraph('Recommendation:', body_gold))
story.append(Paragraph(
    'Apply tier-specific DTI caps to the data generator for realistic production '
    'credit distribution. In deployment, restrict new credit extensions for D Critical '
    'clients and require quarterly facility review for C High clients.',
    body))

story.append(Spacer(1, 4))
add_chart(story,
          '04_advanced_analysis/outputs/risk_distribution.png',
          caption_text='Credit Risk: client count by tier and DTI vs DTC scatter by risk classification')
story.append(PageBreak())

# ── FINDING 5 ─────────────────────────────────────────────────
story.append(Paragraph('Finding 5 - AUM Trajectory and Forecast', section_head))
story.append(hr())
story.append(Spacer(1, 4))

story.append(Paragraph(
    'The 24-month cumulative net flow trend shows positive AUM momentum throughout '
    'the observation period. The 6-month moving average projection estimates base '
    'case AUM reaching approximately USD 1.38B by May 2026, with a 95% confidence '
    'interval ranging from USD 1.21B to USD 1.55B.',
    body))

story.append(Paragraph(
    'The forecast captures relationship-driven AUM change: inflows from deepening '
    'relationships, outflows from withdrawals, fee drag. It does not capture market '
    'appreciation or depreciation on existing AUM. The positive trajectory is '
    'consistent with a book in healthy growth phase.',
    body))

story.append(Paragraph('Recommendation:', body_gold))
story.append(Paragraph(
    'Monitor actual monthly net flow against the base case projection. A single month '
    'below the lower confidence bound warrants investigation. Two consecutive months '
    'below the lower bound triggers a senior review of RM productivity and the '
    'corridor acquisition pipeline.',
    body))

story.append(Paragraph('KPI:', body_gold))
story.append(Paragraph(
    'Positive net flow in at least 10 of every 12 months. Alert threshold: two '
    'consecutive months of net outflow triggers senior review.',
    kpi_style))

story.append(Spacer(1, 4))
add_chart(story,
          '04_advanced_analysis/outputs/aum_forecast.png',
          caption_text='AUM Trend and 6-Month Projection with 95% Confidence Interval')
story.append(PageBreak())

# ── APPENDIX ──────────────────────────────────────────────────
story.append(Paragraph('Appendix - Dashboard Charts', section_head))
story.append(hr())

story.append(Paragraph('Transaction Intelligence Dashboard', sub_head))
add_chart(story,
          '05_visualization/outputs/page_3_transaction_intelligence.png',
          caption_text='Monthly flows, fee revenue decomposition, corridor net flow, FX exposure, churn early warning')

story.append(Spacer(1, 6))
story.append(Paragraph('Statistical Analysis', sub_head))
add_chart(story,
          '04_advanced_analysis/outputs/aum_distribution.png',
          caption_text='AUM distribution by client tier and jurisdiction')

story.append(PageBreak())
story.append(Paragraph('Correlation Matrix', sub_head))
add_chart(story,
          '04_advanced_analysis/outputs/correlation_matrix.png',
          caption_text='Pearson correlation across key client and portfolio variables')

story.append(Spacer(1, 10))
story.append(hr(GOLD, 0.5))
story.append(Paragraph(
    'Meridian Capital Management Pte. Ltd.  |  Singapore MAS Jurisdiction  |  Confidential',
    conf_label))

# ── BUILD ─────────────────────────────────────────────────────
doc.build(story)
print("Business report saved to 06_business_report/outputs/business_report.pdf")
