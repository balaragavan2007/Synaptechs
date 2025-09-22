# app.py (Final Version with Multimodal Image Analysis)

import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# --- Import all existing LangChain components ---
from langchain_groq import ChatGroq
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.document_loaders import PyPDFLoader, UnstructuredImageLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.tools.tavily_search import TavilySearchResults

# --- CONFIGURATION & ENVIRONMENT ---
DB_PATH = "chroma_db"
TEMP_DOCS_PATH = "temp_docs"
load_dotenv()

# Configure the Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# --- HELPER FUNCTIONS ---
def process_and_store_documents(uploaded_files):
    # This function remains the same as before
    all_documents = []
    for uploaded_file in uploaded_files:
        temp_filepath = os.path.join(TEMP_DOCS_PATH, uploaded_file.name)
        with open(temp_filepath, "wb") as f: f.write(uploaded_file.getbuffer())
        try:
            loader = PyPDFLoader(temp_filepath) if uploaded_file.name.lower().endswith(".pdf") else UnstructuredImageLoader(temp_filepath, mode="single")
            all_documents.extend(loader.load())
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")
        finally:
            os.remove(temp_filepath)
    if not all_documents: return False
    splits = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200).split_documents(all_documents)
    Chroma.from_documents(documents=splits, embedding=SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2"), persist_directory=DB_PATH)
    return True

# NEW, corrected code
def get_gemini_vision_response(image, prompt):
    """Generates a response from the Gemini Vision model."""
    # Use the latest supported model name
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    response = model.generate_content([prompt, image])
    return response.text

# --- STREAMLIT APP ---
st.set_page_config(page_title="Synaptechs Learning Assistant", layout="wide")

# --- Page 1: Main Document Chat Assistant ---
def main_chat_page():
    st.title("🎓 Synaptechs: Your Personalized Learning Assistant")

    if not os.path.exists(TEMP_DOCS_PATH):
        os.makedirs(TEMP_DOCS_PATH)

    with st.sidebar:
        st.header("📚 Your Knowledge Base")
        uploaded_files = st.file_uploader("Upload your documents (PDF, PNG for OCR)", accept_multiple_files=True, type=['pdf', 'png', 'jpg', 'jpeg'])
        if st.button("Add to Knowledge Base"):
            if uploaded_files:
                with st.spinner("Processing documents..."):
                    process_and_store_documents(uploaded_files)
                    st.success("Documents added to knowledge base!")
                    st.rerun()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if os.path.exists(DB_PATH):
        llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.7) # Using the faster model
        embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        vectorstore = Chroma(persist_directory=DB_PATH, embedding_function=embedding_function)
        retriever = vectorstore.as_retriever(search_kwargs={'k': 3})
        search_tool = TavilySearchResults()
        
        rag_prompt = ChatPromptTemplate.from_template(
            "Answer based on context. If unanswerable, say 'unanswerable'. Context: {context}\nQuestion: {question}"
        )
        rag_chain = ({"context": retriever, "question": RunnablePassthrough()} | rag_prompt | llm | StrOutputParser())
        search_chain = (ChatPromptTemplate.from_template("Answer this: {question}") | llm | StrOutputParser())

        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if user_question := st.chat_input("Ask a question..."):
            st.session_state.messages.append({"role": "user", "content": user_question})
            with st.chat_message("user"):
                st.markdown(user_question)

            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    rag_response = rag_chain.invoke(user_question)
                    if "unanswerable" in rag_response.lower():
                        st.write("Couldn't find an answer in your documents. Searching the web...")
                        search_results = search_tool.invoke(user_question)
                        final_response = search_chain.invoke({"question": f"Based on these search results: {search_results}, answer the question: {user_question}"})
                    else:
                        final_response = rag_response
                    st.markdown(final_response)
            
            st.session_state.messages.append({"role": "assistant", "content": final_response})
    else:
        st.info("👋 Welcome! Please upload your study materials to get started.")

# --- Page 2: Image Analysis ---
def image_analysis_page():
    st.title("🖼️ Image Analysis with Gemini Vision")
    st.write("Upload an image and ask a question about its visual content.")
    
    uploaded_image = st.file_uploader("Upload an image", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_image is not None:
        from PIL import Image
        image = Image.open(uploaded_image)
        st.image(image, caption='Uploaded Image.', use_column_width=True)
        
        prompt = st.text_input("What do you want to know about this image?", "Describe this image in detail.")
        
        if st.button("Analyze Image"):
            with st.spinner("Analyzing..."):
                response = get_gemini_vision_response(image, prompt)
                st.write("### Analysis Result")
                st.write(response)

# --- Multi-page navigation ---
page_names_to_funcs = {
    "Learning Assistant": main_chat_page,
    "Image Analysis": image_analysis_page,
}
selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()