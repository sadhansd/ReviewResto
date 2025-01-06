import streamlit as st

st.set_page_config(
    page_icon=':cook:',
    page_title='ReviewResto',
    layout='centered'
)

st.title("I love vicky")
name = st.text_input("enter name: ")
st.write("vicky loves ",name)