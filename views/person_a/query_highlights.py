"""Screen: Reports (our Phase 3 queries).

OWNER: Person A (SCOPE.md item 4). Only Person A edits this file.
Pick a question in plain words and see the answer right away. The SQL behind it
is one click away for anyone who wants it. The queries are read from
sql/Team4_Queries.sql, so the file stays the one source.
"""
import re
from pathlib import Path

import streamlit as st

import db
from views.person_a.display import show_table

QUERY_FILE = Path(__file__).resolve().parents[2] / "sql" / "Team4_Queries.sql"
HEADER = re.compile(r"^-- ((?:Basic|Intermediate|Advanced) Query \d+): (.*)$")

# Each query as the question a user would ask
QUESTIONS = {
    "Basic Query 1": "Which inspections did Rodney Hong do?",
    "Basic Query 2": "Which problems are medium or high priority?",
    "Basic Query 3": "Which work orders are still open?",
    "Basic Query 4": "What equipment is at each site?",
    "Basic Query 5": "Which equipment is not working?",
    "Basic Query 6": "What repairs were done on pump PMP-001?",
    "Basic Query 7": "Which parts were used for work order 4?",
    "Intermediate Query 1": "Which technicians did 3 or more inspections?",
    "Intermediate Query 2": "Which parts are used the most?",
    "Intermediate Query 3": "Which technicians have no work assigned?",
    "Intermediate Query 4": "Which equipment needed more than one work order?",
    "Intermediate Query 5": "Which equipment has never been inspected?",
    "Advanced Query 1": "How many days does each repair take?",
    "Advanced Query 2": "What is the maintenance summary for each item?",
}


def load_queries():
    """Return {name: (purpose, sql)} from the query file, in file order."""
    queries = {}
    name = None
    for line in QUERY_FILE.read_text().splitlines():
        match = HEADER.match(line)
        if match:
            name, purpose = match.groups()
            queries[name] = [purpose, []]
        elif name and not line.startswith("-- "):
            queries[name][1].append(line)
    return {n: (p, "\n".join(lines).strip()) for n, (p, lines) in queries.items()}


def render():
    st.header("Reports")
    st.write("Ready-made answers to common questions. Pick a question to see the answer.")

    queries = load_queries()
    name = st.selectbox("Question", list(queries), format_func=lambda n: QUESTIONS.get(n, n))
    purpose, sql = queries[name]

    st.caption(purpose)
    result = db.fetch_df(sql.rstrip(";"))
    st.write(f"**{len(result)} result(s)**")
    show_table(result)

    with st.expander(f"See the SQL behind this report ({name})"):
        st.code(sql, language="sql")
