"""MySQL connection helpers.

OWNER: Person A (SCOPE.md item 1). Every screen gets its data through these
three functions, so keep their names and inputs the same.

The login comes from .streamlit/secrets.toml (copy secrets.example.toml).
Never commit secrets.toml.
"""
import mysql.connector
import pandas as pd
import streamlit as st


def get_connection():
    """Return an open connection to the oilfield_maintenance database.

    Use this directly only for saves that need several statements in one
    transaction (for example a work order plus its technicians). Close it when done.
    """
    return mysql.connector.connect(**st.secrets["mysql"])


def fetch_df(sql, params=None):
    """Run a SELECT and return the rows as a pandas DataFrame."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        columns = [col[0] for col in cur.description]
        return pd.DataFrame(cur.fetchall(), columns=columns)
    finally:
        conn.close()


def execute(sql, params=None):
    """Run one INSERT or UPDATE, commit it, and return the new row's id (lastrowid).

    mysql.connector.Error is not caught here, so the screen can show it
    with errors.show_db_error().
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(sql, params or ())
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()
