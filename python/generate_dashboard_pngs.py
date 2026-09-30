"""
Generate Power BI-style dashboard visuals from marketplace data.

Reads raw and curated CSVs, computes real metrics, and produces
high-resolution PNG dashboards with a dark theme.

Usage: python python/generate_dashboard_pngs.py
Output: assets/*.png (5 dashboards)
"""

import matplotlib
matplotlib.use("Agg")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

# Paths
BASE = Path(__file__).resolve().parents[1]
RAW = BASE / "data" / "raw"
CURATED = BASE / "data" / "curated"
ASSETS = BASE / "assets"
ASSETS.mkdir(exist_ok=True)

# Load data
orders = pd.read_csv(RAW / "orders.csv")
customers = pd.read_csv(CURATED / "dim_customer.csv")
products = pd.read_csv(CURATED / "dim_product.csv")
sellers = pd.read_csv(CURATED / "dim_seller.csv")

# Merge
orders = orders.merge(products[["product_id", "category", "subcategory"]], on="product_id", how="left")
orders = orders.merge(customers[["customer_id", "segment"]], on="customer_id", how="left")
orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["month"] = orders["order_date"].dt.to_period("M").astype(str)

# Aggregates
total_rev = orders["revenue"].sum()
total_orders = len(orders)
total_profit = orders["profit"].sum()
unique_buyers = orders["customer_id"].nunique()

# By category
cat_rev = orders.groupby("category")["revenue"].sum().sort_values(ascending=True)
cat_orders = orders.groupby("category")["order_id"].count().sort_values(ascending=True)

# By segment
seg_rev = orders.groupby("segment")["revenue"].sum().sort_values(ascending=True)

# Order status
status_counts = orders["order_status"].value_counts()

# Monthly trend
monthly = orders.groupby("month").agg(
    revenue=("revenue", "sum"),
    orders=("order_id", "count"),
    profit=("profit", "sum"),
).reset_index().sort_values("month")

# Seller performance
seller_perf = orders.groupby("seller_id").agg(
    revenue=("revenue", "sum"),
    orders=("order_id", "count"),
    profit=("profit", "sum"),
).reset_index()
seller_perf = seller_perf.merge(sellers[["seller_id", "seller_name", "tier", "rating"]], on="seller_id", how="left")

# Theme
BG = "#1F1509"
CARD_BG = "#2C1F10"
TEXT = "#F5EDE2"
MUTED = "#B39B7E"
ACCENT1 = "#FF9F1C"
ACCENT2 = "#FF6B35"
ACCENT3 = "#FFD166"
ACCENT4 = "#06D6A0"
ACCENT5 = "#EF476F"
GRID = "#4A351B"
PALETTE = [ACCENT1, ACCENT2, ACCENT3, ACCENT4, ACCENT5, "#F4A261", "#E76F51", "#2A9D8F"]


