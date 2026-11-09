"""Shared helper for screens that are not built yet. Delete the todo() call
from a screen once that screen works."""
import streamlit as st


def todo(person, item, what):
    st.info(f"Not built yet. Person {person}, SCOPE.md item {item}: {what}")
