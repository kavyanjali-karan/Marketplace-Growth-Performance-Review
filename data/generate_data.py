import pandas as pd
import numpy as np
from faker import Faker
from pathlib import Path
from datetime import datetime

fake = Faker("en_IN")
np.random.seed(42)

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

N_CUSTOMERS = 10000
N_PRODUCTS = 1000
N_SELLERS = 200
N_ORDERS = 75000

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

# --------------------------------------------------
# FOLDERS
# --------------------------------------------------

BASE_DIR = Path(__file__).parent

RAW_DIR = BASE_DIR / "raw"
CURATED_DIR = BASE_DIR / "curated"
WAREHOUSE_DIR = BASE_DIR / "warehouse"

for d in [RAW_DIR, CURATED_DIR, WAREHOUSE_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# CUSTOMERS
# --------------------------------------------------

print("Generating customers...")

segments = ["Premium", "Standard", "Enterprise"]
segment_probs = [0.25, 0.60, 0.15]

customers = []

for i in range(1, N_CUSTOMERS + 1):
    customers.append({
        "customer_id": f"C{i:06}",
        "customer_name": fake.name(),
        "segment": np.random.choice(segments, p=segment_probs),
        "city": fake.city(),
        "state": fake.state(),
        "country": "India",
        "signup_date": fake.date_between(
            start_date="-3y",
            end_date="today"
        ),
        "status": np.random.choice(
            ["Active", "Inactive"],
            p=[0.92, 0.08]
        ),
        "lifetime_value": round(
            np.random.gamma(4, 2500), 2
        )
    })

customers_df = pd.DataFrame(customers)
customers_df.to_csv(
    RAW_DIR / "customers.csv",
    index=False
)

# --------------------------------------------------
# PRODUCTS
# --------------------------------------------------

print("Generating products...")

categories = {
    "Electronics": [
        "Mobile",
        "Laptop",
        "Audio",
        "TV"
    ],
    "Fashion": [
        "Shoes",
        "Clothing",
        "Accessories"
    ],
    "Home": [
        "Furniture",
        "Kitchen",
        "Decor"
    ],
    "Beauty": [
        "Skincare",
        "Cosmetics"
    ],
    "Sports": [
        "Fitness",
        "Outdoor"
    ],
    "Books": [
        "Education",
        "Fiction"
    ]
}

brands = [
    "Apple",
    "Samsung",
    "Nike",
    "Sony",
    "LG",
    "Boat",
    "Puma",
    "Dell",
    "HP",
    "Philips"
]

products = []

for i in range(1, N_PRODUCTS + 1):

    category = np.random.choice(
        list(categories.keys()),
        p=[0.45,0.25,0.12,0.08,0.06,0.04]
    )

    subcategory = np.random.choice(
        categories[category]
    )

    price = round(
        np.random.uniform(300, 100000),
        2
    )

    cost = round(
        price * np.random.uniform(0.55,0.80),
        2
    )

    products.append({
        "product_id": f"P{i:05}",
        "product_name": f"{subcategory}_{i}",
        "category": category,
        "subcategory": subcategory,
        "brand": np.random.choice(brands),
        "unit_price": price,
        "cost_price": cost
    })

products_df = pd.DataFrame(products)
products_df.to_csv(
    RAW_DIR / "products.csv",
    index=False
)

# --------------------------------------------------
# SELLERS
# --------------------------------------------------

print("Generating sellers...")

tiers = ["Gold","Silver","Bronze"]
tier_probs = [0.20,0.50,0.30]

regions = [
    "North",
    "South",
    "East",
    "West"
]

sellers = []

for i in range(1, N_SELLERS + 1):

    sellers.append({
        "seller_id": f"S{i:05}",
        "seller_name": f"{fake.company()}",
        "tier": np.random.choice(
            tiers,
            p=tier_probs
        ),
        "region": np.random.choice(regions),
        "rating": round(
            np.random.uniform(3.5,5.0),
            1
        ),
        "join_date": fake.date_between(
            start_date="-5y",
            end_date="-30d"
        )
    })

sellers_df = pd.DataFrame(sellers)

sellers_df.to_csv(
    RAW_DIR / "sellers.csv",
    index=False
)

# --------------------------------------------------
# DATE DIMENSION
# --------------------------------------------------

print("Generating date dimension...")

dates = pd.date_range(
    START_DATE,
    END_DATE,
    freq="D"
)

date_df = pd.DataFrame({
    "date": dates
})

date_df["date_key"] = (
    date_df["date"]
    .dt.strftime("%Y%m%d")
    .astype(int)
)

date_df["year"] = date_df["date"].dt.year
date_df["quarter"] = date_df["date"].dt.quarter
date_df["month"] = date_df["date"].dt.month
date_df["month_name"] = date_df["date"].dt.month_name()
date_df["week"] = date_df["date"].dt.isocalendar().week
date_df["day"] = date_df["date"].dt.day

date_df.to_csv(
    CURATED_DIR / "dim_date.csv",
    index=False
)

# --------------------------------------------------
# ORDERS
# --------------------------------------------------

print("Generating orders...")

order_dates = np.random.choice(
    dates,
    N_ORDERS
)

statuses = [
    "Delivered",
    "Cancelled",
    "Returned"
]

status_probs = [
    0.92,
    0.03,
    0.05
]

orders = []

for i in range(1, N_ORDERS + 1):

    product = products_df.sample(1).iloc[0]

    quantity = np.random.randint(1,4)

    revenue = round(
        product["unit_price"] * quantity,
        2
    )

    discount = round(
        revenue *
        np.random.uniform(0,0.15),
        2
    )

    shipping = round(
        np.random.uniform(50,300),
        2
    )

    profit = round(
        (
            revenue
            - discount
            - (product["cost_price"] * quantity)
            - shipping
        ),
        2
    )

    orders.append({
        "order_id": f"O{i:07}",
        "order_date": order_dates[i-1],
        "customer_id":
            customers_df.sample(1).iloc[0]["customer_id"],
        "product_id":
            product["product_id"],
        "seller_id":
            sellers_df.sample(1).iloc[0]["seller_id"],
        "quantity": quantity,
        "revenue": revenue,
        "discount": discount,
        "shipping_cost": shipping,
        "profit": profit,
        "order_status":
            np.random.choice(
                statuses,
                p=status_probs
            ),
        "payment_method":
            np.random.choice([
                "UPI",
                "Credit Card",
                "Debit Card",
                "Net Banking",
                "Wallet"
            ])
    })

orders_df = pd.DataFrame(orders)

orders_df.to_csv(
    RAW_DIR / "orders.csv",
    index=False
)

# --------------------------------------------------
# PAYMENTS
# --------------------------------------------------

print("Generating payments...")

payments = orders_df[
    [
        "order_id",
        "order_date",
        "payment_method",
        "revenue"
    ]
].copy()

payments["payment_id"] = [
    f"PAY{i:07}"
    for i in range(1,len(payments)+1)
]

payments["payment_status"] = np.random.choice(
    ["Success","Failed"],
    len(payments),
    p=[0.98,0.02]
)

payments.rename(
    columns={
        "order_date":"payment_date",
        "revenue":"amount"
    },
    inplace=True
)

payments.to_csv(
    RAW_DIR / "payments.csv",
    index=False
)

# --------------------------------------------------
# DIMENSIONS
# --------------------------------------------------

print("Creating dimensions...")

dim_customer = customers_df.copy()
dim_customer.insert(
    0,
    "customer_key",
    range(1,len(dim_customer)+1)
)

dim_customer.to_csv(
    CURATED_DIR / "dim_customer.csv",
    index=False
)

dim_product = products_df.copy()
dim_product.insert(
    0,
    "product_key",
    range(1,len(dim_product)+1)
)

dim_product.to_csv(
    CURATED_DIR / "dim_product.csv",
    index=False
)

dim_seller = sellers_df.copy()
dim_seller.insert(
    0,
    "seller_key",
    range(1,len(dim_seller)+1)
)

dim_seller.to_csv(
    CURATED_DIR / "dim_seller.csv",
    index=False
)

# --------------------------------------------------
# FACT TABLE
# --------------------------------------------------

print("Creating fact table...")

customer_lookup = dict(
    zip(
        dim_customer.customer_id,
        dim_customer.customer_key
    )
)

product_lookup = dict(
    zip(
        dim_product.product_id,
        dim_product.product_key
    )
)

seller_lookup = dict(
    zip(
        dim_seller.seller_id,
        dim_seller.seller_key
    )
)

fact_orders = orders_df.copy()

fact_orders["customer_key"] = (
    fact_orders["customer_id"]
    .map(customer_lookup)
)

fact_orders["product_key"] = (
    fact_orders["product_id"]
    .map(product_lookup)
)

fact_orders["seller_key"] = (
    fact_orders["seller_id"]
    .map(seller_lookup)
)

fact_orders["date_key"] = pd.to_datetime(
    fact_orders["order_date"]
).dt.strftime("%Y%m%d").astype(int)

fact_orders.insert(
    0,
    "order_key",
    range(1,len(fact_orders)+1)
)

fact_orders.to_csv(
    CURATED_DIR / "fact_orders.csv",
    index=False
)

# --------------------------------------------------
# TARGETS
# --------------------------------------------------

print("Creating warehouse files...")

months = pd.date_range(
    START_DATE,
    END_DATE,
    freq="MS"
)

marketplace_targets = pd.DataFrame({
    "month":
        months.strftime("%Y-%m"),
    "revenue_target":
        np.random.randint(
            12000000,
            18000000,
            len(months)
        ),
    "profit_target":
        np.random.randint(
            2000000,
            3500000,
            len(months)
        ),
    "customer_target":
        np.random.randint(
            7000,
            12000,
            len(months)
        )
})

marketplace_targets.to_csv(
    WAREHOUSE_DIR /
    "marketplace_targets.csv",
    index=False
)

seller_targets = pd.DataFrame({
    "seller_tier":
        ["Gold","Silver","Bronze"],
    "revenue_target":
        [8000000,5000000,2000000]
})

seller_targets.to_csv(
    WAREHOUSE_DIR /
    "seller_targets.csv",
    index=False
)

category_targets = pd.DataFrame({
    "category":
        list(categories.keys()),
    "revenue_target":
        [
            5400000,
            3000000,
            1400000,
            1000000,
            700000,
            500000
        ]
})

category_targets.to_csv(
    WAREHOUSE_DIR /
    "category_targets.csv",
    index=False
)

calendar = pd.DataFrame({
    "event_date":[
        "2024-01-26",
        "2024-08-15",
        "2024-11-01",
        "2025-01-26",
        "2025-08-15",
        "2025-11-01"
    ],
    "event_name":[
        "Republic Day Sale",
        "Independence Day Sale",
        "Diwali Sale",
        "Republic Day Sale",
        "Independence Day Sale",
        "Diwali Sale"
    ],
    "event_type":"Promotion"
})

calendar.to_csv(
    WAREHOUSE_DIR /
    "marketplace_calendar.csv",
    index=False
)

print("DONE")
print("Files generated successfully.")