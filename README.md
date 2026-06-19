# Amazon BI — Proactive Analysis Initiative

**Unsolicited analysis built and submitted as a supplement to Amazon's BA Intern application (Job ID 3100573).** Instead of describing what I can do for Amazon — I did it.

Using a public e-commerce dataset as an Amazon marketplace proxy, I answered the question a BA team actually asks: **where is revenue leaking, and what should we prioritise first?**

Built by [Kavyanjali Karan](https://linkedin.com/in/kavyanjali-karan) · SOA University 2027 · March 2026

---

## Why I Built This

Amazon's BA Intern role (JD 3100573) asks for candidates who can translate ambiguous business questions into structured data analysis and communicate findings to cross-functional stakeholders.

Rather than claim that capability in a cover letter, I ran the analysis unsolicited — on Amazon-relevant data, framed for Amazon's context — and submitted it alongside my application.

This is the work.

---

## Business Question

> *Where is revenue leaking in this e-commerce marketplace, and what should the business prioritise first to recover it?*

---

## Analysis Modules

### 1. Revenue Concentration (Pareto Analysis)

**Finding:** The top 20% of products drive 67% of total revenue — a classic Pareto distribution. Category concentration risk is high: 2 of 8 categories account for 51% of revenue.

**Recommendation:** Build automated revenue concentration alerts. Any category dropping below its 3-month moving average by >15% should trigger a review — this is a BI infrastructure gap, not a one-time analysis.

---

### 2. Customer RFM Segmentation

**Finding:** 23% of customers classified as "At Risk" — high historical value, no purchase in 60+ days. This segment represents the highest ROI retention opportunity: they've already demonstrated willingness to pay.

| Segment | % of Customers | Revenue Contribution |
|---|---|---|
| Champions | 18% | 41% |
| Loyal | 22% | 31% |
| At Risk | 23% | 19% |
| Lost | 37% | 9% |

**Recommendation:** Reactivation campaign targeting At Risk segment. Cost per reactivation is 5–7× lower than new customer acquisition. Expected revenue recovery: 8–12% of current At Risk contribution within 90 days.

---

### 3. Delivery Funnel Analysis

**Finding:** Order → Delivered conversion is 84.3%. The 15.7% gap concentrates in two stages: Warehouse Processing (6.1% drop) and Last-Mile Delivery (7.2% drop).

**Recommendation:** The last-mile gap is disproportionately high in Tier 2/3 cities. A delivery prediction model (estimated ETA vs actual) would allow proactive customer communication — converting a negative experience into a trust-building touchpoint.

---

### 4. Late Delivery Impact on Retention

**Finding:** Customers who received one late delivery have a 34% lower repeat purchase rate in the following 30 days. Customers who received two have a 61% lower rate.

**Recommendation:** Late delivery is the single strongest leading indicator of churn identified in this dataset. Flagging customers who just experienced a late delivery for a proactive service recovery intervention (voucher or apology message) would reduce this gap materially.

---

## Key Findings Summary

| Finding | Business Impact |
|---|---|
| Top 20% products = 67% revenue | Concentration risk — needs monitoring infrastructure |
| 23% customers At Risk | Highest-ROI retention opportunity available |
| 15.7% order-to-delivery drop | Recoverable with last-mile prediction model |
| 1 late delivery → 34% lower retention | Proactive service recovery has measurable ROI |

---

## Priority Recommendation (Ranked)

1. **Reactivate At Risk customers** — highest ROI, lowest cost, fastest to implement
2. **Build delivery prediction model** — proactive communication converts negative experience into trust
3. **Implement revenue concentration monitoring** — automated alerts prevent category blind spots
4. **Late delivery service recovery workflow** — data shows material retention impact; easy to operationalise

---

## Tools & Methods

`Python` · `Pandas` · `Plotly` · `RFM Segmentation` · `Pareto Analysis` · `Funnel Analytics` · `Cohort Analysis`

---

## File Structure

```
amazon-bi-proactive-analysis/
├── data/
│   └── ecommerce_data.csv          ← Public dataset (Amazon marketplace proxy)
├── Amazon_BA_Analysis_Kavyanjali.ipynb  ← Full analysis notebook
└── README.md
```

---

## How to Run

```bash
git clone https://github.com/kavyanjali-karan/amazon-bi-proactive-analysis
cd amazon-bi-proactive-analysis
pip install pandas plotly jupyter
jupyter notebook Amazon_BA_Analysis_Kavyanjali.ipynb
```

---

**Kavyanjali Karan** · B.Tech CSE, ITER SOA University (2027)  
Selected: McKinsey Forward 2026 · Google Gen AI Academy APAC 2026  
[LinkedIn](https://linkedin.com/in/kavyanjali-karan) · [GitHub](https://github.com/kavyanjali-karan) · karankavyanjali77@gmail.com
