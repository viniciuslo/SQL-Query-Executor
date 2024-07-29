# SQL Query Executor
SQL Query Executor is a terminal-based User Interface (TUI) application that allows you to execute SQL queries on a pandas DataFrame, save and load queries, and display results, including graphs.

## Features

- Execute SQL Queries: Allows the execution of SQL queries on a DataFrame.
- Save Queries: Saves queries with a mandatory name and an optional subject.
- Load Queries: Loads saved queries with search by name, query text, or subject.
- Pagination: Navigate through saved queries with pagination.
- Plot Graphs: Displays graphs of query results.
- Advanced Search: Allows advanced search with filters by name, query, and subject.

## Prerequisites

- Python 3.x
- Pandas
- Pandasql
- Urwid
- Matplotlib

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/sql-query-executor.git
cd sql-query-executor
```

Create and activate a virtual environment:

```bash
python -m venv myenv
source myenv/bin/activate  # On Windows, use `myenv\Scripts\activate`
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Project Structure

```
sql-query-executor/
│
├── data/
│   └── queries.json         # JSON file to store saved queries
│
├── src/
│   ├── main.py              # Main script to run the application
│   ├── queries.py           # Functions to save, load, and search queries
│   ├── widgets.py           # Custom widgets for the interface
│   └── utils.py             # Utility functions
│
├── README.md                # This README file
├── requirements.txt         # Dependencies file
└── .gitignore               # File to ignore files/directories

```

## Usage

Start the application:

```bash
python src/main.py
```

Execute a Query:
- Enter your SQL query in the provided text area.
- Click the "Execute" button to run the query and view the results.

Save a Query:
- Enter your SQL query in the provided text area.
- Enter a mandatory name and an optional subject for the query.
- Click the "Save Query" button to save the query.

Load a Query:
- Click the "🔍 Search and Load Query" button.
- Select the search type (by name, query text, or subject).
- Enter the search term and click "Search".
- Navigate through the results using pagination and click on the desired query to load it.

Plot Graphs:
- After executing a query, click the "Plot Graph" button to visualize the graph of the results.

## Contribution

- Fork the project.
- Create a branch for your feature (`git checkout -b feature/fooBar`).
- Commit your changes (`git commit -am 'Add some fooBar'`).
- Push to the branch (`git push origin feature/fooBar`).
- Create a new Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

Your Name - @viniciuslo - vinicius.lima.oem@gmail.com

Project Link: [https://github.com/viniciuslo/sql-query-executor](https://github.com/viniciuslo/sql-query-executor)