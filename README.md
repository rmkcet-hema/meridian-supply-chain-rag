# 🌸 Meridian Supply Chain RAG

> AI-powered Supply Chain Document Intelligence using Retrieval-Augmented Generation (RAG)

## 📌 Overview

**Meridian Supply Chain RAG** is an AI-powered document question-answering system designed to retrieve relevant information from supply-chain and procurement documents and generate accurate, source-grounded answers.

The system uses **local semantic embeddings**, **ChromaDB** for vector storage, and **Groq LLM** for answer generation.

Users can ask natural-language questions through a simple and interactive **Streamlit web application**.

---

## ✨ Key Features

- 📄 PDF document processing
- ✂️ Intelligent text chunking
- 🧠 Local semantic embeddings using Sentence Transformers
- 🔎 Semantic similarity-based document retrieval
- 🗄️ ChromaDB vector database
- 🤖 Groq-powered LLM responses
- 📚 Source-aware answers with document and page references
- 🌸 Interactive Streamlit UI
- 🔐 API keys stored securely using environment variables
- ⚡ Fully local document embedding pipeline

---

## 🏗️ System Architecture

```text
                 ┌─────────────────────┐
                 │    PDF Documents    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Text Extraction    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      Chunking       │
                 └──────────┬──────────┘
                            │
                            ▼
              ┌────────────────────────────┐
              │ Sentence Transformers      │
              │   Local Embeddings         │
              └─────────────┬──────────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      ChromaDB       │
                 │   Vector Database   │
                 └──────────┬──────────┘
                            │
                            │
                     User Question
                            │
                            ▼
                 ┌─────────────────────┐
                 │ Semantic Retrieval  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │     Groq LLM        │
                 │  Answer Generation  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Answer + Sources  │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │    Streamlit UI     │
                 └─────────────────────┘
                 | Technology            | Purpose                         |
| --------------------- | ------------------------------- |
| Python                | Core programming language       |
| Streamlit             | Web application interface       |
| Sentence Transformers | Local text embeddings           |
| ChromaDB              | Vector database                 |
| Groq                  | LLM inference                   |
| PyPDF                 | PDF text extraction             |
| python-dotenv         | Environment variable management |

📂 Project Structure
meridian-supply-chain-rag/
│
├── app.py
├── ingest.py
├── rag.py
│
├── test_api.py
├── test_groq.py
│
├── data/
│   ├── Meridian_Procurement_Policy_Handbook_v4.2.pdf
│   └── Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf
│
├── requirements.txt
├── README.md
├── .gitignore
│
└── chroma_db/
⚙️ Installation
1. Clone the repository
git clone https://github.com/rmkcet-hema/meridian-supply-chain-rag.git
2. Open the project
cd meridian-supply-chain-rag
3. Create a virtual environment
python -m venv venv
4. Activate the virtual environment

Windows:

venv\Scripts\activate
5. Install dependencies
pip install -r requirements.txt
🔐 Environment Setup

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key_here

⚠️ Never upload .env or API keys to GitHub.

The .gitignore file is configured to prevent .env from being committed.

📥 Document Ingestion

Before running the RAG application, process the PDF documents and create the vector database.

Run:

python ingest.py

The ingestion pipeline:

PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Local Embedding Generation
 ↓
ChromaDB Storage

After successful ingestion, the ChromaDB collection will contain the processed document chunks.

🚀 Running the Application

Start the Streamlit application:

streamlit run app.py

The application will open in the browser.

Default local address:

http://localhost:8501
💬 Example Questions

Users can ask questions such as:

Which supplier had the highest Q1 spend?
What was the Q1 spend of Shenzhen Rui Electronics?
Which supplier had the worst on-time delivery?
What was the total procurement spend in Q1?

The system retrieves relevant document sections and generates an answer using the retrieved context.

📊 Example Result
Question
Which supplier had the highest Q1 spend?
Answer
Shenzhen Rui Electronics had the highest Q1 spend at ₹21.9 crore.
Source
Meridian_Supply_Chain_Review_Q1_FY2025-26.pdf
Page 1
🔎 Retrieval Pipeline

The RAG pipeline follows these steps:

1. Document Processing

PDF files are loaded and converted into text.

2. Chunking

Large documents are divided into smaller meaningful text chunks.

3. Embedding Generation

Each chunk is converted into a numerical vector using a local Sentence Transformer model.

4. Vector Storage

The embeddings and associated metadata are stored in ChromaDB.

5. Query Processing

The user's question is converted into an embedding.

6. Semantic Retrieval

ChromaDB retrieves the most relevant document chunks.

7. Answer Generation

The retrieved context is passed to the Groq LLM to generate a concise answer.

8. Source Display

The application displays the relevant document and page information along with the answer.

🎯 Project Objective

The objective of this project is to provide a simple and intelligent way to query supply-chain documents without manually searching through multiple PDF files.

The system demonstrates how Retrieval-Augmented Generation can be applied to supply-chain document intelligence.

🔒 Security

API credentials are managed through environment variables.


## Sample Questions & Answers

### Q1. Which supplier had the highest Q1 spend?
**Answer:** Shenzhen Rui Electronics had the highest Q1 spend at ₹21.9 crore.

### Q2. What was the total procurement spend in Q1 FY 2025-26?
**Answer:** The total procurement spend was ₹81.6 crore.

### Q3. Which supplier had the lowest on-time delivery?
**Answer:** Shenzhen Rui Electronics had the lowest on-time delivery at 79.5%.

### Q4. Which supplier had the best on-time delivery?
**Answer:** Sunrise Connectors had the best on-time delivery at 98.2%.

### Q5. What was the main structural supply-chain risk?
**Answer:** The main structural risk was the absence of a second source for microcontrollers.

### Q6. How many line-stoppage events occurred during the quarter?
**Answer:** Seven line-stoppage events occurred across the two plants.

### Q7. How much production downtime was caused by the line-stoppage events?
**Answer:** The line-stoppage events caused 41 hours of production downtime.

### Q8. Which supplier was responsible for four of the seven line-stoppage events?
**Answer:** Shenzhen Rui Electronics was responsible for four of the seven events due to delayed microcontroller shipments.

### Q9. What was the inventory value at the end of Q1?
**Answer:** Inventory stood at ₹68.4 crore as of 30 June 2025.

### Q10. What technology stack is used in this RAG application?
**Answer:** The application uses Sentence Transformers for embeddings, ChromaDB for vector storage, and Llama 3.3 70B through Groq for answer generation.

The following files are intentionally excluded from Git tracking:

.env
venv/
chroma_db/
__pycache__/
🌱 Future Enhancements
📑 Support for additional document formats
📊 Supply-chain analytics dashboard
📈 Interactive supplier performance charts
🔍 Advanced filtering by supplier and date
💬 Conversation history
📤 Document upload directly from the UI
🚀 Cloud deployment
📱 Responsive user interface
👩‍💻 Author

Hema Varshini S

Meridian Supply Chain RAG
AI + RAG + Supply Chain Document Intelligence

⭐ Project Highlights
✓ Retrieval-Augmented Generation
✓ Local Semantic Embeddings
✓ ChromaDB Vector Search
✓ Groq LLM Integration
✓ Streamlit Interface
✓ Source-Grounded Answers
✓ Secure API Key Management
📜 License

This project is developed for educational and project demonstration purposes.