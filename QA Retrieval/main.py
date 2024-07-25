from flask import Flask, request, jsonify
from flask_cors import CORS

# Import the rest of your dependencies
import google.generativeai as genai
import os
from dotenv import load_dotenv
# ...

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Your existing code for setting up the model, retrievers, and the chain
# ...

import google.generativeai as genai
import os
from dotenv import load_dotenv
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

from langchain.memory import ConversationBufferWindowMemory
from langchain_community.embeddings import VoyageEmbeddings
from langchain_community.embeddings import HuggingFaceBgeEmbeddings


VOYAGE_API_KEY = os.environ["VOYAGE_API_KEY"]
embed = VoyageEmbeddings(voyage_api_key=VOYAGE_API_KEY, model="voyage-2")
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro-latest")

def get_corpus(directory):
    loader = DirectoryLoader(directory, glob = "./*.pdf", loader_cls= PyPDFLoader)
    docs = loader.load()
    return docs

def get_corpus_chunks(corpus):
  text_splitter = RecursiveCharacterTextSplitter(chunk_size=2048, chunk_overlap = 128)
  chunks = text_splitter.split_documents(corpus)
  return chunks

pdf = get_corpus("/Users/deltae/Gyan Srota/Gyan-Srota-backend/Documents")
chunks_faiss = get_corpus_chunks(pdf)


embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_db_faiss = FAISS.from_documents(chunks_faiss, embedding=embed)

model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
faiss_retriever = vector_db_faiss.as_retriever()

retriever_multi_query = MultiQueryRetriever.from_llm(
    retriever = faiss_retriever, llm=model
)

bm25_retriever = BM25Retriever.from_documents(chunks_faiss)
bm25_retriever.k = 5

prompt_template = """

You are an AI assistant named Gyan Srota for Manipal University Jaipur (MUJ), created to provide comprehensive information and assistance to prospective and current students. Your knowledge base covers all aspects of the university, including admission criteria, academic programs, campus life, facilities, student support services, and more. Your role is to engage in natural conversations and provide detailed, personalized responses to the user's queries. 

Each query should be treated independently, without relying on previous context from chat history. Ensure your responses include all relevant details the user may need. Also, ask the user to specify the question in detail if you can't understand.

Answer the user's question completely and accurately, without failing to provide the necessary information.

Context: \n{context}?\n
History: \n{history}\n
Question: \n{question}\n

Answer:
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["history", "context", "question"])


ensemble_retriever = EnsembleRetriever(retrievers=[bm25_retriever, retriever_multi_query], weights=[0.5, 0.5])
memory = ConversationBufferWindowMemory(k=1, return_messages=True, memory_key="history", input_key="question")
chain_of_thought = RetrievalQA.from_chain_type(
    model, retriever=ensemble_retriever, chain_type = "stuff", chain_type_kwargs=
    {"prompt": prompt, 
     "memory": memory}, return_source_documents = True
)

@app.route('/ask', methods=['POST'])
def ask():
    prompt = request.json.get('prompt')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    try:
        response = chain_of_thought(prompt)
        return jsonify({'answer': response['result']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

