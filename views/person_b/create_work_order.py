"""Screen: Create a work order.

OWNER: Person B (SCOPE.md item 7). Only Person B edits this file.
Form: Routine or Corrective, dates, problem report (Corrective only), and technicians.

Hint: INSERT INTO WORK_ORDER, then one WORK_ASSIGNMENT row per technician (use db.get_connection() to do both in one transaction).
"""
import streamlit as st

from views.placeholder import todo


def render():
    st.header("Create a work order")
    todo("B", 7, "Form: Routine or Corrective, dates, problem report (Corrective only), and technicians.")
