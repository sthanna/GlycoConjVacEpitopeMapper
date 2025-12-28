# --------------------------------------------------------------------------------
# Author: Sandeep Thanna
# Copyright: 2025, Sandeep Thanna
# Maintainer: Sandeep Thanna
# --------------------------------------------------------------------------------
from pathlib import Path
from typing import List, Tuple
# Imports assume standard LangChain and community packages are installed
try:
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_huggingface import HuggingFaceEmbeddings
    HAS_RAG_DEPS = True
except ImportError:
    HAS_RAG_DEPS = False
    print("Warning: LangChain or related packages not found. RAG functionality will be disabled.")

def build_agent_knowledge_base(data_dir: str, index_output_path: str) -> Tuple[object, List]:
    if not HAS_RAG_DEPS:
        print("Skipping Vector Store build: Missing dependencies.")
        return None, []
    """
    Build a vector store from documents in a directory.
    
    Args:
        data_dir (str): Path to directory containing PDFs or text files.
        index_output_path (str): Path to save the FAISS index.
        
    Returns:
        Tuple[VectorStore, List[Document]]: The vector store object and list of documents.
    """
    input_path = Path(data_dir)
    docs = []
    
    # Initialize splitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=1500, chunk_overlap=200)
    
    # Load PDFs
    for file_path in input_path.glob("*.pdf"):
        try:
            loader = PyPDFLoader(str(file_path))
            pages = loader.load()
            for page in pages:
                chunks = splitter.split_text(page.page_content)
                # Convert string chunks back to minimal document objects if needed, 
                # or use splitter.split_documents(pages) directly.
                docs.extend(splitter.create_documents(chunks, metadatas=[page.metadata]*len(chunks)))
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

    # Load Text files
    for file_path in input_path.glob("*.txt"):
        try:
            loader = TextLoader(str(file_path), encoding='utf-8')
            documents = loader.load()
            split_docs = splitter.split_documents(documents)
            docs.extend(split_docs)
        except Exception as e:
            print(f"Error loading {file_path} with utf-8: {e}")
            try:
                loader = TextLoader(str(file_path), encoding='latin-1')
                documents = loader.load()
                split_docs = splitter.split_documents(documents)
                docs.extend(split_docs)
            except Exception as e2:
                print(f"Fatal error loading {file_path}: {e2}")

    if not docs:
        print("No documents found or loaded.")
        return None, []

    print(f"Encoded {len(docs)} document chunks.")

    # Initialize Embeddings
    # Using a standard lightweight model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Build Vector Store
    try:
        vectorstore = FAISS.from_documents(docs, embeddings)
        vectorstore.save_local(index_output_path)
        print(f"Index saved to {index_output_path}")
        return vectorstore, docs
    except Exception as e:
        print(f"Error building vector store: {e}")
        return None, docs

if __name__ == "__main__":
    # Example usage
    # build_agent_knowledge_base("./data/papers", "./data/indexes/agent_index")
    pass
