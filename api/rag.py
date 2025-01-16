from elasticsearch import Elasticsearch
es = Elasticsearch('http://localhost:9200/')
import google.generativeai as genai
import os
API_KEY = os.environ['GEMINI_API_KEY']
genai.configure(api_key=API_KEY )

def create_embedding(text):
    result = genai.embed_content(model="models/text-embedding-004", content=text)
    return result['embedding']

def get_context(query):
    vector = create_embedding(query)
    knn = {
        'field': "review_vector",
        'query_vector': vector,
        'k':50
    }
    res = es.search(index='reviews', knn=knn, source=['restaurant_name','review'])
    documents = []
    for doc in res['hits']['hits']:
        documents.append(str(doc['_source']))
    return documents

def get_suggestions(query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    documents = get_context(query)
    output_format = "json format(recommendations: {restaurant_name, review, note}. conclusion). the output should contain top recommendations with review text and note (only if there is any negative review). at last a conclusion. note: donot recommend a restaurant if there is negative opinion"
    prompt = f"You are a resturant suggestor. suggest resturants based on the given data'{query}'.\n\data:\n{''.join(documents)}. output format: {output_format}. donot repeat same restaurant in the output"
    response = model.generate_content(prompt)
    return response.text

def get_res_reviews(name):
    query = {
        "size":1000,
    "query":{
        "match":{
            "restaurant_name":name
            }
        }
    }
    res = es.search(index="reviews", body=query,source=['restaurant_name','review'])
    documents = []
    for doc in res['hits']['hits']:
        documents.append(str(doc['_source']))
    return documents

def get_summary(name):
    model = genai.GenerativeModel("gemini-1.5-flash")
    documents = get_res_reviews(name)
    output_format = "output in json format(restaurant_name, must_try_dishes, highlights, things to note, conclusion, rating). the output should contain best dishes to try(if have data). highlights(if data available). points to keep in mind(if have negative data). at last overall conclusion and overall rating"
    prompt = f"You are a resturant suggestor. you provide summary of the given restaurant:'{name}' based on given reviews.\n\reviews:\n{''.join(documents)}. output format{output_format}"
    response = model.generate_content(prompt)
    return response.text

def restaurant_qna(name, query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    documents = get_res_reviews(name)
    output_format = "json contains restaurant name and answer."
    prompt = f"You are a resturant suggestor.Answer the user's query:'{query} on a restaurant':'{name}' based on given reviews.\n\reviews:\n{''.join(documents)}. output format: {output_format}"
    response = model.generate_content(prompt)
    return response.text

def general_qna(query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    output_format = "json contains answer."
    prompt = f"Answer the user's general query:'{query} output in the provided format. output format: {output_format}"
    response = model.generate_content(prompt)
    return response.text