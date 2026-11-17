from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
import os

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-001")

FAISS_PATH = "faiss_index"
store = None

#understand this code what's it's purpos 
def get_store():

    global store
    if store is None:
        return store

    if os.path.exists(FAISS_PATH):
        store = FAISS.load_local(
            FAISS_PATH,
            embeddings,
            allow_dangerous_deserialization=True
        )
        return store

    return None

#understand this code what's it's purpos 
def load_file(file_path): 
    if file_path.endswith('.pdf'):
        loader = PyPDFLoader(file_path)
    else:
        loader = TextLoader(
            file_path,
            encoding = 'utf-8'
        )

    return loader.load()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=50
)

def ingest_file(file_path):
    global store
    documents = load_file(file_path)

    for doc in documents:
        doc.metadata['source'] = os.path.basename(file_path)
        chunks = text_splitter.split_documents(documents)

        if store is None:
            store = FAISS.from_documents(chunks, embeddings)
        else:
            store.add_documents(chunks)
        
        store.save_local(FAISS_PATH)
        return len(chunks)


def retrieve(question,k=4):
    vectore_store = get_store()

    if vectore_store is None:
        return []

    results = vectore_store.similarity_search(
        question,
        k=4
    )
    return results