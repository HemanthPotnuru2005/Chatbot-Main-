from langchain_community.document_loaders import PyPDFLoader,TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-001")

FAISS_PATH = "faiss_index"
store = None

#understand this code what's it's purpos 
def get_store():

    global store
    if store is not None:
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
    if file_path.endswitch('.pdf'):
        loader = PyPDFLoader(file_path)

    else:
        loader = TextLoader(
            file_path,
            encoding = 'utf-8'
        )

    return loader.load()


