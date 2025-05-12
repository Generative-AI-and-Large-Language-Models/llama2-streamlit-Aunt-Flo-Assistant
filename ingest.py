#Import the Libraries

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter 

Data_path = '/Users/sabafirdausansaria/Downloads/Aunt_Flo_Assistant_Using_Conversational_RAG_LLAMA2/Data'
vectorstore_database_path = 'vectorstore/db'

# Create vector database
def create_vector_db():
    #Load the Data in the PDF Format
    loader = DirectoryLoader(Data_path,
                             glob='*.pdf',
                             loader_cls=PyPDFLoader)

    documents = loader.load()

    #Split the Data
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    #Create the Embeddings
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})

    #Create the Vectorstore Database using FAISS
    db = FAISS.from_documents(texts, embeddings)

    #Saving the Vectorstore Database locally 
    db.save_local(vectorstore_database_path)
    
    print("Vector database created successfully.")

if __name__ == "__main__":
    create_vector_db()
