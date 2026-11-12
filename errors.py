import re

import streamlit as st

CHECK_MESSAGES = {
    "CK_INSP_RESULT": "The inspection result must be Pass, Needs Maintenance, or Fail.",
    "CK_PROB_PRIORITY": "The priority must be Low, Medium, or High.",
    "CK_WO_TYPE": "The work order type must be Routine or Corrective.",
    "CK_WO_STATUS": "The work order status must be Open, In Progress, Completed, or Cancelled.",
    "CK_WO_TYPE_PROBLEM": "BR14: Corrective work needs a problem report, and Routine work cannot have one.",
    "CK_WO_DUE_DATE": "The due date cannot be before the created date.",
    "CK_USAGE_QTY": "The part quantity must be greater than 0.",
    "CK_PART_UNIT": "The part unit must be each, liter, or meter.",
    "CK_EQUIP_STATUS": "The equipment status must be Operational, Out of Service, or Retired.",
}

CONNECTION_ERRNOS = {1045, 1049, 2003, 2005, 2013}


def show_db_error(err):
    """Show a MySQL error (mysql.connector.Error) in plain words."""
    errno = err.errno
    sqlstate = err.sqlstate
    msg = err.msg

    if sqlstate == "45000":
        st.error("Blocked by a business rule. " + msg)
    elif errno == 3819:
        match = re.search(r"'([^']+)'", msg)
        name = match.group(1) if match else ""
        st.error(CHECK_MESSAGES.get(name, "Blocked by a CHECK rule. " + msg))
    elif errno == 1062:
        if "UQ_MAINTENANCE_RECORD_WO" in msg:
            st.error("This work order already has a maintenance record.")
        else:
            st.error("This record already exists. " + msg)
    elif errno == 1452:
        st.error("Bad link: the record you picked does not exist in the database. " + msg)
    elif errno in CONNECTION_ERRNOS:
        st.error("Could not reach the database. Check that MySQL is running and that "
                 ".streamlit/secrets.toml has the right login. " + msg)
    else:
        st.error(msg)

    st.caption(f"Nothing was saved. MySQL error {errno} (SQLSTATE {sqlstate})")
