"""Screen: Work orders.

OWNER: Person A (SCOPE.md item 3). Only Person A edits this file.
List work orders with their equipment and assigned technicians. Filter by status.

Hint: Join WORK_ORDER, EQUIPMENT, WORK_ASSIGNMENT, and TECHNICIAN. Filter: WO_STATUS.
"""
import streamlit as st

from views.placeholder import todo


def render():
    st.header("Work orders")
    todo("A", 3, "List work orders with their equipment and assigned technicians. Filter by status.")
