"""Screen: Add an inspection.

OWNER: Person B (SCOPE.md item 5). Only Person B edits this file.
Form: equipment, technician, date, result (Pass / Needs Maintenance / Fail), notes.

Hint: INSERT INTO INSPECTION with db.execute(). On mysql.connector.Error call errors.show_db_error().
"""
import streamlit as st

from views.placeholder import todo


def render():
    st.header("Add an inspection")
    todo("B", 5, "Form: equipment, technician, date, result (Pass / Needs Maintenance / Fail), notes.")
