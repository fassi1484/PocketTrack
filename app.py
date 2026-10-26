
from flask import Flask, request, redirect, render_template_string, abort
import sqlite3
import math
from pathlib import Path
from datetime import date

app = Flask(__name__)

DB_PATH = Path(__file__).resolve().parent / "expenses.db"

CATEGORIES = [
    "Food", "Transport", "Education", "Shopping",
    "Bills", "Health", "Entertainment", "Other"
]

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>PocketTrack | Expense Manager</title>
<style>
:root {
    --bg: #f5f7fc;
    --card: #ffffff;
    --text: #172033;
    --muted: #6b7280;
    --primary: #4f46e5;
    --primary-dark: #3730a3;
    --border: #e5e7ef;
    --green: #15803d;
    --red: #dc2626;
    --soft-purple: #eef2ff;
}
* { box-sizing: border-box; }
body {
    margin: 0;
    background: var(--bg);
    color: var(--text);
    font-family: Arial, Helvetica, sans-serif;
    line-height: 1.5;
}
.container { max-width: 1200px; margin: auto; padding: 34px 22px 56px; }
header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 12px;
    margin-bottom: 28px;
}
.brand { display: flex; align-items: center; gap: 12px; }
.logo {
    background: linear-gradient(135deg, var(--primary), #818cf8);
    color: white;
    width: 48px;
    height: 48px;
    display: grid;
    place-items: center;
    border-radius: 14px;
    font-size: 24px;
}
h1 { font-size: 27px; letter-spacing: -0.7px; margin: 0; }
h2 { font-size: 19px; letter-spacing: -0.25px; margin: 0 0 16px; }
p { margin-top: 5px; }
.muted { color: var(--muted); font-size: 13px; }
.grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 16px;
    margin-bottom: 20px;
}
.card {
    background: var(--card);
    padding: 24px;
    border: 1px solid var(--border);
    border-radius: 18px;
    box-shadow: 0 8px 28px rgba(23, 32, 51, 0.045);
    min-width: 0;
}
.metric-label { color: var(--muted); font-size: 14px; }
.metric { font-size: clamp(22px, 2.5vw, 29px); font-weight: 800; letter-spacing: -0.7px; margin: 9px 0 3px; overflow-wrap: anywhere; }
.green { color: var(--green); }
.red { color: var(--red); }
.layout {
    display: grid;
    grid-template-columns: minmax(0, 1.1fr) minmax(0, 0.9fr);
    gap: 18px;
    margin-bottom: 20px;
}
label { display: block; font-size: 13px; font-weight: 650; margin: 12px 0 5px; }
input, select {
    display: block;
    width: 100%;
    min-width: 0;
    padding: 12px 13px;
    border: 1px solid #d9deea;
    border-radius: 10px;
    background: white;
    color: var(--text);
    font: inherit;
}
input:focus, select:focus { outline: 2px solid #405cf544; border-color: var(--primary); }
button, .button {
    display: inline-block;
    padding: 10px 14px;
    border: 0;
    border-radius: 9px;
    background: var(--primary);
    color: white;
    font: inherit;
    font-size: 13px;
    font-weight: 650;
    text-decoration: none;
    cursor: pointer;
    text-align: center;
}
button:hover, .button:hover { filter: brightness(.96); transform: translateY(-1px); }
button, .button { transition: transform .15s ease, filter .15s ease, box-shadow .15s ease; }
button:focus-visible, .button:focus-visible { outline: 3px solid #818cf8; outline-offset: 2px; }
.secondary { background: var(--soft-purple); color: #3730a3; }
.danger { background: #fff0f1; color: #bb263b; }
.success { background: #e8f7ee; color: #137547; }
.full { width: 100%; margin-top: 15px; }
.row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
.row > * { flex: 1; }
form.inline { display: inline; }
.filters {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr 1fr;
    gap: 10px;
    align-items: end;
}
.filters label { margin-top: 0; }
.filters button { width: 100%; }
.expense {
    padding: 15px 0;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
}
.expense:last-child { border-bottom: 0; }
.expense-title { font-weight: 700; overflow-wrap: anywhere; }
.amount { font-weight: 750; white-space: nowrap; }
.expense-actions { display: flex; gap: 7px; margin-top: 8px; flex-wrap: wrap; }
.expense-actions button, .expense-actions .button { padding: 7px 10px; }
.pill {
    display: inline-block;
    background: var(--soft-purple);
    color: #3730a3;
    border-radius: 20px;
    padding: 3px 9px;
    font-size: 11px;
    margin-top: 5px;
}
.progress {
    height: 10px;
    border-radius: 10px;
    background: #e9edf5;
    overflow: hidden;
    margin: 14px 0 8px;
}
.progress-bar { height: 100%; background: var(--green); border-radius: 10px; transition: width .25s ease; }
.chart-row { margin: 15px 0; }
.chart-heading { display: flex; justify-content: space-between; gap: 10px; font-size: 13px; margin-bottom: 5px; }
.bar-bg { height: 9px; background: #edf0f6; border-radius: 10px; overflow: hidden; }
.bar { height: 100%; background: linear-gradient(90deg, var(--primary), #818cf8); border-radius: 10px; }
.notice {
    padding: 12px 14px;
    background: #fff7e5;
    border: 1px solid #f3dfac;
    border-radius: 10px;
    margin-bottom: 16px;
    font-size: 14px;
}
.empty { text-align: center; padding: 30px 10px; color: var(--muted); }
a { color: var(--primary-dark); }
::selection { background: #c7d2fe; color: #1e1b4b; }
.section-heading {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 15px;
}
@media (max-width: 760px) {
    .grid { grid-template-columns: 1fr; gap: 10px; }
    .layout { grid-template-columns: 1fr; }
    .filters { grid-template-columns: 1fr 1fr; }
    .metric { font-size: 24px; }
}
@media (max-width: 430px) {
    .filters { grid-template-columns: 1fr; }
    .expense { align-items: flex-start; }
    .expense-right { text-align: right; }
    .card { padding: 16px; }
}
</style>
</head>
<body>
<div class="container">
<header>
    <div class="brand">
        <div class="logo">P</div>
        <div>
            <h1>PocketTrack</h1>
            <div class="muted">Your personal finance dashboard</div>
        </div>
    </div>
    <span class="pill">PKR · Personal tracker</span>
</header>

{% if error %}
<div class="notice">{{ error }}</div>
{% endif %}

<div class="grid">
    <div class="card">
        <div class="metric-label">All-time spending</div>
        <div class="metric">PKR {{ "%.2f"|format(all_time_total) }}</div>
        <div class="muted">Across all recorded expenses</div>
    </div>
    <div class="card">
        <div class="metric-label">{{ current_month_label }} spending</div>
        <div class="metric">PKR {{ "%.2f"|format(month_total) }}</div>
        <div class="muted">{{ month_count }} expenses this month</div>
    </div>
    <div class="card">
        <div class="metric-label">Selected month remaining</div>
        <div class="metric {{ 'red' if remaining < 0 else 'green' }}">
            PKR {{ "%.2f"|format(remaining) }}
        </div>
        <div class="muted">
            {% if budget > 0 %}
                PKR {{ "%.2f"|format(budget) }} budget · {{ budget_month }}
            {% else %}
                Set a budget to track your limit
            {% endif %}
        </div>
    </div>
</div>

<div class="layout">
    <section class="card">
        <h2>{{ "Edit expense" if edit_expense else "Add an expense" }}</h2>
        <form method="post"
              action="{{ '/edit/' ~ edit_expense.id if edit_expense else '/add' }}">
            <label for="title">Expense title</label>
            <input id="title" name="title" maxlength="100" required
                   placeholder="e.g. Lunch, bus fare"
                   value="{{ edit_expense.title if edit_expense else '' }}">

            <label for="amount">Amount (PKR)</label>
            <input id="amount" name="amount" type="number" min="0.01"
                   max="1000000000" step="0.01" required
                   placeholder="e.g. 350"
                   value="{{ edit_expense.amount if edit_expense else '' }}">

            <label for="category">Category</label>
            <select id="category" name="category" required>
                {% for cat in categories %}
                <option value="{{ cat }}"
                    {% if edit_expense and edit_expense.category == cat %}selected{% endif %}>
                    {{ cat }}
                </option>
                {% endfor %}
            </select>

            <label for="expense_date">Date</label>
            <input id="expense_date" name="date" type="date" required
                   value="{{ edit_expense.date if edit_expense else today }}">

            <label for="notes">Notes (optional)</label>
            <input id="notes" name="notes" maxlength="500"
                   placeholder="Extra details"
                   value="{{ edit_expense.notes if edit_expense else '' }}">

            <button class="full" type="submit">
                {{ "Save changes" if edit_expense else "Add expense" }}
            </button>
            {% if edit_expense %}
            <a class="button secondary full" href="/">Cancel editing</a>
            {% endif %}
        </form>
    </section>

    <section class="card">
        <h2>Monthly budget</h2>
        <p class="muted">Choose a month and set your spending limit.</p>
        <form method="post" action="/budget">
            <label for="budget_month">Budget month</label>
            <input id="budget_month" type="month" name="month"
                   value="{{ budget_month }}" required>

            <label for="budget_amount">Budget amount (PKR)</label>
            <input id="budget_amount" type="number" name="amount"
                   min="0.01" max="1000000000" step="0.01" required
                   placeholder="e.g. 15000"
                   value="{{ budget if budget > 0 else '' }}">

            <button class="full" type="submit">Save monthly budget</button>
        </form>

        {% if budget > 0 %}
        <div class="progress">
            <div class="progress-bar"
                 style="width: {{ budget_percent }}%; background: {{ '#dc2626' if budget_spending > budget else '#15803d' }};">
            </div>
        </div>
        <div class="chart-heading">
            <span>Budget used · {{ budget_month }}</span>
            <strong>{{ "%.1f"|format(budget_percent) }}%</strong>
        </div>
        {% if budget_spending > budget %}
        <p class="red muted">You've exceeded this month's budget by PKR {{ "%.2f"|format(budget_spending - budget) }}.</p>
        {% else %}
        <p class="green muted">PKR {{ "%.2f"|format(budget_spending) }} spent this month. You're within budget.</p>
        {% endif %}
        {% endif %}
    </section>
</div>

<section class="card" style="margin-bottom:20px">
    <div class="section-heading">
        <h2 style="margin:0">Spending breakdown</h2>
        <span class="muted">{{ chart_month_label }}</span>
    </div>
    {% if chart_data %}
        {% for item in chart_data %}
        <div class="chart-row">
            <div class="chart-heading">
                <span>{{ item.category }}</span>
                <strong>PKR {{ "%.2f"|format(item.total) }}</strong>
            </div>
            <div class="bar-bg">
                <div class="bar" style="width: {{ item.percent }}%"></div>
            </div>
        </div>
        {% endfor %}
    {% else %}
        <div class="empty">No expenses recorded for this month yet.</div>
    {% endif %}
</section>

<section class="card">
    <div class="section-heading">
        <h2 style="margin:0">Expenses</h2>
        <span class="muted">{{ expenses|length }} matching records</span>
    </div>

    <form method="get" action="/" class="filters">
        <div>
            <label for="q">Search</label>
            <input id="q" name="q" placeholder="Title or notes"
                   value="{{ filters.q }}">
        </div>
        <div>
            <label for="filter_category">Category</label>
            <select id="filter_category" name="category">
                <option value="">All categories</option>
                {% for cat in categories %}
                <option value="{{ cat }}"
                    {% if filters.category == cat %}selected{% endif %}>
                    {{ cat }}
                </option>
                {% endfor %}
            </select>
        </div>
        <div>
            <label for="filter_month">Month</label>
            <input id="filter_month" type="month" name="month"
                   value="{{ filters.month }}">
        </div>
        <div>
            <label>&nbsp;</label>
            <button type="submit">Apply filters</button>
        </div>
    </form>
    <p><a href="/" class="muted">Clear all filters</a></p>

    {% if expenses %}
        {% for expense in expenses %}
        <div class="expense">
            <div style="min-width:0">
                <div class="expense-title">{{ expense.title }}</div>
                <span class="pill">{{ expense.category }}</span>
                <div class="muted">{{ expense.date }}</div>
                {% if expense.notes %}
                <div class="muted">{{ expense.notes }}</div>
                {% endif %}
                <div class="expense-actions">
                    <a class="button secondary"
                       href="/?edit={{ expense.id }}">Edit</a>
                    <form class="inline" action="/delete/{{ expense.id }}"
                          method="post"
                          onsubmit="return confirm('Delete this expense?');">
                        <button class="danger" type="submit">Delete</button>
                    </form>
                </div>
            </div>
            <div class="expense-right">
                <div class="amount">PKR {{ "%.2f"|format(expense.amount) }}</div>
            </div>
        </div>
        {% endfor %}
    {% else %}
        <div class="empty">No matching expenses. Try different filters or add an expense.</div>
    {% endif %}
</section>

<p class="muted" style="text-align:center;margin-top:25px">
    PocketTrack · Track spending, understand habits, manage your budget.
</p>
</div>
</body>
</html>
"""


def get_db():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_db():
    connection = get_db()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            notes TEXT DEFAULT ''
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS budgets (
            month TEXT PRIMARY KEY,
            amount REAL NOT NULL
        )
    """)
    connection.commit()
    connection.close()


def valid_expense(form):
    title = form.get("title", "").strip()
    amount_text = form.get("amount", "")
    category = form.get("category", "")
    expense_date = form.get("date", "")
    notes = form.get("notes", "").strip()

    if not title or len(title) > 100:
        return None, "Title is required and must be at most 100 characters."

    try:
        amount = float(amount_text)
    except (TypeError, ValueError):
        return None, "Enter a valid amount."

    if not math.isfinite(amount) or amount <= 0 or amount > 1_000_000_000:
        return None, "Amount must be positive and no more than 1 billion PKR."

    if category not in CATEGORIES:
        return None, "Choose a valid category."

    if len(notes) > 500:
        return None, "Notes must be at most 500 characters."

    try:
        parsed_date = date.fromisoformat(expense_date)
        if parsed_date.isoformat() != expense_date:
            raise ValueError
    except (TypeError, ValueError):
        return None, "Choose a valid date."

    return (title, amount, category, expense_date, notes), None


@app.route("/")
def index():
    today = date.today()
    current_month = today.strftime("%Y-%m")
    month_label = today.strftime("%B %Y")

    search = request.args.get("q", "").strip()[:100]
    category = request.args.get("category", "")
    month_filter = request.args.get("month", "")

    if category not in CATEGORIES:
        category = ""

    if month_filter:
        try:
            if len(month_filter) != 7 or month_filter[4] != "-":
                raise ValueError
            date.fromisoformat(month_filter + "-01")
        except ValueError:
            month_filter = ""

    connection = get_db()

    all_time_total = connection.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses"
    ).fetchone()[0]

    month_total = connection.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE substr(date, 1, 7) = ?",
        (current_month,)
    ).fetchone()[0]

    month_count = connection.execute(
        "SELECT COUNT(*) FROM expenses WHERE substr(date, 1, 7) = ?",
        (current_month,)
    ).fetchone()[0]

    budget_row = connection.execute(
        "SELECT amount FROM budgets WHERE month = ?", (current_month,)
    ).fetchone()
    budget = budget_row["amount"] if budget_row else 0.0
    remaining = budget - month_total if budget > 0 else 0.0
    budget_percent = min(100.0, month_total / budget * 100) if budget > 0 else 0.0

    chart_rows = connection.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE substr(date, 1, 7) = ?
        GROUP BY category
        ORDER BY total DESC
    """, (current_month,)).fetchall()

    max_chart_total = max((row["total"] for row in chart_rows), default=0)
    chart_data = [
        {
            "category": row["category"],
            "total": row["total"],
            "percent": round(row["total"] / max_chart_total * 100, 1)
            if max_chart_total else 0
        }
        for row in chart_rows
    ]

    conditions = []
    params = []

    if search:
        conditions.append("(title LIKE ? OR notes LIKE ?)")
        params.extend([f"%{search}%", f"%{search}%"])

    if category:
        conditions.append("category = ?")
        params.append(category)

    if month_filter:
        conditions.append("substr(date, 1, 7) = ?")
        params.append(month_filter)

    sql = "SELECT * FROM expenses"
    if conditions:
        sql += " WHERE " + " AND ".join(conditions)
    sql += " ORDER BY date DESC, id DESC"

    expenses = connection.execute(sql, params).fetchall()

    selected_budget_month = month_filter or current_month
    selected_month_total = connection.execute(
        "SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE substr(date, 1, 7) = ?",
        (selected_budget_month,)
    ).fetchone()[0]

    selected_budget_row = connection.execute(
        "SELECT amount FROM budgets WHERE month = ?",
        (selected_budget_month,)
    ).fetchone()
    selected_budget = (
        selected_budget_row["amount"] if selected_budget_row else 0.0
    )
    selected_remaining = selected_budget - selected_month_total if selected_budget > 0 else 0.0
    selected_budget_percent = (
        min(100.0, selected_month_total / selected_budget * 100)
        if selected_budget > 0 else 0.0
    )

    selected_chart_rows = connection.execute("""
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE substr(date, 1, 7) = ?
        GROUP BY category
        ORDER BY total DESC
    """, (selected_budget_month,)).fetchall()
    selected_max_chart_total = max(
        (row["total"] for row in selected_chart_rows), default=0
    )
    selected_chart_data = [
        {
            "category": row["category"],
            "total": row["total"],
            "percent": round(row["total"] / selected_max_chart_total * 100, 1)
            if selected_max_chart_total else 0
        }
        for row in selected_chart_rows
    ]
    selected_month_date = date.fromisoformat(selected_budget_month + "-01")
    selected_month_label = selected_month_date.strftime("%B %Y")

    edit_id = request.args.get("edit", type=int)
    edit_expense = None
    if edit_id is not None:
        edit_expense = connection.execute(
            "SELECT * FROM expenses WHERE id = ?", (edit_id,)
        ).fetchone()

    connection.close()

    return render_template_string(
        HTML,
        expenses=expenses,
        all_time_total=all_time_total,
        month_total=month_total,
        month_count=month_count,
        budget=selected_budget,
        remaining=selected_remaining,
        budget_spending=selected_month_total,
        budget_percent=selected_budget_percent,
        categories=CATEGORIES,
        today=today.isoformat(),
        current_month_label=month_label,
        chart_month_label=selected_month_label,
        chart_data=selected_chart_data,
        filters={"q": search, "category": category, "month": month_filter},
        budget_month=selected_budget_month,
        edit_expense=edit_expense,
        error=None,
    )


@app.route("/add", methods=["POST"])
def add():
    data, error = valid_expense(request.form)
    if error:
        return error, 400

    connection = get_db()
    connection.execute("""
        INSERT INTO expenses (title, amount, category, date, notes)
        VALUES (?, ?, ?, ?, ?)
    """, data)
    connection.commit()
    connection.close()
    return redirect("/")


@app.route("/edit/<int:expense_id>", methods=["POST"])
def edit(expense_id):
    data, error = valid_expense(request.form)
    if error:
        return error, 400

    connection = get_db()
    existing = connection.execute(
        "SELECT id FROM expenses WHERE id = ?", (expense_id,)
    ).fetchone()

    if existing is None:
        connection.close()
        abort(404)

    connection.execute("""
        UPDATE expenses
        SET title = ?, amount = ?, category = ?, date = ?, notes = ?
        WHERE id = ?
    """, (*data, expense_id))
    connection.commit()
    connection.close()
    return redirect("/")


@app.route("/delete/<int:expense_id>", methods=["POST"])
def delete(expense_id):
    connection = get_db()
    connection.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    connection.commit()
    connection.close()
    return redirect("/")


@app.route("/budget", methods=["POST"])
def save_budget():
    month = request.form.get("month", "")
    amount_text = request.form.get("amount", "")

    try:
        if len(month) != 7 or month[4] != "-":
            raise ValueError
        date.fromisoformat(month + "-01")
        amount = float(amount_text)
        if not math.isfinite(amount) or amount <= 0 or amount > 1_000_000_000:
            raise ValueError
    except (TypeError, ValueError):
        return "Enter a valid month and a positive budget amount.", 400

    connection = get_db()
    connection.execute("""
        INSERT INTO budgets (month, amount)
        VALUES (?, ?)
        ON CONFLICT(month) DO UPDATE SET amount = excluded.amount
    """, (month, amount))
    connection.commit()
    connection.close()

    return redirect("/?month=" + month)


initialize_db()

if __name__ == "__main__":
    app.run(debug=True)
