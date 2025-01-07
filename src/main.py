import streamlit as st
import requests

API_KEY = 'http://127.0.0.1:8000/'

st.set_page_config(
    page_icon=':cook:',
    page_title='ReviewResto',
    layout='centered'
)

st.title("ReviewResto")
query = st.text_input('What do you look for', placeholder='eg: Suggest a affordable pizza spot')

if st.button("Search",icon='🔍'):
    response = requests.get(f'{API_KEY}/suggest?query={query}')
    result = response.json()
    st.info(result['conclusion'])
    st.subheader("Suggestions...")
    restaurants = [i['restaurant_name'] for i in result['recommendations']]
    res_name = st.radio("Select a restaurant",restaurants)
    
    user_query = st.text_input('Enter your queries', placeholder='eg: Suggest a affordable pizza spot')
    if st.button("Submit Query", type='primary'):
        payload = {"query": user_query+f" in {res_name}"}
        response = requests.post(f'{API_KEY}/query', json=payload)
        if response.status_code==200:
            result = response.json()
            st.write(result['response'])
