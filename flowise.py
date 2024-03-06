import requests
import streamlit as st

API_URL = "http://localhost:3000/api/v1/prediction/7dc1cf7a-1baf-47d4-acec-03fa0914a239"
headers = {"Authorization": "Bearer 08GlvWppUHU6OhQqqGouPgt7QOjvPwbM3YhLqttDLwg="}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

question = st.text_input("What is your favorite public holiday? We will recommend a recipe.")
if question:
    output = query({"question": question})
    st.write(output['text'])
