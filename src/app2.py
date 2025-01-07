import streamlit as st
import requests

API_URL = 'http://127.0.0.1:8000/'

def get_suggestions(query):
    data = {
  "recommendations": [
    {
      "restaurant_name": "Kafros Pizzeria",
      "review": "Amazing pizzas omg!",
      "rating": 3.4,
      "note": ""
    },
    {
      "restaurant_name": "Pizza Fellas",
      "review": "They make delicious pizza with nice ingredients on thin dough. Slice pizza and all pizza options are available. You can try two different flavors as a whole by making two different choices for the whole pizza. We wanted the mushroom and sausage. It was very nice; warm; and it was cooked in its consistency without drying the ingredients.",
      "rating": 3.8,
      "note": ""
    },
    {
      "restaurant_name": "Leman Kultur",
      "review": "Location is nice. We love it as a family. Pizza was delicious.",
      "rating": 4.2,
      "note": ""
    },
    {
      "restaurant_name": "Umut Pide",
      "review": "Nice pizza!",
      "rating": 3.9,
      "note": ""
    }
  ],
  "conclusion": "Based on the provided reviews, Kafros Pizzeria, Pizza Fellas, Leman Kultur, and Umut Pide are recommended for their delicious pizzas.  Miss Pizza has mixed reviews, with some praising its variety and others citing declining quality and service issues, so it has been excluded.  "
}
    return data['recommendations']

def get_answers(res_name, user_query):
    return f"some relevant answers to the query: {user_query} regarding {res_name}"

def get_summary(res_name):
    data = {
  "restaurant_name": "Pizza Fellas",
  "must_try_dishes": [
    "Mixed pizza",
    "Mushroom and sausage pizza",
    "Roast beef and mohair pizza"
  ],
  "highlights": [
    "Delicious pizzas with thin, tasty dough",
    "Option to create a half-and-half pizza with two different toppings",
    "Large pizza size, enough for two people",
    "Good ingredients",
    "Convenient location, close to parking",
    "Generally affordable prices",
    "Similar in taste to Italian pizzas"
  ],
  "things_to_note": [
    "Can get very crowded, requiring a wait",
    "Small and cramped seating area",
    "Some reviews mention a lack of napkins and wet wipes",
    "One review stated the pizza had only a doughy taste and lacked sufficient service for the price",
    "Service can be inconsistent based on reviews"
  ],
  "overall_conclusion": f"{res_name} is a popular pizzeria known for its delicious, thin-crust pizzas with a variety of topping options. While the quality of the pizza is generally praised, the small size of the restaurant and potential wait times are noteworthy.  The value for money appears to be a mixed experience based on reviews.  Despite some service inconsistencies, the overall experience seems positive for most customers.",
  "overall_rating": "3.5 out of 5"
}
    return data

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
st.write("A review based restaurant suggesting app")

def home():
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
        
        for i in st.session_state['suggestion']:
            with st.expander(f'#### {i['restaurant_name']}'):
                summary = get_summary(i['restaurant_name'])
                st.info(summary['overall_conclusion'])
                col1, col2, col3 = st.columns(3)
                col1.subheader("Must try dishes")
                for i in summary['must_try_dishes']:
                    col1.write(f'🍽️ {i}')
                col2.subheader("Highlights")
                for i in summary['highlights']:
                    col2.write(f'⭐ {i}')
                col3.subheader("Things to be noted")
                for i in summary['things_to_note']:
                    col3.write(f'⚠️ {i}')

        restaurant = st.sidebar.pills('suggested restaurants', options=res, selection_mode="single")
        st.session_state['restaurant'] = restaurant
                
        if st.session_state['restaurant']:
            with st.sidebar:
                for message in st.session_state['messages']:
                    with st.chat_message(message['role']):
                        st.markdown(message['content'])
            
                if prompt:=st.chat_input('Type here...'):
                    st.chat_message("user").markdown(prompt)
                    st.session_state['messages'].append({'role':'user','content':prompt})
                    response = get_answers(st.session_state['restaurant'], st.session_state['question'])
                    st.chat_message("assistant").markdown(response)
                    st.session_state['messages'].append({'role':'assistant','content':response})
        else:
            st.warning("⚠️ select a valid restaurant")               
    else:
        st.warning("⚠️ Enter a valid query")
        
def chat_bot():
    
    pass
        

    
    
    
    # st.sidebar.write(f'Enter your queries about {st.session_state['restaurant']}')
    # question = st.sidebar.chat_input('type here')
    # if question:
    #     st.session_state['question'] = question
    #     st.session_state['answer'] = get_answers(st.session_state['restaurant'], st.session_state['question'])
    #     st.sidebar.write(st.session_state['answer'])
    # else:
    #     st.info("🤖 Ask your doubts in the chatbot")

home()
