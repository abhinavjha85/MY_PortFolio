import streamlit as st
import pandas as pd
import plotly.express as px
import time
import random

st.set_page_config(page_title="NeuralRetail Dashboard", page_icon="🛍️", layout="wide")

refresh_interval = st.sidebar.slider("Auto-refresh (seconds)", 10, 60, 30)
auto_refresh = st.sidebar.checkbox("Enable Auto-refresh", value=True)
st.sidebar.info(f"🕐 Last Refresh: {time.strftime('%H:%M:%S')}")

st.title("🛍️ NeuralRetail - AI Sales Intelligence")
st.markdown("---")

@st.cache_data(ttl=30)
def load_data():
    df = pd.read_csv('data/processed/clean_data.csv')
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    return df

@st.cache_data(ttl=30)
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

st.markdown("---")
st.subheader("⚡ Live Transactions Feed")

def generate_live_transaction():
    products = ['WHITE HANGING HEART T-LIGHT HOLDER', 'REGENCY CAKESTAND 3 TIER',
                'PAPER CRAFT LITTLE BIRDIE', 'PARTY BUNTING', 'JUMBO BAG RED RETROSPOT']
    countries = ['United Kingdom', 'Germany', 'France', 'Australia', 'Netherlands']
    return {
        'Time': time.strftime('%H:%M:%S'),
        'Product': random.choice(products),
        'Quantity': random.randint(1, 50),
        'Price': round(random.uniform(1.5, 15.0), 2),
        'Country': random.choice(countries),
        'Revenue': round(random.uniform(10, 500), 2)
    }

live_data = [generate_live_transaction() for _ in range(5)]
live_df = pd.DataFrame(live_data)
st.dataframe(live_df, use_container_width=True)
st.success(f"✅ {len(live_df)} new transactions processed!")

st.markdown("---")
st.subheader("📊 Live Revenue Chart")

fig_live = px.bar(
    live_df,
    x='Product',
    y='Revenue',
    color='Country',
    title=f"Live Revenue — {time.strftime('%H:%M:%S')}",
    color_discrete_sequence=px.colors.qualitative.Set2
)
fig_live.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig_live, use_container_width=True)

if 'total_transactions' not in st.session_state:
    st.session_state.total_transactions = 0
st.session_state.total_transactions += len(live_df)

col1, col2, col3 = st.columns(3)
col1.metric("🔄 Live Transactions", st.session_state.total_transactions)
col2.metric("💰 Live Revenue", f"£{live_df['Revenue'].sum():,.2f}")
col3.metric("🌍 Countries Active", live_df['Country'].nunique())

if auto_refresh:
    time.sleep(refresh_interval)
    st.rerun()