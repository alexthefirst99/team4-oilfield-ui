"""Screen: Query highlights.

OWNER: Person A (SCOPE.md item 4). Only Person A edits this file.
Pick one of our Phase 3 queries, show its SQL, and run it.

Hint: Read the queries from sql/Team4_Queries.sql (each starts with a '-- Basic/Intermediate/Advanced Query' comment).
"""
import streamlit as st

from views.placeholder import todo


def render():
    st.header("Query highlights")
    todo("A", 4, "Pick one of our Phase 3 queries, show its SQL, and run it.")
