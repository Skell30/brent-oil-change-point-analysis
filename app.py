import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Brent Oil Prices & Structural Change Detection")

# Load data
brent_df = pd.read_csv(r"C:\Users\pc\brent-oil-change-point-analysis\data\bren.csv", parse_dates=["Date"])
events_df = pd.read_csv(r"C:\Users\pc\brent-oil-change-point-analysis\data\event_data_extended.csv", parse_dates=["date"])

# Sidebar: Change point
most_likely_tau = st.sidebar.number_input("Detected Change Point Index", min_value=0, max_value=len(brent_df)-1, value=245)
change_date = brent_df.loc[most_likely_tau, "Date"]

st.sidebar.write(f"Detected change date: **{change_date.date()}**")

# Plot Brent oil prices
st.subheader("Brent Oil Price Over Time")
fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(brent_df["Date"], brent_df["Price"], label="Price", color="blue")
ax.axvline(change_date, color="red", linestyle="--", label="Change Point")
ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.set_title("Monthly Brent Oil Prices with Change Point")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# Plot Log Returns
st.subheader("Log Returns Over Time")
fig2, ax2 = plt.subplots(figsize=(14, 4))
ax2.plot(brent_df["Date"], brent_df["LogReturn"], color="green", label="Log Return")
ax2.axvline(change_date, color="red", linestyle="--", label="Change Point")
ax2.set_xlabel("Date")
ax2.set_ylabel("Log Return")
ax2.set_title("Monthly Brent Oil Log Returns")
ax2.legend()
ax2.grid(True)
st.pyplot(fig2)

# Optional: Show events near change point
st.subheader("Events Around Change Point")
window_days = st.slider("Event Matching Window (days)", 1000, 3000, 6000)

nearby_events = events_df[
    (events_df["date"] >= change_date - pd.Timedelta(days=window_days)) &
    (events_df["date"] <= change_date + pd.Timedelta(days=window_days))
]

if not nearby_events.empty:
    st.write(nearby_events)
else:
    st.info("No events found within this window.")
