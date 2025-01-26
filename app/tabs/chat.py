import streamlit as st
from objs.plotter import Plotter
from objs.database import Database

import os
from static.prompts import code_template, non_sql_code_template


def chat():
    if 'plotter' not in st.session_state:
        st.session_state['plotter'] = Plotter()

    if 'database' not in st.session_state:
        st.session_state['database'] = Database()

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []  # To store chat history

    # Chat header
    st.title("Interactive Plotter Chat")

    # Display previous messages
    for message in st.session_state['messages']:
        with st.chat_message(message["role"]):  # "assistant" or "user"
            st.markdown(message["content"])

    # Database selection
    database = st.selectbox('Choose a database to work with',
                            st.session_state['database'].get_added_databases())
    dbms = st.session_state['database'].get_dbms(database)
    if not dbms:
        st.write('Database not found. Please add a new database configuration.')
        return
    # Chat input box
    if prompt := st.chat_input("What do you want to plot?"):
        # Save user input to chat history
        st.session_state['messages'].append(
            {"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Begin response
        with st.chat_message("assistant"):
            st.markdown("Fetching data from the database...")

        # Generate SQL query
        sql_query = st.session_state['plotter'].generate_sql_query(
            prompt, database, dbms)
        with st.chat_message("assistant"):
            st.markdown(f"Here is the generated SQL query:\n```sql\n{sql_query}\n```")

        if sql_query != 'I do not know.':
            # Generate Python code for plotting
            st.chat_message("assistant").markdown(
                "Generating code for the plot...")
            code = st.session_state['plotter'].generate_code(
                prompt, sql_query, dbms)
            st.chat_message("assistant").markdown(
                f"Here is the generated code:\n```python\n{code}\n```")

            # Execute the Python code to create the plot
            message, status = st.session_state['plotter'].execute_code(
                'plot.py', code_template, sql_query, code, database, dbms
            )

            if status == 0:  # If no errors occurred
                st.chat_message("assistant").markdown("Here is your plot:")
                st.chat_message("assistant").image('plot.png')
            else:
                st.chat_message("assistant").markdown(
                    f"An error occurred during code execution:\n```\n{message.decode()}\n```")

        
