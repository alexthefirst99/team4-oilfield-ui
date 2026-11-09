"""Screen: Home.

OWNER: Person A (SCOPE.md item 1). Only Person A edits this file.
Connect to MySQL and show how many rows each of the 11 tables has.

Hint: Use db.fetch_df() to count the rows in each table.
"""
import streamlit as st

from views.placeholder import todo


def render():
    st.header("Home")
    todo("A", 1, "Connect to MySQL and show how many rows each of the 11 tables has.")
