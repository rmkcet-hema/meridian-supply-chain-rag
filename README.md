# 🌸 Meridian Supply Chain RAG

An AI-powered Retrieval-Augmented Generation system for querying supply-chain and procurement documents.

## Features

- PDF document ingestion
- Intelligent document chunking
- Local semantic embeddings
- ChromaDB vector database
- Groq LLM integration
- Source-grounded answers
- Streamlit UI
- Document upload and indexing

## Tech Stack

- Python
- Streamlit
- Sentence Transformers
- ChromaDB
- Groq
- Llama 3.3
- PyPDF

## Architecture

PDF Documents
↓
Text Extraction
↓
Chunking
↓
Local Embeddings
↓
ChromaDB
↓
Semantic Retrieval
↓
Groq LLM
↓
AI Answer + Sources

## Run Locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py