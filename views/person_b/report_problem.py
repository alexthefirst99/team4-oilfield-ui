"""Screen: Report a problem.

OWNER: Person B (SCOPE.md item 6). Only Person B edits this file.
Form: equipment, optional inspection, priority (Low / Medium / High), description.

Hint: INSERT INTO PROBLEM_REPORT. The BR18 trigger blocks an inspection from different equipment.
"""
import streamlit as st

from views.placeholder import todo


def render():
    st.header("Report a problem")
    todo("B", 6, "Form: equipment, optional inspection, priority (Low / Medium / High), description.")
