# langchain_client.py
import os
import openai
import dotenv
from django.conf import settings
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import OpenAI
from langchain_openai import ChatOpenAI

env_vars = dotenv.dotenv_values()
openai.api_key = env_vars["OPENAI_API_KEY"]

def load_and_process_documents(course_id=None):
    texts = []

    # Load specific course documents if a course_id is provided
    if course_id is not None:
        course_directory = os.path.join(settings.MEDIA_ROOT, 'documents', str(course_id))
        if os.path.exists(course_directory):
            course_loader = PyPDFDirectoryLoader(course_directory)
            course_documents = course_loader.load()
            print(f"Loaded {len(course_documents)} documents for course ID: {course_id}")
            for doc in course_documents:
                print(f"Document: {doc.metadata['source']}")
            texts.extend(course_documents)

    # Load general documents
    general_directory = os.path.join(settings.MEDIA_ROOT, 'documents', 'general')
    if os.path.exists(general_directory):
        general_loader = PyPDFDirectoryLoader(general_directory)
        general_documents = general_loader.load()
        texts.extend(general_documents)

    # Split the texts into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_texts = text_splitter.split_documents(texts)

    # Create embeddings for the text chunks
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(split_texts, embeddings)

    return db       

def generate_contextual_prompt(query, user=None, course_id=None):

    if course_id == 2:
        instructions = "You are a knowledgeable chatbot that helps COMP120 students answer questions based on course documents. COMP120 is about Programming Abstractions and Methodologies. You have information about the syllabus and Lab 05 which is about learning how to use a debugger in VS Code."
        user_info = f"The user is {user.username}" if user else "The user is anonymous."

        prompt = f"{instructions}\n{user_info}\nUser Query: {query}\nResponse:"
        return prompt
    elif course_id ==4: 
        instructions = "You are a knowledgeable chatbot that helps COMP375 students answer questions based on course documents. COMP375 is about computer networks and how they play a large role in today’s society. The final exam for section 1 is Friday, May 17, 11:00am - 1:00pm and for section 2 Friday, May 17, 2:00 - 4:00pm. Monday 10 - 11am Tuesday 3 - 4pm (Zoom Only) and Wednesday 10 - 11am  4 - 5pm. There will be three major exams in this course: two midterm exams and a final exam. The midterm exams are tentatively scheduled for Monday, March 4 and Monday, April 15, both during our regularly scheduled class meeting time. Course Meeting Times Section 01 Lectures MWF Time 11:15am - 12:10pm Labs M 2:30 - 3:50pm Section 02 Lectures MWF 1:25 - 2:20pm Lab W 2:30 - 3:50pm."
        user_info = f"The user is {user.username}" if user else "The user is anonymous."

        prompt = f"{instructions}\n{user_info}\nUser Query: {query}\nResponse:"
        return prompt
    

def answer_question(query, course_id=None, prompt=None):
    db = load_and_process_documents(course_id)
    retriever = db.as_retriever(search_type="mmr", search_kwargs={"k": 20})
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.5,
        max_tokens=1000
    )

    qa = RetrievalQA.from_chain_type(
        llm=llm, chain_type="stuff", retriever=retriever, return_source_documents=True
    )

    # Use provided prompt or fall back to the user query
    result = qa({"query": prompt or query})
    return result['result']
