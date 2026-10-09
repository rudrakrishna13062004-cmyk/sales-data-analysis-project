"""
Retail Sales Analysis — beginner portfolio project.
Run: python main.py
Creates SQLite database, summary CSVs, and charts in outputs/.
"""
from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "sales.csv"
OUTPUTS = ROOT / "outputs"
CHARTS = OUTPUTS / "charts"
DB_PATH = ROOT / "sales.db"

def main():
    OUTPUTS.mkdir(exist_ok=True)
    CHARTS.mkdir(parents=True, exist_ok=True)

    # 1) Load data
    sales = pd.read_csv(DATA)
    print("FIRST 5 ROWS")
    print(sales.head().to_string(index=False))

    # 2) Basic data-quality checks
    sales["order_date"] = pd.to_datetime(sales["order_date"], errors="coerce")
    print("\nDATA QUALITY")
    print("Rows:", len(sales))
    print("Duplicate order IDs:", int(sales["order_id"].duplicated().sum()))
    print("Missing values by column:")
    print(sales.isna().sum().to_string())

    # Remove invalid rows if any, then calculate revenue from source columns.
    sales = sales.dropna(subset=["order_id", "order_date", "product", "category", "quantity", "unit_price"])
    sales = sales[(sales["quantity"] > 0) & (sales["unit_price"] >= 0)]
    sales["revenue"] = sales["quantity"] * sales["unit_price"]
    sales["month"] = sales["order_date"].dt.to_period("M").astype(str)

    # 3) Store cleaned records in SQLite
    db_sales = sales.copy()
    db_sales["order_date"] = db_sales["order_date"].dt.strftime("%Y-%m-%d")
    with sqlite3.connect(DB_PATH) as conn:
        db_sales.to_sql("sales", conn, if_exists="replace", index=False)

        kpis = pd.read_sql_query("""
            SELECT COUNT(*) AS total_orders,
                   SUM(quantity) AS units_sold,
                   ROUND(SUM(revenue), 2) AS total_revenue,
                   ROUND(AVG(revenue), 2) AS average_order_revenue
            FROM sales
        """, conn)
        category = pd.read_sql_query("""
            SELECT category, ROUND(SUM(revenue), 2) AS revenue
            FROM sales GROUP BY category ORDER BY revenue DESC
        """, conn)
        monthly = pd.read_sql_query("""
            SELECT substr(order_date, 1, 7) AS month,
                   ROUND(SUM(revenue), 2) AS revenue
            FROM sales GROUP BY substr(order_date, 1, 7) ORDER BY month
        """, conn)
        products = pd.read_sql_query("""
            SELECT product, SUM(quantity) AS units_sold,
                   ROUND(SUM(revenue), 2) AS revenue
            FROM sales GROUP BY product ORDER BY revenue DESC
        """, conn)

    # 4) Save tables for review
    kpis.to_csv(OUTPUTS / "kpis.csv", index=False)
    category.to_csv(OUTPUTS / "category_revenue.csv", index=False)
    monthly.to_csv(OUTPUTS / "monthly_revenue.csv", index=False)
    products.to_csv(OUTPUTS / "product_performance.csv", index=False)

    # 5) Charts
    plt.figure(figsize=(8, 5))
    plt.bar(category["category"], category["revenue"])
    plt.title("Revenue by Category")
    plt.xlabel("Category")
    plt.ylabel("Revenue (INR)")
    plt.tight_layout()
    plt.savefig(CHARTS / "revenue_by_category.png", dpi=150)
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.plot(monthly["month"], monthly["revenue"], marker="o")
    plt.title("Monthly Revenue")
    plt.xlabel("Month")
    plt.ylabel("Revenue (INR)")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(CHARTS / "monthly_revenue.png", dpi=150)
    plt.close()

    top = products.sort_values("revenue", ascending=True)
    plt.figure(figsize=(8, 5))
    plt.barh(top["product"], top["revenue"])
    plt.title("Product Revenue Comparison")
    plt.xlabel("Revenue (INR)")
    plt.ylabel("Product")
    plt.tight_layout()
    plt.savefig(CHARTS / "product_revenue.png", dpi=150)
    plt.close()

    print("\nKEY PERFORMANCE INDICATORS")
    print(kpis.to_string(index=False))
    print("\nREVENUE BY CATEGORY")
    print(category.to_string(index=False))
    print("\nMONTHLY REVENUE")
    print(monthly.to_string(index=False))
    print("\nPRODUCT PERFORMANCE")
    print(products.to_string(index=False))
    print(f"\nDone. Charts and CSV outputs are saved in: {OUTPUTS}")

if __name__ == "__main__":
    main()
