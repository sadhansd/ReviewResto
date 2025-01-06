from fastapi import FastAPI
from rag import get_suggestions,get_summary,restaurant_qna
import uvicorn
import json

app = FastAPI()

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

@app.get("/{restaurant_name}")
async def answer(restaurant_name: str, query: str):
    res = restaurant_qna(restaurant_name, query)
    res = res.split('```json')[1].split('```')[0]
    res = json.loads(res)
    return res

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
