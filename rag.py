import os
import chromadb
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()

# -----------------------------
# Load embedding model
# -----------------------------
print("Loading embedding model...")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Connect to ChromaDB
# -----------------------------
client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="supply_chain"
)

# -----------------------------
# Connect to Groq
# -----------------------------
groq_client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# -----------------------------
# Ask question
# -----------------------------
question = input("\nAsk a question: ")

# Create question embedding
query_vector = embedding_model.encode(
    question
).tolist()

# Retrieve relevant chunks
results = collection.query(
    query_embeddings=[query_vector],
    n_results=3
)

documents = results["documents"][0]
metadatas = results["metadatas"][0]

# -----------------------------
# Build context
# -----------------------------
context = ""

for i in range(len(documents)):
    context += f"""
SOURCE {i + 1}
File: {metadatas[i]["file"]}
Page: {metadatas[i]["page"]}
Type: {metadatas[i]["type"]}

Content:
{documents[i]}

"""

# -----------------------------
# Send context to Groq
# -----------------------------
prompt = f"""
You are a supply-chain document assistant.

Answer the user's question ONLY using the provided context.

If the answer is not available in the context, say:
"I could not find this information in the provided documents."

Be concise and factual.

User Question:
{question}

Context:
{context}
"""

response = groq_client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "You answer questions using only the supplied document context."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0
)

answer = response.choices[0].message.content

# -----------------------------
# Display answer
# -----------------------------
print("\n==============================")
print("ANSWER")
print("==============================")
print(answer)

print("\n==============================")
print("SOURCES")
print("==============================")

for i in range(len(documents)):
    print(
        f"{i + 1}. "
        f"{metadatas[i]['file']} "
        f"(Page {metadatas[i]['page']})"
    )