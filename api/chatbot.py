from llama_index.vector_stores.elasticsearch import ElasticsearchStore
from llama_index.core import Document, Settings, VectorStoreIndex, QueryBundle,StorageContext, load_index_from_storage
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

while True:
    user_query = input("Enter your query: ")
    if user_query.lower() == "exit":
        break
    bundle = QueryBundle(query_str=user_query, embedding=Settings.embed_model.get_query_embedding(query=user_query))
    response = query_engine.query(bundle)
    response = query_engine.query(user_query)
    print(response)