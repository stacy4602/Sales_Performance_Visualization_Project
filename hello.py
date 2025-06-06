import pandas as pd
import plotly.express as px
import preswald

# ------------------ Load Dataset ------------------
df = pd.read_csv('data/sales_data_sample.csv')
df["ORDERDATE"] = pd.to_datetime(df["ORDERDATE"])
df["SALES"] = pd.to_numeric(df["SALES"], errors="coerce")

# ------------------ Task 2: Query or Manipulate Data ------------------

# Filter orders where sales > 2000
filtered_orders = df.query('SALES > 1000')[["ORDERNUMBER","QUANTITYORDERED", "COUNTRY", "SALES"]]


# Monthly Revenue Trend
monthly_sales = df.groupby(df["ORDERDATE"].dt.to_period("M"))["SALES"].sum().reset_index()
monthly_sales["ORDERDATE"] = monthly_sales["ORDERDATE"].astype(str)

# Revenue by Country
country_sales = df.groupby("COUNTRY")["SALES"].sum().reset_index()

# Product Line Revenue Treemap
product_treemap = df.groupby(["COUNTRY", "PRODUCTLINE"])["SALES"].sum().reset_index()

# Order Status Distribution
status_counts = df["STATUS"].value_counts().reset_index()
status_counts.columns = ["STATUS", "count"]

# Top 10 Customers by Revenue
top_customers = df.groupby("CUSTOMERNAME")["SALES"].sum().nlargest(10).reset_index()

# ------------------ Task 4: Create Visualizations ------------------

line_plot = px.line(
    monthly_sales,
    x="ORDERDATE",
    y="SALES",
    title="Monthly Sales Trend",
    markers=True,
)

bar_plot = px.bar(
    country_sales.sort_values("SALES", ascending=False),
    x="COUNTRY",
    y="SALES",
    title="Revenue by Country"
)

treemap = px.treemap(
    product_treemap,
    path=["COUNTRY", "PRODUCTLINE"],
    values="SALES",
    color="SALES",
    title="Revenue Distribution by Country and Product Line"
)

pie_chart = px.pie(
    status_counts,
    names="STATUS",
    values="count",
    title="Order Status Distribution"
)

customer_bar = px.bar(
    top_customers,
    x="CUSTOMERNAME",
    y="SALES",
    title="Top 10 Customers by Revenue"
)

scatter_plot = px.scatter(
    df,
    x="QUANTITYORDERED",
    y="SALES",
    color="STATUS",
    hover_data=["PRODUCTLINE", "CUSTOMERNAME"],
    title="Sales vs Quantity Ordered by Order Status"
)



# ------------------ Task 3: Build Interactive UI ------------------

preswald.text("# 📊 Sales Performance Dashboard")

preswald.text("## 🔍  Filter Orders > $2000")
preswald.text("A preview of all sales transactions with revenue greater than $2000.")
preswald.table(filtered_orders, title="High-Value Orders (SALES > $2000)")

preswald.text("# 📊 Visualizations")

preswald.text("## 📈 1.Sales vs Quantity Scatter Plot")
preswald.text("This scatter plot helps identify patterns between how much was ordered and the total sales, grouped by order status. It can reveal high-revenue, low-quantity VIP orders or bulk buys.")
preswald.plotly(scatter_plot)

preswald.text("## 📅 2. Monthly Sales Trend")
preswald.text("This line chart shows how total revenue has evolved over each month. Peaks may indicate seasonal demand or promotional campaigns.")
preswald.plotly(line_plot)

preswald.text("## 🌍 3.Revenue by Country")
preswald.text("A bar chart displaying country-wise sales volume. Use it to identify top-performing regions.")
preswald.plotly(bar_plot)

preswald.text("## 🧭 4. Product Line Revenue Treemap")
preswald.text("This hierarchical treemap breaks down revenue contribution by product line within each country.")
preswald.plotly(treemap)

preswald.text("## 📌 5.Order Status Distribution")
preswald.text("A pie chart representing how many orders fall under each status—Shipped, On Hold, Cancelled, etc.")
preswald.plotly(pie_chart)

preswald.text("## 🏆 6. Top Customers by Revenue")
preswald.text("This bar chart highlights the top 10 customers based on their total purchases, useful for client retention targeting.")
preswald.plotly(customer_bar)
