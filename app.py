"""Team 4: Oilfield Equipment Maintenance UI.

SHARED FILE: this only wires the screens together. Each screen lives in its own
file under views/person_a/ or views/person_b/, so we never edit the same file.

To add a new screen: import its module below and add one st.Page line to PAGES.
Start the app with:  streamlit run app.py
"""
import streamlit as st

from views.person_a import home, equipment, work_orders, query_highlights, equipment_history
from views.person_b import add_inspection, report_problem, create_work_order, complete_work_order, change_status


def page(module, title, icon, url):
    # Every screen module has a render() function; url_path must be unique
    return st.Page(module.render, title=title, icon=f":material/{icon}:", url_path=url)


PAGES = {
    "Look Up": [
        page(home, "Home", "home", "home"),
        page(equipment, "Equipment", "precision_manufacturing", "equipment"),
        page(work_orders, "Work Orders", "assignment", "work-orders"),
        page(query_highlights, "Reports", "query_stats", "reports"),
        page(equipment_history, "Equipment History", "history", "equipment-history"),
    ],
    "Record Work": [
        page(add_inspection, "Add an Inspection", "fact_check", "add-inspection"),
        page(report_problem, "Report a Problem", "report_problem", "report-problem"),
        page(create_work_order, "Create a Work Order", "add_task", "create-work-order"),
        page(complete_work_order, "Complete a Work Order", "task_alt", "complete-work-order"),
        page(change_status, "Change Work Order Status", "sync_alt", "change-status"),
    ],
}

st.set_page_config(page_title="Team 4 Oilfield Maintenance", page_icon=":material/oil_barrel:", layout="wide")
st.navigation(PAGES).run()
