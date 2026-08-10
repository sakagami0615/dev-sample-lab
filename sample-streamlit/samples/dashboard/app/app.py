import streamlit as st

from dashboard_logic import filter_sales, load_sales_data

st.set_page_config(page_title="Sales Dashboard Sample", page_icon="📈", layout="wide")
st.title("Sales Dashboard Sample")

df = load_sales_data()

min_date, max_date = df["date"].min(), df["date"].max()
categories = sorted(df["category"].unique())
regions = sorted(df["region"].unique())

with st.sidebar:
    st.header("Filters")
    date_range = st.date_input(
        "Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date
    )
    selected_categories = st.multiselect("Category", categories, default=categories)
    selected_regions = st.multiselect("Region", regions, default=regions)

if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date

filtered = filter_sales(df, start_date, end_date, selected_categories, selected_regions)

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"¥{filtered['sales'].sum():,.0f}")
col2.metric("Total Profit", f"¥{filtered['profit'].sum():,.0f}")
col3.metric("Transactions", f"{len(filtered):,}")

st.subheader("Sales Trend")
trend = filtered.groupby("date")["sales"].sum()
st.line_chart(trend)

st.subheader("Sales by Category")
by_category = filtered.groupby("category")["sales"].sum()
st.bar_chart(by_category)

st.subheader("Filtered Data")
st.dataframe(filtered, use_container_width=True)
