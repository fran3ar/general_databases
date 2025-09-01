import streamlit as st

# Crear la conexión UNA SOLA VEZ
conn = st.connection("pg_db", type="sql")
