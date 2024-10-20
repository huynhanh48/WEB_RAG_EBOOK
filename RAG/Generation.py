import google.generativeai as genai
from chromadb import Documents, EmbeddingFunction, Embeddings
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import chromadb
from typing import List
from dotenv import load_dotenv
from RAG.Loadfile import loadfilecsv, convertDocument
from RAG.Embbeding import get_relevant_passage, load_chroma_collection, create_chroma_db, db

def make_rag_prompt(query, relevant_passage):
    if isinstance(relevant_passage, list) and len(relevant_passage) > 0:
        relevant_passage = relevant_passage[0]
        prompt = ("""
        'system': Bạn là nhân viên sách để hỗ trợ người dùng trả lời câu hỏi. 
        Nếu thông tin từ câu hỏi và câu trả lời có sự liên quan, bạn hãy mô tả trả lời 
        cho người dùng dễ hiểu về nội dung tóm tắt của sách và đề xuất giá sách hoặc hỏi 
        khách hàng cần thông tin gì nữa không. 
        Trường hợp câu hỏi query không liên quan đến câu tham khảo passage hoặc không tìm thấy 
        thông tin phù hợp trong cơ sở dữ liệu, hãy sử dụng kiến thức bên ngoài của bạn để 
        trả lời một cách chính xác và dễ hiểu nhất.

        Lưu ý: không sử dụng ký tự đặc biệt hoặc định dạng Markdown.
        'Human': '{query}'
        PASSAGE: '{relevant_passage}'
        """).format(query=query, relevant_passage=relevant_passage)
    else:
        # Prompt thay thế khi không có thông tin trong cơ sở dữ liệu
        prompt = ("""Bạn là một trợ lý ảo hỗ trợ người dùng
                  trả lời các thông tin về  và nội dung của cuốn sách 
        
        'Human': '{query}'
        Answer: 
        """).format(query=query)
    
    return prompt

def generate_answer_from_prompt(prompt):
    gemini_api_key = os.getenv("GOOGLE_API_KEY")


    llm = ChatGoogleGenerativeAI(
        api_key=gemini_api_key,
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    if not gemini_api_key:
        raise ValueError("Gemini API Key not provided. Please provide GEMINI_API_KEY as an environment variable")
    ai_msg = llm.invoke(prompt)
    return ai_msg.content

def generate_answer(db, query):
    # retrieve top 3 relevant text chunks
    relevant_text = get_relevant_passage(query, db, n_results=3)
    # Kiểm tra nếu không có relevant_text hoặc relevant_text trống
    if not relevant_text:
        prompt = make_rag_prompt(query, relevant_passage=[])
    else:
        prompt = make_rag_prompt(query, relevant_passage=relevant_text)
        
    answer = generate_answer_from_prompt(prompt)
    return answer

# answer = generate_answer(db=db, query='To Kill a Mockingbird')
# print(answer)
