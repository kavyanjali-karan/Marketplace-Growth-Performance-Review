"""
Generate data-driven Marketplace dashboard from actual CSV data.

Reads raw and curated CSVs, computes real metrics, and produces
an interactive HTML dashboard with Chart.js.

Usage: python python/generate_dashboards.py
Output: assets/dashboard.html
"""

import csv
import json
import tempfile
from collections import defaultdict
from pathlib import Path

# Chart.js is inlined when a local copy exists (CI downloads one), so the
# dashboard works offline and without depending on a CDN at view time.
CHART_JS = Path(tempfile.gettempdir()) / "chart.min.js"
CHART_JS_URL = "https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"
if CHART_JS.exists():
    CHART_JS_TAG = "<script>\n" + CHART_JS.read_text(encoding="utf-8") + "\n</script>"
else:
    CHART_JS_TAG = f'<script src="{CHART_JS_URL}"></script>'


ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
OUTPUT = ROOT / "assets" / "dashboard.html"


def read_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def compute_metrics():
    orders = read_csv(DATA_DIR / "raw" / "orders.csv")
    products = {p["product_id"]: p for p in read_csv(DATA_DIR / "raw" / "products.csv")}
    customers = read_csv(DATA_DIR / "raw" / "customers.csv")
    sellers = {s["seller_id"]: s for s in read_csv(DATA_DIR / "raw" / "sellers.csv")}

    total_rev = sum(float(o["revenue"]) for o in orders)
    total_orders = len(orders)
    total_buyers = len(customers)

    # Revenue by category
    cat_rev = defaultdict(float)
    cat_count = defaultdict(int)
    for o in orders:
        cat = products[o["product_id"]]["category"]
        cat_rev[cat] += float(o["revenue"])
        cat_count[cat] += 1

    # Revenue by status
    status_counts = defaultdict(int)
    for o in orders:
        status_counts[o["order_status"]] += 1

    # Monthly revenue
    monthly = defaultdict(float)
    monthly_count = defaultdict(int)
    for o in orders:
        m = o["order_date"][:7]
        monthly[m] += float(o["revenue"])
        monthly_count[m] += 1

    months_sorted = sorted(monthly.keys())

    # Payment methods
    payment_counts = defaultdict(int)
    for o in orders:
        payment_counts[o["payment_method"]] += 1

    # Top sellers
    seller_rev = defaultdict(float)
    seller_orders = defaultdict(int)
    for o in orders:
        sid = o["seller_id"]
        seller_rev[sid] += float(o["revenue"])
        seller_orders[sid] += 1
    top_sellers = sorted(seller_rev.items(), key=lambda x: -x[1])[:5]

    return {
        "total_rev": total_rev,
        "total_orders": total_orders,
        "total_buyers": total_buyers,
        "cat_rev": dict(sorted(cat_rev.items(), key=lambda x: -x[1])),
        "cat_count": dict(cat_count),
        "status_counts": dict(status_counts),
        "months": months_sorted,
        "monthly_rev": [round(monthly[m] / 1e6, 1) for m in months_sorted],
        "monthly_count": [monthly_count[m] for m in months_sorted],
        "payment_counts": dict(sorted(payment_counts.items(), key=lambda x: -x[1])),
        "top_sellers": [(sid, round(seller_rev[sid] / 1e6, 1), seller_orders[sid],
                         sellers.get(sid, {}).get("tier", "Unknown")) for sid, _ in top_sellers],
    }


