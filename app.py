"""Interactive Streamlit dashboard for the fictional retail sales dataset."""
from pathlib import Path
import sqlite3
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "sales.csv"
DB_PATH = BASE_DIR / "sales.db"

st.set_page_config(page_title="Retail Sales Dashboard", page_icon="📊", layout="wide")
st.title("📊 Retail Sales Analysis Dashboard")
st.caption("Portfolio project • Python + SQL + Pandas + Streamlit • Fictional sample data")

@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH, parse_dates=["order_date"])
    # SQL database is also provided so learners can practice database queries.
    with sqlite3.connect(DB_PATH) as conn:
        try:
            db_count = pd.read_sql_query("SELECT COUNT(*) AS n FROM sales", conn).iloc[0, 0]
        except Exception:
            db_count = None
    return df, db_count

df, db_count = load_data()

st.sidebar.header("Filters")
min_date, max_date = df["order_date"].min().date(), df["order_date"].max().date()
date_range = st.sidebar.date_input("Order date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)
categories = sorted(df["category"].dropna().unique().tolist())
selected_categories = st.sidebar.multiselect("Category", categories, default=categories)
products = sorted(df[df["category"].isin(selected_categories)]["product"].dropna().unique().tolist())
selected_products = st.sidebar.multiselect("Product", products, default=products)

filtered = df.copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[filtered["order_date"].dt.date.between(date_range[0], date_range[1])]
if selected_categories:
    filtered = filtered[filtered["category"].isin(selected_categories)]
else:
    filtered = filtered.iloc[0:0]
if selected_products:
    filtered = filtered[filtered["product"].isin(selected_products)]
else:
    filtered = filtered.iloc[0:0]

orders = filtered["order_id"].nunique()
units = int(filtered["quantity"].sum()) if not filtered.empty else 0
revenue = float(filtered["revenue"].sum()) if not filtered.empty else 0.0
avg_order = revenue / orders if orders else 0.0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Orders", f"{orders:,}")
k2.metric("Units sold", f"{units:,}")
k3.metric("Total revenue", f"₹{revenue:,.0f}")
k4.metric("Average revenue / order", f"₹{avg_order:,.0f}")

left, right = st.columns(2)
with left:
    st.subheader("Revenue by category")
    by_category = filtered.groupby("category", as_index=False)["revenue"].sum().sort_values("revenue", ascending=False)
    if by_category.empty:
        st.info("No rows match the selected filters.")
    else:
        st.bar_chart(by_category.set_index("category")["revenue"])
with right:
    st.subheader("Monthly revenue")
    monthly = filtered.assign(month=filtered["order_date"].dt.to_period("M").astype(str)).groupby("month", as_index=False)["revenue"].sum().sort_values("month")
    if monthly.empty:
        st.info("No rows match the selected filters.")
    else:
        st.line_chart(monthly.set_index("month")["revenue"])

st.subheader("Product performance")
by_product = filtered.groupby("product", as_index=False).agg(units_sold=("quantity", "sum"), revenue=("revenue", "sum")).sort_values("revenue", ascending=False)
st.dataframe(by_product, use_container_width=True, hide_index=True)

st.subheader("Filtered order records")
st.dataframe(filtered.sort_values("order_date", ascending=False), use_container_width=True, hide_index=True)

if not by_category.empty and not by_product.empty:
    top_category = by_category.iloc[0]
    top_product = by_product.iloc[0]
    st.subheader("Quick insights")
    st.write(f"- Highest-revenue category in this selection: **{top_category['category']}** (₹{top_category['revenue']:,.0f}).")
    st.write(f"- Highest-revenue product in this selection: **{top_product['product']}** (₹{top_product['revenue']:,.0f}).")
st.caption("Note: this is a small fictional practice dataset. Revenue is not profit; costs and returns are not included.")
