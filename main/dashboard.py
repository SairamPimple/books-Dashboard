import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path
import os

st.set_page_config(layout="wide", page_title="Books to Scrape Dashboard")

# DATA_PATH = '../data/books_data.csv'
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / 'data' / 'books_data.csv'

# Load data
@st.cache_data
def load_data():
    if os.path.exists(DATA_PATH):
        return pd.read_csv(DATA_PATH)
    else:
        st.error("Data not found. Please run the scraper first.")
        return pd.DataFrame()

df = load_data()

st.title("📚 Books to Scrape - Interactive Dashboard")
st.markdown("Explore book data scraped from [Books to Scrape](http://books.toscrape.com)")

if not df.empty:
    st.sidebar.header("🔍 Filter Options")
    rating_filter = st.sidebar.multiselect("Select Rating", sorted(df['Rating'].unique()), default=df['Rating'].unique())
    price_range = st.sidebar.slider("Price Range (£)", float(df['Price'].min()), float(df['Price'].max()), (float(df['Price'].min()), float(df['Price'].max())))

    filtered_df = df[df['Rating'].isin(rating_filter) & df['Price'].between(*price_range)]

    # 1. Show filtered table (optional toggle)
    with st.expander("📘 Show Filtered Book List"):
        st.dataframe(filtered_df[['Title', 'Price', 'Rating', 'Stock', 'URL']], use_container_width=True)

    # Create columns layout
    col1, col2, col3 = st.columns(3)

    # Pie chart: Rating distribution
    with col1:
        st.subheader("⭐ Rating Distribution (Pie)")
        rating_counts = filtered_df['Rating'].value_counts().reset_index()
        rating_counts.columns = ['Rating', 'Count']
        fig1 = px.pie(rating_counts, names='Rating', values='Count', title='Book Ratings')
        st.plotly_chart(fig1, use_container_width=True)

    # Bar: Top 10 expensive books
    with col3:
        st.subheader("💰 Top 10 Expensive Books")
        top10 = filtered_df.sort_values(by='Price', ascending=False).head(10)
        fig3 = px.bar(top10, x='Price', y='Title', orientation='h', title='Top 10 Expensive Books')
        st.plotly_chart(fig3, use_container_width=True)

    # Second row of charts
    col4, col5 = st.columns(2)

    # Histogram: Price distribution
    with col4:
        st.subheader("📉 Price Histogram")
        fig4 = px.histogram(filtered_df, x='Price', nbins=20, title='Price Distribution')
        st.plotly_chart(fig4, use_container_width=True)

    # Average Price by Rating
    with col5:
        st.subheader("📈 Average Price by Rating")
        avg_price = df.groupby("Rating")["Price"].mean().reset_index()
        fig5 = px.bar(avg_price, x="Rating", y="Price", title="Average Price per Rating")
        st.plotly_chart(fig5, use_container_width=True)