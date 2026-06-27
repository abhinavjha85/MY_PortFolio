import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="NeuralRetail Dashboard", page_icon="🛍️", layout="wide")
st.title("🛍️ NeuralRetail - AI Sales Intelligence")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/clean_data.csv')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

@st.cache_data
def load_segments():
    return pd.read_csv('data/processed/customer_segments.csv')

df = load_data()
segments = load_segments()

st.subheader("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"£{df['TotalPrice'].sum():,.0f}")
col2.metric("Total Orders", f"{df['InvoiceNo'].nunique():,}")
col3.metric("Total Customers", f"{df['CustomerID'].nunique():,}")
col4.metric("Countries", f"{df['Country'].nunique()}")

st.markdown("---")
st.subheader("📈 Daily Sales Trend")
daily = df.groupby(df['InvoiceDate'].dt.date)['TotalPrice'].sum().reset_index()
fig1 = px.line(daily, x='InvoiceDate', y='TotalPrice', title='Daily Revenue')
st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")
st.subheader("👥 Customer Segments")
col1, col2 = st.columns(2)
seg_counts = segments['Segment'].value_counts().reset_index()
fig2 = px.pie(seg_counts, values='count', names='Segment', title='Customer Distribution')
col1.plotly_chart(fig2)
fig3 = px.scatter(segments, x='Recency', y='Monetary', color='Segment', title='RFM Analysis')
col2.plotly_chart(fig3)

st.markdown("---")
st.subheader("🏆 Top 10 Products")
top_products = df.groupby('Description')['TotalPrice'].sum().nlargest(10).reset_index()
fig4 = px.bar(top_products, x='TotalPrice', y='Description', orientation='h', title='Top Products by Revenue')
st.plotly_chart(fig4, use_container_width=True)

