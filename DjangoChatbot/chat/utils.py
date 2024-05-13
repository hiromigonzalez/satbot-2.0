#utils.py
import os
from langchain.llms import OpenAI
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

def qa(file_path, query, k=5):
    # Load document
    with open(file_path, 'rb') as file:
        loader = PyPDFLoader(file)
        documents = loader.load()
    
    # Split the documents into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    
    # Select which embeddings we want to use
    embeddings = OpenAIEmbeddings()
    
    # Create the vector store to use as the index
    db = Chroma.from_documents(texts, embeddings)
    
    # Expose this index in a retriever interface
    retriever = db.as_retriever(search_type="similarity", search_kwargs={"k": k})
    
    # Create a chain to answer questions
    llm = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type='map_reduce', retriever=retriever, return_source_documents=False)
    
    result = qa({"query": query})
    return result['result']

