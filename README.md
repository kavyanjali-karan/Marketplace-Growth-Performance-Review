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

## Executive Summary

This project analyzes the Brazilian Olist marketplace dataset to identify growth opportunities through customer segmentation, revenue analysis, retention evaluation, and funnel diagnostics.

The objective is to simulate the type of business analysis performed by Amazon Business Analysts when evaluating marketplace performance, customer behavior, and operational efficiency.

The analysis culminates in prioritized recommendations designed to improve revenue growth, customer retention, and marketplace performance.

---

## Resume Highlights

- Analyzed 100k+ e-commerce orders across multiple relational datasets
- Built customer segmentation framework using RFM methodology
- Performed revenue, category, and funnel analysis
- Identified customer retention and conversion opportunities
- Developed executive-level recommendations supported by data
- Demonstrated SQL-style business analytics workflows

---

## Business Problem

E-commerce platforms generate large volumes of customer, order, seller, payment, and product data.

Without structured analysis, decision-makers struggle to determine:

- Which customers drive the most value
- Which product categories contribute most revenue
- Where conversion opportunities are lost
- Which customer segments require retention strategies

This project investigates these questions using transactional marketplace data.

---

## Dataset

Brazilian Olist Marketplace Dataset

Data Sources:

- Customers
- Orders
- Payments
- Reviews
- Products
- Sellers
- Geolocation

Combined dataset contains over 100,000 orders across multiple years and provides a realistic representation of marketplace operations.

---

## Analysis Modules

## Revenue Analysis

Key Questions:

- How does revenue evolve over time?
- Which periods contribute the most sales?
- Are there seasonal trends?

Outcome:

Revenue trend analysis identified periods of accelerated marketplace growth and highlighted fluctuations that warrant operational investigation.

---

## Product Category Analysis

Key Questions:

- Which categories generate the highest revenue?
- Which categories generate the highest order volume?
- Are revenue and volume concentrated?

Outcome:

Category-level analysis identified the marketplace's most valuable product segments and opportunities for targeted expansion.

---

## Customer Segmentation (RFM)

RFM Variables:

- Recency
- Frequency
- Monetary Value

Segments:

- Champions
- Loyal Customers
- Potential Loyalists
- At Risk
- Lost Customers

Outcome:

Customer segmentation enabled prioritization of retention and re-engagement strategies.

---

### 4. Late Delivery Impact on Retention

## Funnel Analysis

Key Questions:

- Where do customers drop off?
- Which stages create friction?
- What operational improvements could increase conversion?

Outcome:

Funnel analysis highlighted opportunities to improve customer experience and reduce conversion leakage.

---

## Key Findings

### Finding 1

A small subset of customers contributes a disproportionate share of revenue.

### Finding 2

Several product categories dominate marketplace sales.

### Finding 3

At-risk customer segments represent significant retention opportunities.

### Finding 4

Operational bottlenecks exist within the purchase journey and contribute to conversion loss.

### Finding 5

Customer behavior patterns support differentiated lifecycle strategies.

---

## Recommendations

### Priority 1 — Retain High-Value Customers

Develop loyalty programs targeting Champion and Loyal segments.

### Priority 2 — Re-Engage At-Risk Customers

Deploy lifecycle marketing campaigns before churn occurs.

### Priority 3 — Double Down on High-Performing Categories

Increase visibility and inventory investment in top-performing categories.

### Priority 4 — Improve Funnel Conversion

Investigate friction points identified during checkout and fulfillment stages.

### Priority 5 — Strengthen Review Collection

Higher review participation improves trust and conversion performance.

---

## Tools & Methods

`Python` · `Pandas` · `Plotly` · `RFM Segmentation` · `Pareto Analysis` · `Funnel Analytics` · `Cohort Analysis`

---

## File Structure

```
amazon-business-analyst-case-study/
│
├── README.md
├── Amazon_BA_Analysis_Kavyanjali.ipynb
├── requirements.txt
│
├── data/
│   ├── olist_customers_dataset.csv
│   ├── olist_geolocation_dataset.csv
│   ├── olist_orders_dataset.csv
│   ├── olist_order_items_dataset.csv
│   ├── olist_order_payments_dataset.csv
│   ├── olist_order_reviews_dataset.csv
│   ├── olist_products_dataset.csv
│   ├── olist_sellers_dataset.csv
│   └── product_category_name_translation.csv
│
├── sql/
│   ├── revenue_analysis.sql
│   ├── customer_segmentation.sql
│   ├── retention_analysis.sql
│   └── funnel_analysis.sql
│
├── outputs/
│   ├── executive_summary.md
│   ├── revenue_trend.png
│   ├── category_analysis.png
│   ├── customer_segments.png
│   ├── funnel_analysis.png
│   └── recommendations.md
│
└── screenshots/
    ├── revenue_dashboard.png
    ├── category_dashboard.png
    ├── rfm_dashboard.png
    ├── funnel_dashboard.png
    └── executive_summary.png

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
