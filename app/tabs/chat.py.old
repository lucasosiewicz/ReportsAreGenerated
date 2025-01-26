import streamlit as st
from objs.plotter import Plotter
from objs.database import Database

from static.prompts import code_template


def chat():
    if 'plotter' not in st.session_state:
        st.session_state['plotter'] = Plotter()

    if 'database' not in st.session_state:
        st.session_state['database'] = Database()

    database = st.selectbox('Choose a database which you want to work with', st.session_state['database'].get_added_databases())
    dbms = st.session_state['database'].get_dbms(database)
    if not dbms:
        st.write('Database not found. Please add a new database configuration.')
        return

    with st.form('genAI'):
        query = st.text_area('What do You want to plot?')
        submit = st.form_submit_button('Generate plot!')

        if submit:
            st.write('Fetching data from database...')
            sql_query = st.session_state['plotter'].generate_sql_query(query, database, dbms)
            st.write(sql_query)
            if sql_query != 'I do not know.':
                st.write('Generating plot...')
                code = st.session_state['plotter'].generate_code(query, sql_query, dbms)
                st.write(code)
                message, status = st.session_state['plotter'].execute_code('plot.py', code_template, sql_query, code, database, dbms)
                st.image('plot.png')
                submit = False