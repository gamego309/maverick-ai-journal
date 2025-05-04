import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Logo and App Title
st.set_page_config(page_title="Maverick AI Trade Journal", layout="wide")
st.image("maverick_logo.png", use_container_width=True)
st.title("🚀 Maverick – Your AI-Powered Trade Journal")

# Upload CSV
uploaded_file = st.file_uploader("📤 Upload your trade CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Basic cleanup
    df.dropna(inplace=True)
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])
    else:
        st.error("Your CSV must have a 'Date' column.")

    # Calculate Profit/Loss
    df["PnL"] = (df["Sell_Price"] - df["Buy_Price"]) * df["Qty"]
    df["Holding_Time(min)"] = (
                                      pd.to_datetime(df["Exit_Time"]) - pd.to_datetime(df["Entry_Time"])
                              ).dt.total_seconds() / 60
    df["Cumulative_PnL"] = df["PnL"].cumsum()

    # Dashboard Metrics
    st.subheader("📊 Trade Summary")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Trades", len(df))
    col2.metric("Winning %", f"{(df['PnL'] > 0).mean() * 100:.2f}%")
    col3.metric("Total PnL", f"₹{df['PnL'].sum():,.2f}")
    col4.metric("Avg Holding Time", f"{df['Holding_Time(min)'].mean():.1f} mins")

    st.divider()

    # Equity Curve
    st.subheader("📈 Equity Curve")
    fig_equity = px.line(df, x="Date", y="Cumulative_PnL", title="Equity Over Time")
    st.plotly_chart(fig_equity, use_container_width=True)

    # Symbols Breakdown
    st.subheader("🧩 PnL by Symbol")
    fig_symbols = px.bar(df.groupby("Symbol")["PnL"].sum().sort_values(), title="Symbol Performance")
    st.plotly_chart(fig_symbols, use_container_width=True)

    # Holding Time Distribution
    st.subheader("⏱ Holding Time Distribution")
    fig_hold = px.histogram(df, x="Holding_Time(min)", nbins=30, title="Holding Time Histogram")
    st.plotly_chart(fig_hold, use_container_width=True)

    # Notes (optional)
    st.subheader("📝 Journal Notes")
    with st.form("notes"):
        note = st.text_area("Add a note or journal entry:")
        submitted = st.form_submit_button("Save Note")
        if submitted and note:
            st.success("Note saved (not persistent in this version).")

    st.divider()

    # AI Tip (Mock for now)
    st.subheader("🤖 AI Insight")
    if df["PnL"].mean() < 0:
        st.error("Your average trade is losing. Consider reducing trade frequency or reviewing entry signals.")
    else:
        st.success("You're trading profitably! Focus on consistency and risk control.")

else:
    st.info("Please upload your trade history CSV to begin.")
