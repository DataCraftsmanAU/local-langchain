import requests
import streamlit as st

API_URL = "http://localhost:3000/api/v1/prediction/eca139de-abcc-46ea-b264-f05b31b1d9ba"

def query(payload):
    response = requests.post(API_URL, json=payload)
    return response.json()
 
question = st.text_area('Query:')

button = st.button("Submit")

if button:
    output = query({
        "question": question
    })

    st.write(output['text'])