"""MySQL connection helpers.

OWNER: Person A (SCOPE.md item 1). Build this first and push it, because every
screen uses it. Person B can already write forms against these function names.

The login comes from .streamlit/secrets.toml (copy secrets.example.toml).
Never commit secrets.toml.
"""
import streamlit as st


def get_connection():
    """Return an open connection to the oilfield_maintenance database.

    TODO (Person A): connect with mysql.connector using st.secrets["mysql"].
    Person B can also use this for saves that need several INSERTs together
    (for example a work order plus its technicians).
    """
    raise NotImplementedError("Person A: write get_connection() in db.py")


def fetch_df(sql, params=None):
    """Run a SELECT and return the rows as a pandas DataFrame.

    TODO (Person A)
    """
    raise NotImplementedError("Person A: write fetch_df() in db.py")


def execute(sql, params=None):
    """Run one INSERT or UPDATE, commit it, and return the new row's id (lastrowid).

    Do not catch mysql.connector.Error here. Let it go up so the screen can show
    it with errors.show_db_error().

    TODO (Person A)
    """
    raise NotImplementedError("Person A: write execute() in db.py")
