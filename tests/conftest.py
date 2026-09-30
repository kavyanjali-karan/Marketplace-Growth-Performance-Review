"""Shared fixtures for marketplace tests."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest
import pandas as pd

DATA_DIR = ROOT / "data" / "raw"

RAW_FILES = ["orders.csv", "customers.csv", "products.csv", "sellers.csv", "payments.csv"]


def _ensure_data() -> None:
    """Build the (gitignored, seeded) datasets on a fresh clone."""
    if all((DATA_DIR / name).exists() for name in RAW_FILES):
        return
    subprocess.run(
        [sys.executable, str(ROOT / "data" / "generate_data.py")],
        check=True,
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


_ensure_data()


@pytest.fixture(scope="session")
def orders():
    return pd.read_csv(DATA_DIR / "orders.csv")


@pytest.fixture(scope="session")
def customers():
    return pd.read_csv(DATA_DIR / "customers.csv")


@pytest.fixture(scope="session")
def products():
    return pd.read_csv(DATA_DIR / "products.csv")


@pytest.fixture(scope="session")
def sellers():
    return pd.read_csv(DATA_DIR / "sellers.csv")


@pytest.fixture(scope="session")
def payments():
    return pd.read_csv(DATA_DIR / "payments.csv")


@pytest.fixture(scope="session")
def orders_with_category(orders, products):
    return orders.merge(products[["product_id", "category"]], on="product_id", how="left")
