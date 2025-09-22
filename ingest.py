# ingest.py

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, UnstructuredImageLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# Load environment variables
load_dotenv()

# --- CONFIGURATION ---
DOCS_FOLDER = "documents"
DB_PATH = "chroma_db"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# --- 1. LOAD DOCUMENTS FROM FOLDER ---
print("Scanning for documents and images...")
all_documents = []
for filename in os.listdir(DOCS_FOLDER):
    filepath = os.path.join(DOCS_FOLDER, filename)
    
    try:
        if filename.lower().endswith(".pdf"):
            # Use PyPDFLoader for PDF files
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            print(f"Loaded {len(docs)} page(s) from PDF: {filename}")
            all_documents.extend(docs)
            
        elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
            # Use UnstructuredImageLoader for image files (performs OCR)
            loader = UnstructuredImageLoader(filepath, mode="single")
            docs = loader.load()
            print(f"Extracted text from image: {filename}")
            all_documents.extend(docs)
            
    except Exception as e:
        print(f"Failed to load {filename}. Error: {e}")

if not all_documents:
    print("No documents were loaded. Please check the 'documents' folder and file types.")
    exit()

print(f"\nTotal documents loaded: {len(all_documents)}")


# --- 2. SPLIT TEXT ---
print("Splitting documents into chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
splits = text_splitter.split_documents(all_documents)

print(f"Split documents into {len(splits)} chunks.")


# ingest.py

# ... (keep all the code from the top until this section) ...


# --- 3. STORE IN VECTOR DATABASE ---
print("Creating and saving vector database...")

# First, define the embedding model we'll use
embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# Now, create the vector store, passing the embedding model correctly
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=embedding_model, # Use the 'embedding' argument here
    persist_directory=DB_PATH
)

print(f"\n✅ Vector database created successfully at {DB_PATH}")