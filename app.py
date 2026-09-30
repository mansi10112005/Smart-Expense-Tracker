# app.py
# Smart Expense Tracker - main file

import streamlit as st
import pandas as pd
from datetime import date

from utils.expense_utils import (
    CATEGORIES,
    PAYMENT_METHODS,
    load_expenses,
    save_expense,
    update_expense,
    delete_expense,
    get_total_expenses,
    get_category_totals,
    get_monthly_totals,
    filter_expenses,
    get_available_months,
    get_expenses_for_month,
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
    ["Add Expense", "View Expenses", "Dashboard", "Monthly Summary"]
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
        st.dataframe(all_expenses.tail(5))

elif page == "View Expenses":
    st.header("View Expenses")

    # Show a message left by the last Update / Delete (if any)
    if "message" in st.session_state:
        st.success(st.session_state["message"])
        del st.session_state["message"]

    expenses = load_expenses()

    if expenses.empty:
        st.info("No expenses yet. Go to 'Add Expense' to add one.")
    else:
        # ---------- Filters ----------
        st.subheader("Filters")

        all_dates = pd.to_datetime(expenses["Date"]).dt.date
        col1, col2 = st.columns(2)
        start_date = col1.date_input("From date", value=all_dates.min())
        end_date = col2.date_input("To date", value=all_dates.max())

        col3, col4 = st.columns(2)
        category_filter = col3.selectbox("Category", ["All"] + CATEGORIES)
        payment_filter = col4.selectbox("Payment method", ["All"] + PAYMENT_METHODS)

        # Apply the filters
        filtered = filter_expenses(
            expenses, start_date, end_date, category_filter, payment_filter
        )

        # ---------- The table ----------
        st.subheader("All expenses")

        if start_date > end_date:
            st.error("'From date' must be before 'To date'.")
        elif filtered.empty:
            st.warning("No expenses match these filters.")
        else:
            st.write(
                f"Showing **{len(filtered)}** expense(s) | "
                f"Total: **₹{get_total_expenses(filtered):,.2f}**"
            )
            st.write("The number on the left is the Row ID.")
            st.dataframe(filtered)

            # ---------- Choose which expense to change ----------
            st.subheader("Edit or Delete an Expense")

            row_ids = list(filtered.index)
            chosen = st.selectbox(
                "Choose the expense (Row ID)",
                row_ids,
                format_func=lambda i: (
                    f"{i} - {expenses.loc[i, 'Date']} - "
                    f"{expenses.loc[i, 'Name']} - ₹{expenses.loc[i, 'Amount']}"
                ),
            )
            row = expenses.loc[chosen]

            # Find the current category / payment method in our lists
            if row["Category"] in CATEGORIES:
                cat_index = CATEGORIES.index(row["Category"])
            else:
                cat_index = 0

            if row["Payment Method"] in PAYMENT_METHODS:
                pay_index = PAYMENT_METHODS.index(row["Payment Method"])
            else:
                pay_index = 0

            # ---------- Edit form (already filled with the old values) ----------
            st.markdown("**Edit**")
            with st.form(f"edit_form_{chosen}"):
                new_date = st.date_input(
                    "Date",
                    value=date.fromisoformat(str(row["Date"])),
                    key=f"date_{chosen}",
                )
                new_name = st.text_input("Expense name / description", value=row["Name"], key=f"name_{chosen}")
                new_category = st.selectbox("Category", CATEGORIES, index=cat_index, key=f"cat_{chosen}")
                new_amount = st.number_input(
                    "Amount (₹)",
                    min_value=0.0,
                    step=1.0,
                    value=float(row["Amount"]),
                    key=f"amount_{chosen}",
                )
                new_payment = st.selectbox("Payment method", PAYMENT_METHODS, index=pay_index, key=f"pay_{chosen}")

                update_clicked = st.form_submit_button("Update Expense")

            if update_clicked:
                if new_name.strip() == "":
                    st.error("Please enter an expense name.")
                elif new_amount <= 0:
                    st.error("Amount must be greater than 0.")
                else:
                    update_expense(chosen, new_date, new_name.strip(), new_category, new_amount, new_payment)
                    st.session_state["message"] = "Expense updated successfully! ✅"
                    st.rerun()

            # ---------- Delete ----------
            st.markdown("**Delete**")
            sure = st.checkbox("Yes, I am sure I want to delete this expense", key=f"sure_{chosen}")
            if st.button("🗑️ Delete Expense"):
                if sure:
                    delete_expense(chosen)
                    st.session_state["message"] = "Expense deleted successfully! 🗑️"
                    st.rerun()
                else:
                    st.warning("Please tick the 'I am sure' box first.")

elif page == "Dashboard":
    st.header("Dashboard")

    expenses = load_expenses()

    if expenses.empty:
        st.info("No expenses yet. Add some expenses to see the dashboard.")
    else:
        # ---------- Two number cards ----------
        total = get_total_expenses(expenses)
        count = len(expenses)

        col1, col2 = st.columns(2)
        col1.metric("Total Expenses", f"₹{total:,.2f}")
        col2.metric("Number of Expenses", count)

        # ---------- Category-wise expenses ----------
        st.subheader("Category-wise expenses")
        category_totals = get_category_totals(expenses)
        st.dataframe(category_totals)
        st.bar_chart(category_totals)

        # ---------- Monthly expenses ----------
        st.subheader("Monthly expenses")
        monthly_totals = get_monthly_totals(expenses)
        st.dataframe(monthly_totals)
        st.bar_chart(monthly_totals)

elif page == "Monthly Summary":
    st.header("Monthly Summary")

    expenses = load_expenses()

    if expenses.empty:
        st.info("No expenses yet. Add some expenses to see the summary.")
    else:
        # Choose a month (only months that have expenses are shown)
        months = get_available_months(expenses)
        chosen_month = st.selectbox("Choose a month", months)

        # Keep only that month's expenses
        month_df = get_expenses_for_month(expenses, chosen_month)

        # ---------- Two number cards ----------
        col1, col2 = st.columns(2)
        col1.metric(f"Total spent in {chosen_month}", f"₹{get_total_expenses(month_df):,.2f}")
        col2.metric("Number of expenses", len(month_df))

        # ---------- Simple sentences ----------
        category_totals = get_category_totals(month_df)
        top_category = category_totals.idxmax()
        top_amount = category_totals.max()
        st.success(
            f"You spent the most on **{top_category}** this month "
            f"(₹{top_amount:,.2f})."
        )

        biggest = month_df.loc[month_df["Amount"].idxmax()]
        st.info(
            f"Biggest single expense: **{biggest['Name']}** - "
            f"₹{biggest['Amount']:,.2f} on {biggest['Date']}."
        )

        # ---------- Category-wise for this month ----------
        st.subheader("Category-wise for this month")
        st.dataframe(category_totals)
        st.bar_chart(category_totals)

        # ---------- All expenses of this month ----------
        st.subheader("All expenses of this month")
        st.dataframe(month_df)