def generate_html(m):
    cat_pcts = {k: round(v / m["total_rev"] * 100, 1) for k, v in m["cat_rev"].items()}
    elec_pct = cat_pcts.get("Electronics", 0)
    ret_pct = round((m["status_counts"].get("Returned", 0) + m["status_counts"].get("Cancelled", 0)) / m["total_orders"] * 100, 1)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Marketplace Revenue Analytics</title>
    {CHART_JS_TAG}
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #f4f6f9; color: #1e293b; }}
        .topbar {{ background: #1a1f36; color: #fff; padding: 10px 24px; display: flex; justify-content: space-between; align-items: center; }}
        .topbar h1 {{ font-size: 15px; font-weight: 600; }}
        .topbar .sub {{ color: #94a3b8; font-size: 11px; }}
        .dash {{ padding: 16px 24px; }}
        .kpi-row {{ display: grid; grid-template-columns: repeat(5,1fr); gap: 14px; margin-bottom: 16px; }}
        .kpi {{ background: #fff; border-radius: 8px; padding: 16px 18px; box-shadow: 0 1px 2px rgba(0,0,0,0.06); border-top: 3px solid #3b82f6; }}
        .kpi:nth-child(2) {{ border-top-color: #10b981; }}
        .kpi:nth-child(3) {{ border-top-color: #f59e0b; }}
        .kpi:nth-child(4) {{ border-top-color: #ef4444; }}
        .kpi:nth-child(5) {{ border-top-color: #8b5cf6; }}
        .kpi-label {{ font-size: 11px; color: #64748b; text-transform: uppercase; margin-bottom: 4px; }}
        .kpi-val {{ font-size: 26px; font-weight: 700; }}
        .kpi-note {{ font-size: 10px; color: #94a3b8; margin-top: 3px; }}
        .row {{ display: grid; gap: 14px; margin-bottom: 16px; }}
        .row-2 {{ grid-template-columns: 3fr 2fr; }}
        .row-eq {{ grid-template-columns: 1fr 1fr; }}
        .box {{ background: #fff; border-radius: 8px; padding: 16px 18px; box-shadow: 0 1px 2px rgba(0,0,0,0.06); }}
        .box-title {{ font-size: 12px; font-weight: 600; color: #475569; margin-bottom: 12px; text-transform: uppercase; }}
        table.dt {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
        table.dt th {{ text-align: left; padding: 7px 8px; background: #f8fafc; border-bottom: 2px solid #e2e8f0; font-weight: 600; color: #64748b; font-size: 10px; text-transform: uppercase; }}
        table.dt td {{ padding: 6px 8px; border-bottom: 1px solid #f1f5f9; }}
        .footer {{ text-align: center; padding: 14px; font-size: 10px; color: #cbd5e1; }}
    </style>
</head>
<body>
<div class="topbar">
    <h1>&#x1F4CA; Marketplace Revenue Analytics</h1>
    <span class="sub">{m['total_orders']:,} orders &middot; {m['total_buyers']:,} buyers &middot; Generated from live data</span>
</div>
<div class="dash">
    <div class="kpi-row">
        <div class="kpi"><div class="kpi-label">Total Revenue</div><div class="kpi-val">${m['total_rev']/1e9:.2f}B</div><div class="kpi-note">{m['total_orders']:,} orders processed</div></div>
        <div class="kpi"><div class="kpi-label">Unique Buyers</div><div class="kpi-val">{m['total_buyers']:,}</div><div class="kpi-note">Avg ${m['total_rev']/m['total_buyers']:,.0f}/buyer</div></div>
        <div class="kpi"><div class="kpi-label">Electronics Share</div><div class="kpi-val">{elec_pct}%</div><div class="kpi-note">${m['cat_rev'].get('Electronics',0)/1e9:.2f}B of ${m['total_rev']/1e9:.2f}B</div></div>
        <div class="kpi"><div class="kpi-label">Returns + Cancel</div><div class="kpi-val">{ret_pct}%</div><div class="kpi-note">{m['status_counts'].get('Returned',0)+m['status_counts'].get('Cancelled',0):,} orders</div></div>
        <div class="kpi"><div class="kpi-label">Categories</div><div class="kpi-val">{len(m['cat_rev'])}</div><div class="kpi-note">Product lines</div></div>
    </div>

    <div class="row row-2">
        <div class="box">
            <div class="box-title">Monthly Revenue Trend ($M)</div>
            <canvas id="monthlyRev" height="180"></canvas>
        </div>
        <div class="box">
            <div class="box-title">Revenue by Category</div>
            <canvas id="catPie" height="180"></canvas>
        </div>
    </div>

    <div class="row row-eq">
        <div class="box">
            <div class="box-title">Order Status</div>
            <canvas id="statusDonut" height="170"></canvas>
        </div>
        <div class="box">
            <div class="box-title">Payment Methods</div>
            <canvas id="paymentBar" height="170"></canvas>
        </div>
    </div>

    <div class="row row-eq">
        <div class="box">
            <div class="box-title">Top 5 Sellers by Revenue</div>
            <table class="dt">
                <thead><tr><th>Seller</th><th>Revenue</th><th>Orders</th><th>Tier</th></tr></thead>
                <tbody>{"".join(f'<tr><td>{sid}</td><td>${rev}M</td><td>{cnt:,}</td><td>{tier}</td></tr>' for sid, rev, cnt, tier in m['top_sellers'])}</tbody>
            </table>
        </div>
        <div class="box">
            <div class="box-title">Category Breakdown</div>
            <table class="dt">
                <thead><tr><th>Category</th><th>Revenue</th><th>Share</th><th>Orders</th></tr></thead>
                <tbody>{"".join(f'<tr><td>{cat}</td><td>${rev/1e6:.0f}M</td><td>{cat_pcts[cat]}%</td><td>{m["cat_count"][cat]:,}</td></tr>' for cat, rev in m['cat_rev'].items())}</tbody>
            </table>
        </div>
    </div>
</div>
<div class="footer">Marketplace Revenue Analytics &middot; SQL &middot; Python &middot; Power BI &middot; DAX &middot; 7 Performance Areas</div>

<script>
const months = {json.dumps([m[-5:] for m in m['months']])};
const C = ['#3b82f6','#10b981','#f59e0b','#ef4444','#8b5cf6','#06b6d4'];

new Chart(document.getElementById('monthlyRev'), {{
    type: 'bar',
    data: {{ labels: months, datasets: [{{ data: {json.dumps(m['monthly_rev'])}, backgroundColor: '#3b82f6', borderRadius: 3 }}] }},
    options: {{ responsive: true, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ ticks: {{ callback: v => '$'+v+'M' }}, grid: {{ color: '#f1f5f9' }} }}, x: {{ grid: {{ display: false }} }} }} }}
}});

new Chart(document.getElementById('catPie'), {{
    type: 'doughnut',
    data: {{ labels: {json.dumps(list(m['cat_rev'].keys()))}, datasets: [{{ data: {json.dumps([round(v/m['total_rev']*100,1) for v in m['cat_rev'].values()])}, backgroundColor: C, borderWidth: 2, borderColor: '#fff' }}] }},
    options: {{ responsive: true, plugins: {{ legend: {{ position: 'right', labels: {{ boxWidth: 10, font: {{ size: 10 }} }} }} }} }}
}});

new Chart(document.getElementById('statusDonut'), {{
    type: 'doughnut',
    data: {{ labels: {json.dumps(list(m['status_counts'].keys()))}, datasets: [{{ data: {json.dumps(list(m['status_counts'].values()))}, backgroundColor: ['#10b981','#f59e0b','#ef4444'], borderWidth: 2, borderColor: '#fff' }}] }},
    options: {{ responsive: true, plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 10, font: {{ size: 10 }} }} }} }} }}
}});

new Chart(document.getElementById('paymentBar'), {{
    type: 'bar',
    data: {{ labels: {json.dumps(list(m['payment_counts'].keys()))}, datasets: [{{ data: {json.dumps(list(m['payment_counts'].values()))}, backgroundColor: C, borderRadius: 3 }}] }},
    options: {{ responsive: true, indexAxis: 'y', plugins: {{ legend: {{ display: false }} }}, scales: {{ x: {{ grid: {{ color: '#f1f5f9' }} }}, y: {{ grid: {{ display: false }} }} }} }}
}});
</script>
</body>
</html>"""


def main():
    OUTPUT.parent.mkdir(exist_ok=True)
    m = compute_metrics()
    html = generate_html(m)
    OUTPUT.write_text(html, encoding="utf-8")
    print(f"Dashboard generated: {OUTPUT}")
    print(f"  Revenue: ${m['total_rev']/1e9:.2f}B | Orders: {m['total_orders']:,} | Buyers: {m['total_buyers']:,}")
    print(f"  Electronics: {m['cat_rev'].get('Electronics',0)/m['total_rev']*100:.1f}%")
    ret = m['status_counts'].get('Returned',0) + m['status_counts'].get('Cancelled',0)
    print(f"  Returns+Cancelled: {ret/m['total_orders']*100:.1f}%")


if __name__ == "__main__":
    main()
