import google.generativeai as genai
from chromadb import Documents, EmbeddingFunction, Embeddings
import os
import chromadb
from typing import List
from dotenv import load_dotenv
from Loadfile import loadfilecsv,convertDocument
class GeminiEmbeddingFunction(EmbeddingFunction):
    """
    Custom embedding function using the Gemini AI API for document retrieval.

    This class extends the EmbeddingFunction class and implements the __call__ method
    to generate embeddings for a given set of documents using the Gemini AI API.

    Parameters:
    - input (Documents): A collection of documents to be embedded.

    Returns:
    - Embeddings: Embeddings generated for the input documents.
    """
    def __call__(self, input: Documents) -> Embeddings:
        # Load environment variables
        load_dotenv()
        gemini_api_key = os.getenv("GOOGLE_API_KEY")
        
        # Debug: print API key (remove this in production)
        
        if not gemini_api_key:
            raise ValueError("Gemini API Key not provided. Please provide GEMINI_API_KEY as an environment variable")
        
        # Configure the generative AI API
        genai.configure(api_key=gemini_api_key)
        model = "models/embedding-001"
        title = "Custom query"
        
        # Generate embeddings
        response = genai.embed_content(model=model,
                                       content=input,
                                       task_type="retrieval_document",
                                       title=title)
        
        # Return the embeddings
        return response["embedding"]
def create_chroma_db(documents:List, path:str, name:str):
    """
    Creates a Chroma database using the provided documents, path, and collection name.

    Parameters:
    - documents: An iterable of documents to be added to the Chroma database.
    - path (str): The path where the Chroma database will be stored.
    - name (str): The name of the collection within the Chroma database.

    Returns:
    - Tuple[chromadb.Collection, str]: A tuple containing the created Chroma Collection and its name.
    """
    chroma_client = chromadb.PersistentClient(path=path)

    db = chroma_client.create_collection(name=name, embedding_function=GeminiEmbeddingFunction())

    for i, d in enumerate(documents):
        db.add(documents=d, ids=str(i))

    return db, name
def load_chroma_collection(path, name):
    """        print(i)
        print(d)
    Loads an existing Chroma collection from the specified path with the given name.

    Parameters:
    - path (str): The path where the Chroma database is stored.
    - name (str): The name of the collection within the Chroma database.

    Returns:
    - chromadb.Collection: The loaded Chroma Collection.
    """
    chroma_client = chromadb.PersistentClient(path=path)
    db = chroma_client.get_collection(name=name, embedding_function=GeminiEmbeddingFunction())

    return db
def get_relevant_passage(query, db, n_results):
  passage = db.query(query_texts=[query], n_results=n_results)['documents'][0]
  return passage # return list document  neighbor
# ds = loadfilecsv('RAG/Real_Books_FAQ_200.csv')
# data =convertDocument(ds)
# create_chroma_db(data,'Database','book')
db =load_chroma_collection('Database','book')
# passage = get_relevant_passage('To Kill a Mockingbird',db=db,n_results=3)
# print(passage[0])
