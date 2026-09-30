# app.py
# Smart Expense Tracker - main file

import streamlit as st
from datetime import date

from utils.expense_utils import (
    CATEGORIES,
    PAYMENT_METHODS,
    load_expenses,
    save_expense,
)

# 1. Basic page settings
st.set_page_config(page_title="Smart Expense Tracker", page_icon="💰")

# 2. Heading
st.title("💰 Smart Expense Tracker")
st.write("Track your daily spending in a simple way.")

# 3. Menu on the left side
st.sidebar.title("Menu")
page = st.sidebar.radio(
    "Go to",
    ["Add Expense", "View Expenses", "Dashboard"]
)

# 4. Show content depending on the menu choice
if page == "Add Expense":
    st.header("Add Expense")

    # The form (the paper slip)
    with st.form("expense_form", clear_on_submit=True):
        expense_date = st.date_input("Date", value=date.today())
        name = st.text_input("Expense name / description")
        category = st.selectbox("Category", CATEGORIES)
        amount = st.number_input("Amount (₹)", min_value=0.0, step=1.0)
        payment_method = st.selectbox("Payment method", PAYMENT_METHODS)

        submitted = st.form_submit_button("Add Expense")

    # What happens after the button is clicked
    if submitted:
        if name.strip() == "":
            st.error("Please enter an expense name.")
        elif amount <= 0:
            st.error("Amount must be greater than 0.")
        else:
            save_expense(expense_date, name.strip(), category, amount, payment_method)
            st.success("Expense added successfully! ✅")

    # Small preview: last 5 expenses
    st.subheader("Last 5 expenses")
    all_expenses = load_expenses()
    if all_expenses.empty:
        st.info("No expenses yet. Add your first one above!")
    else:
        st.dataframe(all_expenses.tail(5), use_container_width=True)

elif page == "View Expenses":
    st.header("View Expenses")
    st.info("The expense table will come here (Step 6).")

elif page == "Dashboard":
    st.header("Dashboard")
    st.info("Totals and charts will come here (Step 7).")