import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# PAGE CONFIG
st.set_page_config(page_title="Stock Analytics App", layout="wide")

# CUSTOM CSS (APP STYLE)
st.markdown("""
<style>
body {
    background-color: #0E1117;
}
.main {
    background-color: #0E1117;
}
.card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0 0 10px rgba(0,0,0,0.4);
}
h1, h2, h3 {
    color: #00FFAA;
}
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("<h1>📊 Stock Volatility Analytics Dashboard</h1>", unsafe_allow_html=True)

# SIDEBAR
st.sidebar.title("⚙️ Controls")

stocks = {
    "Apple": "AAPL",
    "Tesla": "TSLA",
    "Infosys": "INFY.NS",
    "TCS": "TCS.NS",
    "Reliance": "RELIANCE.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS"
}

selected_stocks = st.sidebar.multiselect(
    "Select Stocks",
    list(stocks.keys()),
    default=["Apple", "Tesla"]
)

start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2024-01-01"))

if len(selected_stocks) == 0:
    st.warning("Please select at least one stock")
    st.stop()

# FETCH DATA
data_dict = {}

for stock in selected_stocks:
    ticker = stocks[stock]
    data = yf.download(ticker, start=start_date, end=end_date)

    data['Returns'] = data['Close'].pct_change()
    data['Rolling Volatility'] = data['Returns'].rolling(window=30).std()

    data_dict[stock] = data

# METRICS SECTION (CARDS)
st.subheader("📊 Key Metrics")

cols = st.columns(len(selected_stocks))

volatility_values = {}

for i, stock in enumerate(selected_stocks):
    vol = data_dict[stock]['Returns'].std()
    volatility_values[stock] = vol

    with cols[i]:
        st.markdown(f"""
        <div class="card">
            <h3>{stock}</h3>
            <h2>{round(vol, 5)}</h2>
            <p>Volatility</p>
        </div>
        """, unsafe_allow_html=True)

# FIND MOST & LEAST
most_volatile = max(volatility_values, key=volatility_values.get)
least_volatile = min(volatility_values, key=volatility_values.get)

# CHARTS
col1, col2 = st.columns(2)

# PRICE CHART (INTERACTIVE)
with col1:
    st.subheader("📈 Price Trend")

    fig_price = go.Figure()

    for stock in selected_stocks:
        fig_price.add_trace(go.Scatter(
            x=data_dict[stock].index,
            y=data_dict[stock]['Close'],
            mode='lines',
            name=stock
        ))

    fig_price.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(fig_price, use_container_width=True)

# VOLATILITY CHART
with col2:
    st.subheader("📉 Volatility Trend")

    fig_vol = go.Figure()

    for stock in selected_stocks:
        fig_vol.add_trace(go.Scatter(
            x=data_dict[stock].index,
            y=data_dict[stock]['Rolling Volatility'],
            mode='lines',
            name=stock
        ))

    fig_vol.update_layout(
        template="plotly_dark",
        height=400
    )

    st.plotly_chart(fig_vol, use_container_width=True)

# TREND ANALYSIS CARD
st.markdown("### 📊 Trend Analysis")

for stock in selected_stocks:
    data = data_dict[stock]
    avg_vol = data['Rolling Volatility'].mean()

    st.markdown(f"""
    <div class="card">
        <h3>{stock}</h3>
        <p>Average Volatility: {round(avg_vol,5)}</p>
    </div>
    """, unsafe_allow_html=True)

# INSIGHTS CARD
st.markdown("### 🔍 Insights")

st.markdown(f"""
<div class="card">
<ul>
<li><b>{most_volatile}</b> is the most volatile stock</li>
<li><b>{least_volatile}</b> is the most stable stock</li>
<li>Volatility spikes indicate uncertain market periods</li>
<li>High volatility = high risk & reward</li>
</ul>
</div>
""", unsafe_allow_html=True)

# CONCLUSION CARD
st.markdown("### 📌 Conclusion")

st.markdown(f"""
<div class="card">
<p>✅ Most Stable: <b>{least_volatile}</b></p>
<p>⚠️ Most Risky: <b>{most_volatile}</b></p>
<p>Invest based on your risk tolerance.</p>
</div>
""", unsafe_allow_html=True)