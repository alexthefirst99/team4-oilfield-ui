"""Show database errors on screen.

OWNER: Person B (SCOPE.md item 9). Every form calls show_db_error() when MySQL
blocks a save (a trigger or a CHECK), so the app shows a message instead of crashing.
"""
import streamlit as st


def show_db_error(err):
    """Show a MySQL error in plain words.

    TODO (Person B): for trigger errors (SQLSTATE 45000) show only our message,
    for example "BR15: Assign at least one technician ...".
    The line below already works, it just shows the raw error.
    """
    st.error(f"The database blocked this save: {err}")
