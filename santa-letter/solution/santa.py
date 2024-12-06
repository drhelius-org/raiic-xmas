import streamlit as st
import requests

st.title("Write a Letter to Santa Claus")

st.header("Dear Santa Claus,")

name = st.text_input("Your Name:")
age = st.number_input("Your Age:", min_value=0, step=1)
behavior = st.selectbox("How have you been this year?", ["Very Good", "Good", "Okay", "Not So Good", "Bad"])
letter_content = st.text_area("Write your letter here:")

if st.button("Send Letter"):
    if name and age and letter_content:
        response = requests.post("http://localhost:8000/send_letter", json={
            "name": name,
            "age": age,
            "behavior": behavior,
            "letter_content": letter_content
        })
        if response.status_code == 200:
            st.success("Your letter has been sent to Santa Claus!")
            santa_response = response.json().get("santa_response", "")
            if santa_response:
                st.subheader("Santa's Response:")
                st.write(santa_response)
        else:
            st.error("There was an error sending your letter. Please try again.")
    else:
        st.error("Please provide your name, age, and write something in the letter before sending.")