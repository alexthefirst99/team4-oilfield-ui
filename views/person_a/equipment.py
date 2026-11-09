"""Screen: Equipment.

OWNER: Person A (SCOPE.md item 2). Only Person A edits this file.
List every equipment item with its site and type. Filter by site and status.

Hint: Join EQUIPMENT, SITE, and EQUIPMENT_TYPE. Filters: SITE_NAME and EQUIP_STATUS.
"""
import streamlit as st

from views.placeholder import todo


def render():
    st.header("Equipment")
    todo("A", 2, "List every equipment item with its site and type. Filter by site and status.")
