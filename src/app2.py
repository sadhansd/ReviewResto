import streamlit as st
import requests

API_URL = 'http://127.0.0.1:8000/'

@st.cache_data
def get_suggestions(query):
    
    response = requests.get(f'{API_URL}/suggest?query={query}')
    if response.status_code == 200:
        result = response.json()
        return result['recommendations']
    else:
        st.error("Failed to fetch")
        return None

@st.cache_data
def get_answers(res_name, user_query):
    if res_name == 'general':
        payload = {"query": user_query}
    else:
        payload = {"query": user_query+f" in {res_name}", "restaurant":res_name}
    response = requests.post(f'{API_URL}/query', json=payload)
    if response.status_code == 200:
        result = response.json()
        return result["response"]
    else:
        st.error("Failed to fetch")
        return "No answers available"

@st.cache_data
def get_summary(res_name):
    response = requests.get(f'{API_URL}/summary/{res_name}')
    if response.status_code == 200:
        result = response.json()
        return result
    else:
        st.error("Failed to fetch")
        return None

st.set_page_config(
    page_icon=':cook:',
    page_title='ReviewResto',
    layout='wide'
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
    
if "messages" not in st.session_state:
    st.session_state['messages'] = []

    

st.title("ReviewResto")
st.caption("A review based restaurant suggesting app")

def home():
    col1, col2 = st.columns([3,1],vertical_alignment="bottom")

    query = col1.text_input('What do you look for', placeholder='eg: Suggest a affordable pizza spot')

    if col2.button("Search",icon='🔍'):
        if query:
            st.session_state['query'] = query
            suggestions = get_suggestions(query)
            st.session_state['suggestion'] = list(set([i['restaurant_name'] for i in suggestions]))
        else:
            st.warning("⚠️ Enter a valid query")
            
    if st.session_state['suggestion']:

        for i in st.session_state['suggestion']:
            with st.expander(f'#### {i}'):
                col1, col2 = st.columns([8,1])
                summary = get_summary(i)
                col1.info(summary['conclusion'])
                # col2.metric('Rating',summary['overall_rating'].split(' ')[0])
                tab1, tab2, tab3 = st.tabs(["Must try dishes", "Highlights", "Things to be noted"])
                with tab1:
                    for i in summary['must_try_dishes']:
                        st.write(f'🍽️ {i}')
                with tab2:
                    for i in summary['highlights']:
                        st.write(f'⭐ {i}')
                with tab3:
                    for i in summary['things_to_note']:
                        st.write(f'⚠️ {i}')
                st.success("🤖 Ask your queries in the chatbot")
                
        restaurant = st.sidebar.pills('select a restaurant and ask queries', options=st.session_state['suggestion']+['general'], selection_mode="single")
        st.session_state['restaurant'] = restaurant
                
        if st.session_state['restaurant']:
            chat_bot()
        else:
            st.success("Click on the suggested restaurants to learn more")               

        
def chat_bot():
    with st.sidebar:
                st.title(f"Ask questions about {st.session_state['restaurant']}")
                user_input = st.chat_input("Type your message here...")
                if user_input:

                    bot_response = get_answers(st.session_state['restaurant'], user_input)
                    chat = [{"role": "user", "content": user_input},{"role": "assistant", "content": f':blue-background[{st.session_state['restaurant']}]: {bot_response}'}]
                    st.session_state.messages.append(chat)

                chat_container = st.container()
                with chat_container:
                    for chat in reversed(st.session_state.messages):
                        with st.container(border=True):
                            st.chat_message(chat[0]['role'], avatar="🧑").markdown(f'**{chat[0]['content']}**')
                        
                        st.chat_message(chat[1]['role'], avatar="🤖").markdown(chat[1]['content'])

with st.spinner('Fetching your data...⌛'):
    home()
