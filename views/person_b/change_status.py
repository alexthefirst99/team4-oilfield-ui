"""Screen: Change work order status.

OWNER: Person B (SCOPE.md item 12). Only Person B edits this file.
(Nice) Move an order from Open to In Progress or Cancelled.

Hint: UPDATE WORK_ORDER SET WO_STATUS. The BR15 trigger blocks In Progress with no technician.
"""
import streamlit as st

from views.placeholder import todo


def render():
    st.header("Change work order status")
    todo("B", 12, "(Nice) Move an order from Open to In Progress or Cancelled.")
