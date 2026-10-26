# PocketTrack

A personal expense-tracking web application built with Python, Flask, and SQLite as my final project for Harvard's CS50x.

## Video Demo

[Watch the PocketTrack demonstration on YouTube](https://youtu.be/AYAHfCmmT8k)

## Overview

PocketTrack helps users record, organize, and review everyday expenses. It uses Pakistani rupees (PKR) and combines a web interface with a local SQLite database.

I built this project to apply the programming concepts I learned through CS50x to a practical problem. Developing PocketTrack gave me experience with Python, SQL databases, web application routes, and user-interface design.

## Features

- **Expense management:** Add, edit, and delete expense records.
- **Search and filtering:** Search expenses and filter by category or month.
- **Monthly budgeting:** Compare spending with a planned monthly budget.
- **Spending summaries:** Review spending totals and category-wise breakdowns.
- **Persistent storage:** Store expense and budget information using SQLite.

## Technologies

- Python
- Flask
- SQLite
- HTML and CSS

## Project Structure

- `app.py` — Main Flask application and application logic.
- `init_db.py` — Script to initialize the expenses database table.
- `requirements.txt` — Python dependency list.

## Getting Started

### Requirements

- Python 3
- pip

### Installation

1. Open a terminal in the project directory.
2. Install the required dependency:

   ```bash
   pip install -r requirements.txt
   ```

3. Initialize both database tables:

   ```bash
   python init_db.py
   ```

4. Start the application:

   ```bash
   python app.py
   ```

In CS50.dev, open the application's forwarded port through the Ports panel when the server is running.

**Note:** The application also initializes the required database tables when it starts. You can run `python init_db.py` first to initialize them explicitly.

## What I Learned

Building PocketTrack helped me practise Python programming, SQL database operations, Flask routing, handling user input, and connecting a web interface to persistent data.

## Future Improvements

Possible improvements include exporting expense records, adding more detailed spending reports, and expanding budget-planning features.
