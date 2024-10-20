import google.generativeai as genai
from chromadb import Documents, EmbeddingFunction, Embeddings
import os
import chromadb
from typing import List
from dotenv import load_dotenv
import sys
import os

# Thêm đường dẫn đến thư mục 'RAG'
sys.path.append(os.path.join(os.path.dirname(__file__), 'RAG'))

# Import từ package RAG
from RAG.Loadfile import loadfilecsv, convertDocument
from RAG.Embbeding import get_relevant_passage, load_chroma_collection, create_chroma_db, db
from RAG.Generation import generate_answer, generate_answer_from_prompt

def result(query) -> str:
    return generate_answer(db, query=query)
    
# print(result('To Kill a Mockingbird'))
