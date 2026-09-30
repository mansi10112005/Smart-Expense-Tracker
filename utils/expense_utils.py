# utils/expense_utils.py
# Helper functions for the Smart Expense Tracker

import os
import pandas as pd

# Where the CSV file is stored (works no matter where you run the app from)
BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE_PATH = os.path.join(BASE_FOLDER, "data", "expenses.csv")

# The columns of our notebook
COLUMNS = ["Date", "Name", "Category", "Amount", "Payment Method"]

# Lists used in the form
CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Education",
    "Bills",
    "Entertainment",
    "Healthcare",
    "Other",
]

PAYMENT_METHODS = ["Cash", "UPI", "Debit Card", "Credit Card", "Net Banking", "Other"]


def load_expenses():
    """Read all expenses from the CSV file and return them as a table."""
    # If the file does not exist or is empty, return an empty table
    if not os.path.exists(FILE_PATH) or os.path.getsize(FILE_PATH) == 0:
        return pd.DataFrame(columns=COLUMNS)
    return pd.read_csv(FILE_PATH)


def save_expense(date, name, category, amount, payment_method):
    """Add ONE new expense to the CSV file."""
    # 1. Read the old expenses
    df = load_expenses()

    # 2. Make a new one-row table
    new_row = pd.DataFrame(
        [[str(date), name, category, amount, payment_method]],
        columns=COLUMNS,
    )

    # 3. Join old + new, then write everything back to the file
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(FILE_PATH, index=False)