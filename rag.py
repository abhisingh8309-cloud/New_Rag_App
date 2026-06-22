from uuid import uuid4
 
from dotenv import load_dotenv
from pathlib import Path
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_community.document_loaders import AsyncHtmlLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from huggingface_hub import login
import os
 
load_dotenv()
 
CHUNK_SIZE=1000
EMBEDDING_MODEL="Alibaba-NLP/gte-base-en-v1.5"
VECTOR_STORE_DIR=Path(__file__).parent/"resources/vector_store"
COLLECTION_NAME="real_estate"
hf_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
 
# Ensure token is set 
if not hf_token:
    raise ValueError("Hugging Face API token not found. Set HUGGINGFACEHUB_API_TOKEN in .env or system enviroment. ")
 
# Authenticate before using the model 
login(token=hf_token)
 
llm=None
Vector_Store=None
 
def initialize_components():
    """ 
    This function initializes the components required
    Initializing llm, embedding model, vector_db
    """
 
    global llm,Vector_Store
 
    if llm is None:
        llm=ChatGroq(model="llama-3.3-70b-versatile",temperature=0.9, max_tokens=500)
 
    if Vector_Store is None:
        ef=HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"trust_remote_code":True}
        )
 
        Vector_Store=Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=ef,
            persist_directory=str(VECTOR_STORE_DIR)
        )
 
def process_urls(urls):
    """ 
    This function scrap data from the urls and stores it in a vector db
    :param urls: input urls
    :return
    """ 
 
    yield "Initializing components....✅" 
    initialize_components()
 
    yield "Reseting vector store.....✅"
    Vector_Store.reset_collection()
 
    # Load HTML content
    loader = AsyncHtmlLoader(urls)
    html_docs = loader.load()
 
    if not html_docs:
        raise ValueError("No content could be loaded from the provided URLs.")
 
    # Transform HTML to text including tables
    bs_transformer = BeautifulSoupTransformer()
    data = bs_transformer.transform_documents(
        html_docs,
        tags_to_extract=["p", "li", "div", "table", "tr", "td", "th", "span", "h1", "h2", "h3"]
    )
 
    if not data:
        raise ValueError("No content could be extracted from the provided URLs.")
 
    yield "Splitting text into chunks....✅"
    text_splitter=RecursiveCharacterTextSplitter(
        separators=["\n\n","\n","."," "],
        chunk_size=CHUNK_SIZE
    )       
 
    docs=text_splitter.split_documents(data)
 
    if not docs:
        raise ValueError("No chunks were created. URLs may have no readable text.")
 
    yield "Adding chunks to vector database...✅"
    uuids=[str(uuid4()) for _ in range(len(docs))]
    Vector_Store.add_documents(docs,ids=uuids)
 
    yield "Done adding docs to the vector database.....✅"
 
def generate_answer(query):
    if not Vector_Store:
        raise RuntimeError("Vector Database is not initialized")
    
    chain=RetrievalQAWithSourcesChain.from_llm(llm=llm,retriever=Vector_Store.as_retriever())
 
    result=chain.invoke({"question":query}, return_only_outputs=True)
 
    sources=result.get("sources","")
 
    return result['answer'],sources