# langchain_client.py
import os
import openai
import dotenv
from django.conf import settings
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import OpenAI
from .models import Document

env_vars = dotenv.dotenv_values()
openai.api_key = env_vars["OPENAI_API_KEY"]

def load_and_process_documents():
    directory_path = os.path.join(settings.MEDIA_ROOT, 'documents')
    loader = PyPDFDirectoryLoader(directory_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(texts, embeddings)
    return db


def answer_question(query):
    db = load_and_process_documents()
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": 2})
    api_key = ""
    llm = OpenAI()
    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="map_reduce", retriever=retriever, return_source_documents=True)
    result = qa({"query": query})
    return result['result']
