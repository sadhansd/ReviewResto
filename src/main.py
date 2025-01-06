import streamlit as st
import requests

API_KEY = 'http://127.0.0.1:8000/'

st.set_page_config(
    page_icon=':cook:',
    page_title='ReviewResto',
    layout='centered'
)

st.title("ReviewResto")
query = st.text_input('Enter your queries', placeholder='eg: Suggest a affordable pizza spot')

if st.button("Search",icon='🔍'):
    response = requests.get(f'{API_KEY}/suggest?query={query}')
    result = response.json()
    for i in result['recommendations']:
        st.markdown(f'### {i['restaurant_name']}')
        st.write(i['review'])
        st.markdown('---')
    st.success(result['conclusion'])