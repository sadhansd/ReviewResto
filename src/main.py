import streamlit as st
from elasticsearch import Elasticsearch
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

es = Elasticsearch('http://localhost:9200/')

def search(input_word):
    vector = model.encode(input_word)
    query = {
    'field': "review_vector",
    'query_vector': vector,
    'k':3,
    'num_candidates':25
    }

    res = es.knn_search(index='reviews', knn=query, source=['name','rating','review_text'])
    return res['hits']['hits']


def main():
    st.title("ReviewResto")
    search_query = st.text_input("What kind of place")
    if st.button("Search"):
        if search_query:
            # Perform the search and get results
            results = search(search_query)

            # Display search results
            st.subheader("Results")
            for result in results:
                with st.container():
                    if '_source' in result:
                        try:
                            st.header(f"{result['_source']['name']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.write(f"Review: {result['_source']['review_text']}")
                        except Exception as e:
                            print(e)
                        
                        try:
                            st.metric('Ratings', f'{result['_source']['rating']}⭐')
                        except Exception as e:
                            print(e)
                        st.divider()

if __name__ == '__main__':
    main()