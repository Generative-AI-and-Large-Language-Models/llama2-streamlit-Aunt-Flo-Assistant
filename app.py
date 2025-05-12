import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import CTransformers
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory


import datetime

vectorstore_database_path = '/Users/sabafirdausansaria/Downloads/Aunt_Flo_Assistant_Using_Conversational_RAG_LLAMA2/vectorstore/db'

#create the embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2", model_kwargs={'device':"cpu"})

#create the vectorstore database
vectorstore_db = FAISS.load_local(vectorstore_database_path, embeddings, allow_dangerous_deserialization = True)

#create the llm 
llm = CTransformers(model="/Users/sabafirdausansaria/Downloads/Aunt_Flo_Assistant_Using_Conversational_RAG_LLAMA2/Model/llama-2-7b-chat.ggmlv3.q4_0.bin",
                    model_type="llama",
                    config={'max_new_tokens':512, 'temperature':0.2})

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

chain = ConversationalRetrievalChain.from_llm(llm=llm, chain_type='stuff', 
                                              retriever=vectorstore_db.as_retriever(search_kwargs={"k":2}),
                                              memory = memory)


#Start the streamlit
st.set_page_config(page_title="Welcome to the Aunt Flo Assistant",page_icon="🤗",)
st.title("Welcome to Aunt Flo Assistant 👩‍⚕️") 
    
st.date_input("what is today's date", datetime.datetime.now())

def conversation_chat(query):
    result = chain({"question": query, "chat_history": st.session_state['history']})
    st.session_state['history'].append((query, result["answer"]))
    return result["answer"]

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state['history'] = []


    #Generated indicates the Chatbot response
    if 'generated' not in st.session_state:
        st.session_state['generated'] = ["Hello! Ask me anything about Periods🤗"]

    #Past denotes the Human User's Input
    if 'past' not in st.session_state:
        st.session_state['past'] = ["Heyya 👋"]

def display_chat_history():

    reply_container = st.container()
    container = st.container()

    with container:
        with st.form(key='my_form', clear_on_submit=True):
            user_input = st.text_input("Ask Something", placeholder="Ask about your Menstrual Cycle related questions", key='input')
            submit_button = st.form_submit_button(label='Send')
      

        if submit_button and user_input:
            output = conversation_chat(user_input)

            st.session_state['past'].append(user_input)
            st.session_state['generated'].append(output)

        

    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state["past"][i], is_user=True, key=str(i) + '_user', avatar_style="initials", seed="User")
                message(st.session_state["generated"][i], key=str(i), avatar_style="initials", seed="AI")

# Initialize session state
initialize_session_state()
# Display chat history
display_chat_history()