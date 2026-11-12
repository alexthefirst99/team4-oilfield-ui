"""Table display helper for Person A's screens.

OWNER: Person A. Shows everyday column names, colors status words, and sizes
tables so short tables show every row without scrolling. Person B can import
show_table() too.
"""
import streamlit as st

# Database column names -> words a non-technical user understands
LABELS = {
    "EQUIP_ASSET_TAG": "Asset tag", "EQUIP_NAME": "Equipment", "TYPE_NAME": "Type",
    "SITE_NAME": "Site", "SITE_LOCATION": "Location", "EQUIP_STATUS": "Status",
    "EQUIP_INSTALL_DATE": "Installed",
    "WO_ID": "Order #", "WO_DESCRIPTION": "Description", "WO_TYPE": "Type", "WO_STATUS": "Status",
    "WO_CREATED_DATE": "Created", "WO_DUE_DATE": "Due", "TECHNICIANS": "Technicians",
    "INSP_DATE": "Date", "INSP_RESULT": "Result", "INSP_NOTES": "Notes", "TECHNICIAN": "Technician",
    "PROB_REPORT_DATE": "Reported", "PROB_PRIORITY": "Priority", "PROB_DESCRIPTION": "Problem",
    "MAINT_COMPLETION_DATE": "Completed", "MAINT_WORK_PERFORMED": "Work done",
    "TECH_ID": "Technician #", "TECH_FNAME": "First name", "TECH_LNAME": "Last name",
    "PART_ID": "Part #", "PART_NUMBER": "Part number", "PART_NAME": "Part", "PART_UNIT": "Unit",
    "USAGE_QTY": "Quantity",
    # names our Phase 3 queries give their results
    "numInspections": "Inspections", "totalQty": "Total used", "numWorkOrders": "Work orders",
    "numProblems": "Problem reports", "numRepairs": "Completed repairs",
    "daysToComplete": "Days to finish", "avgDaysForType": "Average days for this type",
}

# Text colors for status-like words (same palette as the slides)
COLORS = {
    "Operational": "#3F6B4E", "Out of Service": "#C2410C", "Retired": "#5B6B73",
    "Open": "#0F4C5C", "In Progress": "#C2410C", "Completed": "#3F6B4E", "Cancelled": "#5B6B73",
    "Pass": "#3F6B4E", "Needs Maintenance": "#C2410C", "Fail": "#9A3412",
    "Low": "#5B6B73", "Medium": "#0F4C5C", "High": "#C2410C",
}
COLORED_COLUMNS = ["Status", "Result", "Priority"]


def _color(value):
    color = COLORS.get(value)
    return f"color: {color}; font-weight: 600" if color else ""


def show_table(df, max_rows_without_scroll=15):
    """Show a DataFrame with everyday headers, colored status words, and no index."""
    df = df.rename(columns=LABELS)
    styled = df.style.map(_color, subset=[c for c in COLORED_COLUMNS if c in df.columns])
    # 35 px per row + header: tall enough that short tables never scroll
    height = 35 * (len(df) + 1) + 3 if len(df) <= max_rows_without_scroll else "auto"
    st.dataframe(styled, hide_index=True, height=height)
