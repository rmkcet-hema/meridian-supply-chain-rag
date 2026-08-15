import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

load_dotenv()

DATA_FOLDER = "data"
CHROMA_FOLDER = "chroma_db"

# Local embedding model
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)

all_chunks = []

# Read PDFs and create chunks
for filename in os.listdir(DATA_FOLDER):

    if filename.endswith(".pdf"):

        path = os.path.join(DATA_FOLDER, filename)
        reader = PdfReader(path)

        print(f"\nProcessing: {filename}")
        print(f"Pages: {len(reader.pages)}")

        if "Policy" in filename:
            document_type = "policy"
        else:
            document_type = "review"

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if text:
                chunks = text_splitter.split_text(text)

                for chunk in chunks:
                    all_chunks.append({
                        "text": chunk,
                        "file": filename,
                        "page": page_number,
                        "type": document_type
                    })

print("\n==============================")
print("CHUNKING COMPLETED")
print("==============================")
print(f"Total chunks: {len(all_chunks)}")


# Create ChromaDB
print("\nCreating ChromaDB...")

chroma_client = chromadb.PersistentClient(
    path=CHROMA_FOLDER
)

collection = chroma_client.get_or_create_collection(
    name="supply_chain"
)


# Create embeddings locally
print("\nCreating local embeddings...")

texts = [chunk["text"] for chunk in all_chunks]

vectors = embedding_model.encode(
    texts,
    show_progress_bar=True
)

# Store everything in ChromaDB
print("\nStoring chunks in ChromaDB...")

for i, chunk in enumerate(all_chunks):

    collection.upsert(
        ids=[f"chunk_{i}"],
        embeddings=[vectors[i].tolist()],
        documents=[chunk["text"]],
        metadatas=[{
            "file": chunk["file"],
            "page": chunk["page"],
            "type": chunk["type"]
        }]
    )

print("\n==============================")
print("CHROMADB COMPLETED")
print("==============================")
print(f"Collection: supply_chain")
print(f"Chunks stored: {collection.count()}")
print(f"Database folder: {CHROMA_FOLDER}")