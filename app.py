# app.py
# Smart Expense Tracker - main file

import streamlit as st

# 1. Basic page settings (browser tab title and icon)
st.set_page_config(page_title="Smart Expense Tracker", page_icon="💰")

# 2. Big heading at the top of the page
st.title("💰 Smart Expense Tracker")
st.write("Track your daily spending in a simple way.")

# 3. Menu on the left side
st.sidebar.title("Menu")
page = st.sidebar.radio(
    "Go to",
    ["Add Expense", "View Expenses", "Dashboard"]
)

# 4. Show different text depending on the menu choice
if page == "Add Expense":
    st.header("Add Expense")
    st.info("The expense form will come here (Step 5).")

elif page == "View Expenses":
    st.header("View Expenses")
    st.info("The expense table will come here (Step 6).")

elif page == "Dashboard":
    st.header("Dashboard")
    st.info("Totals and charts will come here (Step 7).")