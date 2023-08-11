from typing import TextIO

import openai
import pandas as pd
import streamlit as st
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI

openai.api_key = st.secrets["OPENAI_API_KEY"]

def get_answer_csv(file: TextIO, query: str) -> str:
    """
    Returns the answer to the given query by querying a CSV file.

    Args:
    - file (str): the file path to the CSV file to query.
    - query (str): the question to ask the agent.

    Returns:
    - answer (str): the answer to the query from the CSV file.
    """
    # Load the CSV file as a Pandas dataframe
    df = pd.read_csv(file)
    # Create an agent using OpenAI and the Pandas dataframe
    agent = create_pandas_dataframe_agent(OpenAI(temperature=0), df, verbose=False)

    # Run the agent on the given query and return the answer
    answer = agent.run(query)
    return answer


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    system_msg = ""

    st.header("CSV Bot")
    uploaded_file = st.file_uploader("Upload a csv file", type=["csv"])

    if uploaded_file is not None:
        query = st.text_area("Ask any question related to the document")
        button = st.button("Submit")
        if button:
            st.write(get_answer_csv(uploaded_file, query))