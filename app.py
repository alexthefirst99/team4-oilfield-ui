"""Team 4: Oilfield Equipment Maintenance UI.

SHARED FILE: this only wires the screens together. Each screen lives in its own
file under views/person_a/ or views/person_b/, so we never edit the same file.

To add a new screen: import its module below and add one line to SCREENS.
Start the app with:  streamlit run app.py
"""
import streamlit as st

from views.person_a import home, equipment, work_orders, query_highlights, equipment_history
from views.person_b import add_inspection, report_problem, create_work_order, complete_work_order, change_status

# Sidebar label -> screen module. Every module has a render() function.
SCREENS = {
    "View data": {
        "Home": home,
        "Equipment": equipment,
        "Work orders": work_orders,
        "Query highlights": query_highlights,
        "Equipment history (nice)": equipment_history,
    },
    "Add or change data": {
        "Add an inspection": add_inspection,
        "Report a problem": report_problem,
        "Create a work order": create_work_order,
        "Complete a work order": complete_work_order,
        "Change work order status (nice)": change_status,
    },
}

st.set_page_config(page_title="Team 4 Oilfield Maintenance", layout="wide")
st.sidebar.title("Team 4: Oilfield Maintenance")

group = st.sidebar.radio("Section", list(SCREENS))
choice = st.sidebar.radio("Screen", list(SCREENS[group]))
SCREENS[group][choice].render()
