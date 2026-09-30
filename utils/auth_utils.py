# utils/auth_utils.py
# Helper functions for Register and Login

import os
import hashlib
import pandas as pd

# Where the users are stored
BASE_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
USERS_FILE = os.path.join(BASE_FOLDER, "data", "users.csv")

USER_COLUMNS = ["Username", "Full Name", "Password"]


def hash_password(password):
    """Scramble the password so we never save the real one."""
    return hashlib.sha256(password.encode()).hexdigest()


def load_users():
    """Read all registered users from users.csv."""
    if not os.path.exists(USERS_FILE) or os.path.getsize(USERS_FILE) == 0:
        return pd.DataFrame(columns=USER_COLUMNS)
    return pd.read_csv(USERS_FILE, dtype=str)


def register_user(username, full_name, password):
    """Create a new account. Returns (True/False, message)."""
    username = username.strip().lower()
    full_name = full_name.strip()

    # Check the inputs
    if username == "" or full_name == "" or password == "":
        return False, "Please fill in all the boxes."
    if not username.replace("_", "").isalnum():
        return False, "Username can have only letters, numbers and underscore (_)."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    # Check that the username is not already taken
    users = load_users()
    if username in users["Username"].values:
        return False, "This username is already taken. Please choose another."

    # Save the new user (with the scrambled password)
    new_row = pd.DataFrame(
        [[username, full_name, hash_password(password)]],
        columns=USER_COLUMNS,
    )
    users = pd.concat([users, new_row], ignore_index=True)
    users.to_csv(USERS_FILE, index=False)

    return True, "Registration successful! Now please go to the Login tab."


def login_user(username, password):
    """Check username and password. Returns (True, full_name) or (False, error)."""
    username = username.strip().lower()
    users = load_users()

    match = users[users["Username"] == username]
    if match.empty:
        return False, "Username not found. Please register first."

    if match.iloc[0]["Password"] != hash_password(password):
        return False, "Wrong password."

    return True, match.iloc[0]["Full Name"]