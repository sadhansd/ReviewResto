from fastapi import FastAPI, HTTPException
from rag import get_suggestions,get_summary,general_qna
import uvicorn
import json
from pydantic import BaseModel

from typing import Optional
from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.core import Document, Settings, VectorStoreIndex, QueryBundle, StorageContext, load_index_from_storage
from llama_index.llms.gemini import Gemini
from llama_index.embeddings.gemini import GeminiEmbedding

import os
API_KEY = os.environ['GEMINI_API_KEY']
embed_model = GeminiEmbedding(model_name='models/text-embedding-004', api_key=API_KEY)
Settings.embed_model = embed_model

llm = Gemini(model='models/gemini-1.5-flash', api_key=API_KEY)
storage_context = StorageContext.from_defaults(persist_dir="notebooks/storage")
index = load_index_from_storage(storage_context=storage_context, index_id="vector_index")
query_engine = index.as_query_engine(llm, similarity_top_k=10)

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    restaurant: Optional[str] = None

class QueryResponse(BaseModel):
    response: str

@app.get('/')
def home():
    return {'message': 'connected'}

@app.get("/suggest")
async def suggest_restaurant(query: str):
    result = get_suggestions(query)
    res = result.split('```json')[1].split('```')[0]
    result = json.loads(res)
    return result

@app.get("/summary/{restaurant_name}")
async def summarize(restaurant_name: str):
    res = get_summary(restaurant_name)
    res = res.split('```json')[1].split('```')[0]
    res = json.loads(res)
    return res

@app.post("/query")
async def query_index(request: QueryRequest):
    try:
        if request.restaurant:
            user_query = request.query
            bundle = QueryBundle(query_str=user_query, embedding=Settings.embed_model.get_query_embedding(query=user_query))
            response = query_engine.query(bundle)
            return response
        else:
            user_query = request.query
            res = general_qna(user_query)
            res = res.split('```json')[1].split('```')[0]
            res = json.loads(res)
            return {"response":res["answer"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
    
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
