"""Screen: Equipment history.

OWNER: Person A (SCOPE.md item 11). Only Person A edits this file.
(Nice) Pick one equipment item and show its inspections, problems, and repairs.

Hint: Same idea as Advanced Query 2, but for one item.
"""
import streamlit as st

from views.placeholder import todo


def render():
    st.header("Equipment history")
    todo("A", 11, "(Nice) Pick one equipment item and show its inspections, problems, and repairs.")