def style_ax(ax, title="", xlabel="", ylabel=""):
    ax.set_facecolor(CARD_BG)
    ax.set_title(title, color=TEXT, fontsize=14, fontweight="bold", pad=10, loc="left")
    ax.set_xlabel(xlabel, color=MUTED, fontsize=9)
    ax.set_ylabel(ylabel, color=MUTED, fontsize=9)
    ax.tick_params(colors=MUTED, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.grid(axis="y", color=GRID, linewidth=0.5, alpha=0.5)


def fmt_k(x, _=None):
    if abs(x) >= 1_000_000_000:
        return f"${x/1_000_000_000:.1f}B"
    if abs(x) >= 1_000_000:
        return f"${x/1_000_000:.1f}M"
    if abs(x) >= 1_000:
        return f"${x/1_000:.0f}K"
    return f"${x:.0f}"


# Dashboard 1 - Market Overview
def create_market_overview():
    fig = plt.figure(figsize=(20, 12), facecolor=BG)
    fig.suptitle("Marketplace Overview", color=TEXT, fontsize=20, fontweight="bold", y=0.97, x=0.04, ha="left")
    fig.text(0.04, 0.945, f"75,000 orders  |  10,000 buyers  |  ${total_rev/1e9:.1f}B revenue  |  {len(orders['seller_id'].unique())} sellers",
             color=MUTED, fontsize=10, ha="left")

    # KPI cards
    card_data = [
        ("Total Revenue", f"${total_rev/1e9:.1f}B", f"Profit: ${total_profit/1e9:.1f}B", ACCENT1),
        ("Orders", f"{total_orders:,}", f"Delivered: {status_counts.get('Delivered', 0):,}", ACCENT4),
        ("Buyers", f"{unique_buyers:,}", f"Avg order: ${total_rev/total_orders:,.0f}", ACCENT2),
        ("Returns", f"{status_counts.get('Returned', 0):,}", f"{status_counts.get('Returned', 0)/total_orders*100:.1f}% rate", ACCENT5),
        ("Cancellations", f"{status_counts.get('Cancelled', 0):,}", f"{status_counts.get('Cancelled', 0)/total_orders*100:.1f}% rate", ACCENT3),
    ]

    for i, (label, value, sub, color) in enumerate(card_data):
        x = 0.04 + i * 0.19
        rect = FancyBboxPatch((x, 0.87), 0.17, 0.055, boxstyle="round,pad=0.008",
                              facecolor=CARD_BG, edgecolor=color, linewidth=1.5, transform=fig.transFigure)
        fig.patches.append(rect)
        fig.text(x + 0.085, 0.912, value, color=color, fontsize=18, fontweight="bold", ha="center", va="center")
        fig.text(x + 0.085, 0.895, label, color=MUTED, fontsize=9, ha="center", va="center")
        fig.text(x + 0.085, 0.878, sub, color=MUTED, fontsize=8, ha="center", va="center")

    # Revenue by category
    ax1 = fig.add_axes([0.04, 0.52, 0.44, 0.35])
    style_ax(ax1, "Revenue by Category")
    bars = ax1.barh(cat_rev.index, cat_rev.values, color=PALETTE[:len(cat_rev)], height=0.6)
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    for bar, val in zip(bars, cat_rev.values):
        ax1.text(val + total_rev * 0.01, bar.get_y() + bar.get_height()/2,
                 f"{fmt_k(val)} ({val/total_rev*100:.1f}%)", color=TEXT, fontsize=8, va="center")

    # Order status
    ax2 = fig.add_axes([0.52, 0.52, 0.44, 0.35])
    style_ax(ax2, "Order Status Distribution")
    status_colors = {"Delivered": ACCENT4, "Returned": ACCENT5, "Cancelled": ACCENT3}
    bars = ax2.bar(status_counts.index, status_counts.values,
                   color=[status_colors.get(s, MUTED) for s in status_counts.index], width=0.55)
    for bar, val in zip(bars, status_counts.values):
        ax2.text(bar.get_x() + bar.get_width()/2, val + 500, f"{val:,}\n({val/total_orders*100:.1f}%)",
                 color=TEXT, fontsize=9, ha="center")

    # Monthly revenue trend
    ax3 = fig.add_axes([0.04, 0.06, 0.92, 0.35])
    style_ax(ax3, "Monthly Revenue Trend", ylabel="Revenue")
    ax3.fill_between(range(len(monthly)), monthly["revenue"], alpha=0.15, color=ACCENT1)
    ax3.plot(range(len(monthly)), monthly["revenue"], color=ACCENT1, linewidth=2)
    ax3.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    ax3.set_xticks(range(0, len(monthly), 3))
    ax3.set_xticklabels([monthly["month"].iloc[i] for i in range(0, len(monthly), 3)], rotation=0, fontsize=7)

    fig.savefig(ASSETS / "market_overview.png", dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print("OK market_overview.png")


# Dashboard 2 - Order Trends
def create_order_trends():
    fig = plt.figure(figsize=(20, 12), facecolor=BG)
    fig.suptitle("Order Trends", color=TEXT, fontsize=20, fontweight="bold", y=0.97, x=0.04, ha="left")
    fig.text(0.04, 0.945, f"75,000 orders  |  Monthly volume and revenue trends  |  Category breakdown",
             color=MUTED, fontsize=10, ha="left")

    # Monthly orders
    ax1 = fig.add_axes([0.04, 0.52, 0.44, 0.38])
    style_ax(ax1, "Monthly Order Volume")
    ax1.fill_between(range(len(monthly)), monthly["orders"], alpha=0.15, color=ACCENT2)
    ax1.plot(range(len(monthly)), monthly["orders"], color=ACCENT2, linewidth=2)
    ax1.set_xticks(range(0, len(monthly), 3))
    ax1.set_xticklabels([monthly["month"].iloc[i] for i in range(0, len(monthly), 3)], rotation=0, fontsize=7)

    # Monthly revenue
    ax2 = fig.add_axes([0.52, 0.52, 0.44, 0.38])
    style_ax(ax2, "Monthly Revenue", ylabel="Revenue")
    ax2.fill_between(range(len(monthly)), monthly["revenue"], alpha=0.15, color=ACCENT1)
    ax2.plot(range(len(monthly)), monthly["revenue"], color=ACCENT1, linewidth=2)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    ax2.set_xticks(range(0, len(monthly), 3))
    ax2.set_xticklabels([monthly["month"].iloc[i] for i in range(0, len(monthly), 3)], rotation=0, fontsize=7)

    # Orders by category
    ax3 = fig.add_axes([0.04, 0.06, 0.44, 0.38])
    style_ax(ax3, "Orders by Category")
    bars = ax3.barh(cat_orders.index, cat_orders.values, color=PALETTE[:len(cat_orders)], height=0.6)
    for bar, val in zip(bars, cat_orders.values):
        ax3.text(val + 200, bar.get_y() + bar.get_height()/2, f"{val:,}", color=TEXT, fontsize=8, va="center")

    # Revenue by segment
    ax4 = fig.add_axes([0.52, 0.06, 0.44, 0.38])
    style_ax(ax4, "Revenue by Customer Segment")
    bars = ax4.barh(seg_rev.index, seg_rev.values, color=PALETTE[:len(seg_rev)], height=0.55)
    ax4.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    for bar, val in zip(bars, seg_rev.values):
        ax4.text(val + total_rev * 0.01, bar.get_y() + bar.get_height()/2,
                 fmt_k(val), color=TEXT, fontsize=8, va="center")

    fig.savefig(ASSETS / "order_trends.png", dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print("OK order_trends.png")


# Dashboard 3 - Product Analysis
def create_product_analysis():
    fig = plt.figure(figsize=(20, 12), facecolor=BG)
    fig.suptitle("Product Analysis", color=TEXT, fontsize=20, fontweight="bold", y=0.97, x=0.04, ha="left")
    fig.text(0.04, 0.945, f"{len(products)} products  |  {len(cat_rev)} categories  |  Revenue and volume analysis",
             color=MUTED, fontsize=10, ha="left")

    # Revenue by category (pie)
    ax1 = fig.add_axes([0.04, 0.52, 0.25, 0.38])
    style_ax(ax1, "Revenue Share")
    colors = PALETTE[:len(cat_rev)]
    wedges, texts, autotexts = ax1.pie(cat_rev.values, labels=cat_rev.index,
                                        colors=colors, autopct="%1.1f%%",
                                        textprops={"color": TEXT, "fontsize": 8},
                                        pctdistance=0.75, startangle=90)
    for at in autotexts:
        at.set_fontsize(7)

    # Top subcategories
    ax2 = fig.add_axes([0.32, 0.52, 0.64, 0.38])
    style_ax(ax2, "Revenue by Subcategory")
    sub_rev = orders.groupby("subcategory")["revenue"].sum().sort_values(ascending=True).tail(10)
    bars = ax2.barh(sub_rev.index, sub_rev.values, color=PALETTE[:len(sub_rev)], height=0.6)
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    for bar, val in zip(bars, sub_rev.values):
        ax2.text(val + total_rev * 0.005, bar.get_y() + bar.get_height()/2,
                 fmt_k(val), color=TEXT, fontsize=8, va="center")

    # Category by order count
    ax3 = fig.add_axes([0.04, 0.06, 0.44, 0.38])
    style_ax(ax3, "Order Volume by Category")
    cat_order_counts = orders["category"].value_counts().sort_values(ascending=True)
    bars = ax3.barh(cat_order_counts.index, cat_order_counts.values, color=PALETTE[:len(cat_order_counts)], height=0.6)
    for bar, val in zip(bars, cat_order_counts.values):
        ax3.text(val + 200, bar.get_y() + bar.get_height()/2, f"{val:,}", color=TEXT, fontsize=8, va="center")

    # Avg order value by category
    ax4 = fig.add_axes([0.52, 0.06, 0.44, 0.38])
    style_ax(ax4, "Avg Order Value by Category", ylabel="AOV ($)")
    cat_aov = orders.groupby("category")["revenue"].mean().sort_values(ascending=True)
    bars = ax4.barh(cat_aov.index, cat_aov.values, color=PALETTE[:len(cat_aov)], height=0.6)
    ax4.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    for bar, val in zip(bars, cat_aov.values):
        ax4.text(val + cat_aov.max() * 0.02, bar.get_y() + bar.get_height()/2,
                 fmt_k(val), color=TEXT, fontsize=8, va="center")

    fig.savefig(ASSETS / "product_analysis.png", dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print("OK product_analysis.png")


# Dashboard 4 - Seller Performance
def create_seller_performance():
    fig = plt.figure(figsize=(20, 12), facecolor=BG)
    fig.suptitle("Seller Performance", color=TEXT, fontsize=20, fontweight="bold", y=0.97, x=0.04, ha="left")
    fig.text(0.04, 0.945, f"{len(sellers)} sellers  |  Revenue, order volume, and rating analysis",
             color=MUTED, fontsize=10, ha="left")

    # Top sellers by revenue
    ax1 = fig.add_axes([0.04, 0.52, 0.44, 0.38])
    style_ax(ax1, "Top 10 Sellers by Revenue")
    top_sellers = seller_perf.nlargest(10, "revenue")
    bars = ax1.barh(top_sellers["seller_name"], top_sellers["revenue"], color=PALETTE[:10], height=0.6)
    ax1.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    for bar, val in zip(bars, top_sellers["revenue"]):
        ax1.text(val + seller_perf["revenue"].max() * 0.02, bar.get_y() + bar.get_height()/2,
                 fmt_k(val), color=TEXT, fontsize=8, va="center")

    # Seller tiers
    ax2 = fig.add_axes([0.52, 0.52, 0.44, 0.38])
    style_ax(ax2, "Revenue by Seller Tier")
    tier_rev = seller_perf.groupby("tier")["revenue"].sum().sort_values(ascending=True)
    bars = ax2.barh(tier_rev.index, tier_rev.values, color=PALETTE[:len(tier_rev)], height=0.55)
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    for bar, val in zip(bars, tier_rev.values):
        ax2.text(val + tier_rev.max() * 0.02, bar.get_y() + bar.get_height()/2,
                 fmt_k(val), color=TEXT, fontsize=8, va="center")

    # Orders by seller
    ax3 = fig.add_axes([0.04, 0.06, 0.44, 0.38])
    style_ax(ax3, "Order Volume by Seller Tier")
    tier_orders = seller_perf.groupby("tier")["orders"].sum().sort_values(ascending=True)
    bars = ax3.barh(tier_orders.index, tier_orders.values, color=PALETTE[:len(tier_orders)], height=0.55)
    for bar, val in zip(bars, tier_orders.values):
        ax3.text(val + 100, bar.get_y() + bar.get_height()/2, f"{val:,}", color=TEXT, fontsize=8, va="center")

    # Rating distribution
    ax4 = fig.add_axes([0.52, 0.06, 0.44, 0.38])
    style_ax(ax4, "Seller Rating Distribution", xlabel="Rating")
    ax4.hist(seller_perf["rating"], bins=20, color=ACCENT5, alpha=0.7, edgecolor=CARD_BG, linewidth=0.5)
    ax4.axvline(x=seller_perf["rating"].mean(), color=ACCENT1, linestyle="--", linewidth=1.5,
                label=f'Mean: {seller_perf["rating"].mean():.2f}')
    ax4.legend(fontsize=8, loc="upper left", framealpha=0.3, facecolor=CARD_BG, edgecolor=GRID, labelcolor=TEXT)

    fig.savefig(ASSETS / "seller_performance.png", dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print("OK seller_performance.png")


# Dashboard 5 - Customer Analysis
def create_customer_analysis():
    fig = plt.figure(figsize=(20, 12), facecolor=BG)
    fig.suptitle("Customer Analysis", color=TEXT, fontsize=20, fontweight="bold", y=0.97, x=0.04, ha="left")
    fig.text(0.04, 0.945, f"10,000 unique buyers  |  Segment and behavior analysis",
             color=MUTED, fontsize=10, ha="left")

    # Customers by segment
    ax1 = fig.add_axes([0.04, 0.52, 0.25, 0.38])
    style_ax(ax1, "Customers by Segment")
    seg_counts = customers["segment"].value_counts()
    colors = PALETTE[:len(seg_counts)]
    wedges, texts, autotexts = ax1.pie(seg_counts.values, labels=seg_counts.index,
                                        colors=colors, autopct="%1.0f%%",
                                        textprops={"color": TEXT, "fontsize": 9},
                                        pctdistance=0.75, startangle=90)

    # Revenue by segment
    ax2 = fig.add_axes([0.32, 0.52, 0.64, 0.38])
    style_ax(ax2, "Revenue by Customer Segment")
    bars = ax2.barh(seg_rev.index, seg_rev.values, color=PALETTE[:len(seg_rev)], height=0.55)
    ax2.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    for bar, val in zip(bars, seg_rev.values):
        ax2.text(val + total_rev * 0.01, bar.get_y() + bar.get_height()/2,
                 f"{fmt_k(val)} ({val/total_rev*100:.1f}%)", color=TEXT, fontsize=8, va="center")

    # Top customers
    ax3 = fig.add_axes([0.04, 0.06, 0.44, 0.38])
    style_ax(ax3, "Top 10 Customers by Revenue")
    cust_rev = orders.groupby("customer_id")["revenue"].sum().nlargest(10).reset_index()
    cust_rev = cust_rev.merge(customers[["customer_id", "customer_name"]], on="customer_id", how="left")
    bars = ax3.barh(cust_rev["customer_name"], cust_rev["revenue"], color=PALETTE[:10], height=0.6)
    ax3.xaxis.set_major_formatter(mticker.FuncFormatter(fmt_k))
    for bar, val in zip(bars, cust_rev["revenue"]):
        ax3.text(val + cust_rev["revenue"].max() * 0.02, bar.get_y() + bar.get_height()/2,
                 fmt_k(val), color=TEXT, fontsize=8, va="center")

    # Payment methods
    ax4 = fig.add_axes([0.52, 0.06, 0.44, 0.38])
    style_ax(ax4, "Orders by Payment Method")
    payments = orders["payment_method"].value_counts()
    bars = ax4.bar(payments.index, payments.values, color=PALETTE[:len(payments)], width=0.55)
    for bar, val in zip(bars, payments.values):
        ax4.text(bar.get_x() + bar.get_width()/2, val + 200, f"{val:,}", color=TEXT, fontsize=9, ha="center")

    fig.savefig(ASSETS / "customer_analysis.png", dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.3)
    plt.close(fig)
    print("OK customer_analysis.png")


if __name__ == "__main__":
    print("Generating marketplace dashboards...")
    create_market_overview()
    create_order_trends()
    create_product_analysis()
    create_seller_performance()
    create_customer_analysis()
    print(f"\nAll dashboards saved to {ASSETS}/")
