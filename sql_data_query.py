import os
import logging
import psycopg2
import pandas as pd
from openai import OpenAI
import streamlit as st
from credentials import *


# Point to the local server
OPENAI_BASE_URL = "http://localhost:1234/v1"
client = OpenAI(base_url=OPENAI_BASE_URL, api_key="not-needed")

# Function to establish a connection to the database
def create_database_connection():
    conn = psycopg2.connect(dbname=DB_NAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
    return conn


# Function to get all available tables from the database
def get_available_tables():
    conn = create_database_connection()
    # Create a cursor object
    cursor = conn.cursor()
    # Load the schema and table into a pandas DataFrame
    df = pd.read_sql_query("SELECT table_name FROM information_schema.tables WHERE table_schema = 'jobscraper';", conn)
    # Close the database connection
    conn.close()
    return df['table_name'].tolist()

# Function to establish a connection to the database and load data from the specified table into a DataFrame
def load_data_from_db(table_name):
    conn = create_database_connection()
    # Create a cursor object
    cursor = conn.cursor()
    # Load the schema and table into a pandas DataFrame
    df = pd.read_sql_query(f"SELECT * FROM jobscraper.{table_name};", conn)
    # Close the database connection
    conn.close()
    return df
        
def generate_insights(dataframe, question):
    system_message = """The user will provide you with a dataframe and a question to answer. Do your best to answer them correctly and do not answer with any code."""
    user_message = f"Question: {question} Data: {dataframe}"
    completion = client.chat.completions.create(
        model="local-model",  # this field is currently unused
        messages=[{"role": "system", "content": system_message}, {"role": "user", "content": user_message}],
        temperature=0.7,
    )
    message = completion.choices[0].message
    return message.content    

# Streamlit app setup
available_tables = get_available_tables()
selected_table = st.selectbox("Select a table", available_tables)
dataframe = load_data_from_db(selected_table)
dataframe
question = st.text_input("Enter your question:")
if st.button("Generate Insights"):
    insights = generate_insights(dataframe, question)
    st.write(insights)