# 💰 Smart Expense Tracker

A beginner-level expense tracker built with **Python** and **Streamlit**.
Users can register, log in, and manage their daily expenses. Each user sees only their own data.

## Features

- Register and login (passwords are saved as hashes, not as plain text)
- Add an expense: date, name, category, amount, payment method
- View all expenses in a table
- Edit and delete expenses
- Filter expenses by date, category and payment method
- Dashboard with total expenses, number of expenses, category-wise and monthly expenses
- Simple bar charts
- Monthly spending summary

## Categories

Food, Travel, Shopping, Education, Bills, Entertainment, Healthcare, Other

## Technologies Used

- Python
- Streamlit (web interface and charts)
- pandas (reading and calculating data)
- CSV files (storage)
- Git and GitHub (version control)
- GitHub Projects Kanban board (project management)

## Project Structure

```
Smart-Expense-Tracker/
├── app.py                  # main Streamlit app
├── requirements.txt        # packages needed
├── README.md               # this file
├── .gitignore              # files Git should ignore
├── data/
│   └── .gitkeep            # keeps the data folder on GitHub
└── utils/
    ├── expense_utils.py    # expense functions (load, save, edit, delete, totals, filters)
    └── auth_utils.py       # register and login functions
```

When the app runs, it creates these files inside `data/`:
- `users.csv` - registered users (passwords are hashed)
- `expenses_<username>.csv` - one expense file for each user

## How to Run

1. Clone the repository
```bash
   git clone https://github.com/mansi10112005/Smart-Expense-Tracker.git
   cd Smart-Expense-Tracker
```
2. Install the packages
```bash
   pip install -r requirements.txt
```
3. Start the app
```bash
   python -m streamlit run app.py
```
4. Open the link shown in the terminal (usually http://localhost:8501), register a new account, then log in.

## Project Management

Tasks were tracked as GitHub Issues on a GitHub Projects Kanban board with four columns:
**To Do → In Progress → Review → Done**.
Commits mention issue numbers (like `#4`) to link the code with the task.

## Author

Mansi Kokate - 3rd year Information Technology student