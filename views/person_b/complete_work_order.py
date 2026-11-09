"""Screen: Complete a work order.

OWNER: Person B (SCOPE.md item 8). Only Person B edits this file.
Form: pick an order, completion date, work performed, and parts used.

Hint: INSERT INTO MAINTENANCE_RECORD, then PART_USAGE rows. Our trigger sets the order to Completed. Demo: an order with no technician shows the BR15 message.
"""
import streamlit as st

from views.placeholder import todo


def render():
    st.header("Complete a work order")
    todo("B", 8, "Form: pick an order, completion date, work performed, and parts used.")
