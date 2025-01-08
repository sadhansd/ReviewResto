import streamlit as st
import requests

API_URL = 'http://127.0.0.1:8000/'

def get_suggestions(query):
    response = requests.get(f'{API_URL}/suggest?query={query}')
    if response.status_code == 200:
        result = response.json()
        return result['recommendations']
    else:
        st.error("Failed to fetch")
        return None

def get_answers(res_name, user_query):
    payload = {"query": user_query+f" in {res_name}"}
    response = requests.post(f'{API_URL}/query', json=payload)
    if response.status_code == 200:
        result = response.json()
        return result["response"]
    else:
        st.error("Failed to fetch")
        return "No answers available"

st.set_page_config(
    page_icon=':cook:',
    page_title='ReviewResto',
    layout='centered'
)

if "query" not in st.session_state:
    st.session_state['query'] = ""
    
if "suggestion" not in st.session_state:
    st.session_state['suggestion'] = {}
    
if "restaurant" not in st.session_state:
    st.session_state['restaurant'] = None
    
if "question" not in st.session_state:
    st.session_state['question'] = ""
    
if "answer" not in st.session_state:
    st.session_state['answer'] = ""

    

st.title("ReviewResto")
st.write("A review based restaurant suggesting app")

col1, col2 = st.columns([3,1],vertical_alignment="bottom")

query = col1.text_input('What do you look for', placeholder='eg: Suggest a affordable pizza spot')

if col2.button("Search",icon='🔍'):
    if query:
        st.session_state['query'] = query
        st.session_state['suggestion'] = get_suggestions(query)
    else:
        st.warning("⚠️ Enter a valid query")
        
if st.session_state['suggestion']:
    res = [i['restaurant_name'] for i in st.session_state['suggestion']]
    rev = [f'🙍‍♂️: {i['review']}' for i in st.session_state['suggestion']]
    restaurant = st.radio("select a restaurant", res, captions=rev)
    st.session_state['restaurant'] = restaurant
            
    if st.session_state['restaurant']:
        col3, col4 = st.columns([3,1],vertical_alignment="bottom")
        question = col3.text_input(f'Enter your queries about {st.session_state['restaurant']}', placeholder='eg: what are the must try dishes')
        if col4.button("Get answers"):
            if question:
                st.session_state['question'] = question
                st.session_state['answer'] = get_answers(st.session_state['restaurant'], st.session_state['question'])
                st.write(st.session_state['answer'])
            else:
                st.warning("⚠️ Enter a valid question")
    else:
        st.warning("⚠️ select a valid restaurant")               
else:
    st.warning("⚠️ Enter a valid query")
