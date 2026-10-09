# Retail Sales Data Analysis (Python + SQL)

## Project overview
This beginner-friendly portfolio project analyzes a **fictional sample** of 15 retail orders from January–March 2026. It includes a Python analysis pipeline, SQLite database + SQL queries, generated charts/CSV reports, and an interactive Streamlit dashboard with filters.

> This is sample data for learning, not real company/customer data. Revenue is sales value, not profit; product cost and expenses are not included.

## Questions answered
- What are total orders, units sold, total revenue, and average order revenue?
- Which category contributes the most revenue?
- How does revenue change month to month?
- Which products contribute the most revenue?

## Tools
- Python 3
- Pandas
- SQLite (`sqlite3`, included with Python)
- SQL: `SUM`, `COUNT`, `AVG`, `GROUP BY`, `ORDER BY`, `HAVING`
- Matplotlib
- Streamlit (interactive dashboard)

## Project structure
```text
sales-data-analysis-project/
├── data/
│   └── sales.csv
├── sql/
│   └── analysis_queries.sql
├── outputs/
│   ├── kpis.csv
│   ├── category_revenue.csv
│   ├── monthly_revenue.csv
│   ├── product_performance.csv
│   └── charts/
├── main.py
├── app.py                 # interactive dashboard
├── sales.db               # SQLite database
├── requirements.txt
└── README.md
```

## Run the project
1. Install Python 3.
2. Open a terminal in this folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run:
   ```bash
   python main.py
   ```
5. Check the generated tables in `outputs/` and charts in `outputs/charts/`. A `sales.db` SQLite database is created automatically.
6. Launch the interactive dashboard:
   ```bash
   streamlit run app.py
   ```
   Streamlit opens a local web dashboard where you can filter by date, category, and product.

## Key results from the sample
- Total orders: **15**
- Units sold: **60**
- Total revenue: **₹37,200**
- Highest-revenue category: **Furniture (₹27,000)**
- Monthly revenue: **January ₹6,300; February ₹9,200; March ₹21,700**
- Highest-revenue product: **Desk (₹15,000)**

## Business insights
1. Furniture leads revenue in this small sample, mainly due to high-priced desks and chairs.
2. March has the highest revenue (₹21,700). This is a pattern in this sample only; more months of data are needed before calling it a stable trend.
3. Desk has the highest product revenue, while Pen sells many units but generates less revenue per unit.
4. Revenue alone does not tell us profitability. Cost, discounts, returns, and operating expenses would be needed for profit analysis.

## SQL examples
See [`sql/analysis_queries.sql`](sql/analysis_queries.sql) for queries covering KPIs, category totals, monthly trends, top products, and `HAVING`.

## Portfolio description
Built a retail sales analysis project using Python, Pandas, SQLite, SQL, and Matplotlib. Cleaned and validated sample order data, calculated revenue KPIs, queried category/month/product performance with SQL, and generated charts with actionable business observations.

## Limitations and next steps
- Small fictional dataset (15 orders), so results are for practice, not market conclusions.
- Add more records and a product-cost field to analyze profit margin.
- Add discount, return, region, and customer fields for deeper segmentation.
- Expand the sample dataset and add product cost, discounts, returns, region, and customer fields for deeper analysis.
