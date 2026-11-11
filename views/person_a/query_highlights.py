"""Screen: Query highlights.

OWNER: Person A (SCOPE.md item 4). Only Person A edits this file.
Pick one of our Phase 3 queries, show its SQL, and run it.
The queries are read from sql/Team4_Queries.sql, so the file stays the one source.
"""
import re
from pathlib import Path

import streamlit as st

import db

QUERY_FILE = Path(__file__).resolve().parents[2] / "sql" / "Team4_Queries.sql"
HEADER = re.compile(r"^-- ((?:Basic|Intermediate|Advanced) Query \d+): (.*)$")


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
    st.header("Query highlights")

    queries = load_queries()
    name = st.selectbox("Query", list(queries))
    purpose, sql = queries[name]

    st.write(f"**Purpose:** {purpose}")
    st.code(sql, language="sql")

    if st.button("Run query"):
        result = db.fetch_df(sql.rstrip(";"))
        st.caption(f"{len(result)} row(s) returned")
        st.dataframe(result, hide_index=True)
