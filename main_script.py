import streamlit as st
from db import conn

def load_users():
    return conn.query("SELECT id, name, email, password, active FROM users ORDER BY name ASC", ttl=0)
