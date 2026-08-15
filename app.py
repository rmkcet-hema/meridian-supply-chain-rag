import os
import hashlib
import html

import streamlit as st
import chromadb

from dotenv import load_dotenv
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from groq import Groq


# ============================================================
# CONFIG
# ============================================================

load_dotenv()

DATA_FOLDER = "data"
CHROMA_FOLDER = "chroma_db"

os.makedirs(DATA_FOLDER, exist_ok=True)

st.set_page_config(
    page_title="Meridian RAG",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PREMIUM LAVENDER + FLORAL UI
# ============================================================

st.markdown("""
<style>

/* ==========================================================
   MAIN BACKGROUND
   ========================================================== */

.stApp {

    background:

        radial-gradient(
            circle at 8% 8%,
            rgba(205, 180, 255, 0.70) 0px,
            rgba(205, 180, 255, 0.32) 180px,
            transparent 350px
        ),

        radial-gradient(
            circle at 92% 18%,
            rgba(245, 195, 225, 0.55) 0px,
            rgba(245, 195, 225, 0.20) 180px,
            transparent 350px
        ),

        radial-gradient(
            circle at 85% 90%,
            rgba(195, 180, 250, 0.42) 0px,
            transparent 320px
        ),

        linear-gradient(
            135deg,
            #F0E8FF 0%,
            #E6DAFF 48%,
            #F3E9FF 100%
        );

    color: #342C45;
}


/* ==========================================================
   FLORAL DECORATIONS
   ========================================================== */

.stApp::before {

    content: "🌸";

    position: fixed;

    top: 55px;
    right: 55px;

    font-size: 42px;

    opacity: 0.30;

    transform: rotate(-15deg);

    pointer-events: none;

    z-index: 0;
}


.stApp::after {

    content: "🌷";

    position: fixed;

    bottom: 35px;
    left: 355px;

    font-size: 38px;

    opacity: 0.23;

    transform: rotate(12deg);

    pointer-events: none;

    z-index: 0;
}


/* ==========================================================
   MAIN CONTAINER
   ========================================================== */

.block-container {

    max-width: 1420px;

    padding-top: 2rem;

    padding-bottom: 4rem;

    position: relative;

    z-index: 1;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {

    background:

        radial-gradient(
            circle at 20% 10%,
            rgba(255,255,255,0.75),
            transparent 180px
        ),

        linear-gradient(
            180deg,
            #E7DCFF 0%,
            #DED0FA 55%,
            #EDE3FF 100%
        );

    border-right: 1px solid #D2C3ED;
}


section[data-testid="stSidebar"] .block-container {

    padding-top: 2rem;
}


/* ==========================================================
   BRAND
   ========================================================== */

.brand-title {

    color: #4B3970;

    font-size: 27px;

    font-weight: 850;

    letter-spacing: -0.5px;
}


.brand-subtitle {

    color: #817293;

    font-size: 13px;

    margin-top: 4px;
}


/* ==========================================================
   HERO
   ========================================================== */

.hero-title {

    font-size: 43px;

    font-weight: 850;

    color: #35284F;

    letter-spacing: -1.4px;

    line-height: 1.1;
}


.hero-subtitle {

    color: #80738F;

    font-size: 15px;

    margin-top: 7px;
}


.hero-icon {

    width: 66px;

    height: 66px;

    border-radius: 21px;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 31px;

    background:

        linear-gradient(
            135deg,
            #C5A7FF,
            #8965D8
        );

    box-shadow:

        0 13px 30px
        rgba(118, 87, 200, 0.27);

    border: 1px solid
        rgba(255,255,255,0.75);
}


/* ==========================================================
   SECTION TITLES
   ========================================================== */

.section-title {

    font-size: 21px;

    font-weight: 800;

    color: #403258;

    margin-top: 8px;

    margin-bottom: 13px;
}


/* ==========================================================
   METRIC CARDS
   ========================================================== */

.metric-card {

    position: relative;

    background:
        rgba(255,255,255,0.86);

    border: 1px solid
        rgba(215,201,238,0.95);

    border-radius: 22px;

    padding: 21px;

    min-height: 125px;

    box-shadow:
        0 10px 30px
        rgba(88,64,130,0.09);

    backdrop-filter: blur(12px);

    overflow: hidden;

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}


.metric-card:hover {

    transform:
        translateY(-3px);

    box-shadow:
        0 16px 35px
        rgba(88,64,130,0.15);
}


.metric-card::after {

    content: "✿";

    position: absolute;

    right: 14px;
    top: 9px;

    font-size: 22px;

    color: #B79CE4;

    opacity: 0.55;
}


.metric-number {

    font-size: 29px;

    font-weight: 850;

    color: #7657C8;
}


.metric-label {

    color: #887B96;

    font-size: 13px;

    margin-top: 6px;

    font-weight: 600;
}


/* ==========================================================
   STATUS
   ========================================================== */

.status-ready {

    display: inline-block;

    padding: 8px 14px;

    border-radius: 30px;

    background: #E9FAF1;

    border: 1px solid #C9EEDB;

    color: #258456;

    font-size: 12px;

    font-weight: 800;

    box-shadow:
        0 5px 15px
        rgba(39,145,91,0.08);
}


/* ==========================================================
   QUESTION AREA
   ========================================================== */

.question-box {

    background:
        rgba(255,255,255,0.70);

    border: 1px solid #DCCEF0;

    border-radius: 24px;

    padding: 20px;

    box-shadow:
        0 10px 30px
        rgba(85,65,120,0.07);
}


/* ==========================================================
   TEXT INPUT
   ========================================================== */

.stTextInput input {

    background: #FFFFFF !important;

    border: 1px solid #D6C8EA !important;

    border-radius: 15px !important;

    color: #342C45 !important;

    min-height: 52px;

    font-size: 15px;

    box-shadow:
        0 5px 16px
        rgba(75,55,110,0.05);
}


.stTextInput input:focus {

    border-color:
        #9876E5 !important;

    box-shadow:
        0 0 0 3px
        rgba(152,118,229,0.15)
        !important;
}


/* ==========================================================
   BUTTON
   ========================================================== */

.stButton > button {

    min-height: 47px;

    border-radius: 14px;

    border: none;

    background:

        linear-gradient(
            135deg,
            #9C7AE9,
            #7657C8
        );

    color: white;

    font-weight: 800;

    box-shadow:
        0 9px 22px
        rgba(118,87,200,0.27);

    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}


.stButton > button:hover {

    transform:
        translateY(-2px);

    box-shadow:
        0 13px 27px
        rgba(118,87,200,0.34);
}


/* ==========================================================
   ANSWER CARD
   ========================================================== */

.answer-card {

    position: relative;

    background:

        linear-gradient(
            135deg,
            rgba(255,255,255,0.97),
            rgba(247,241,255,0.97)
        );

    border: 1px solid #DDD0F0;

    border-left: 5px solid #9572E3;

    border-radius: 21px;

    padding: 25px 27px;

    margin-top: 10px;

    margin-bottom: 22px;

    box-shadow:
        0 13px 32px
        rgba(84,62,123,0.10);

    overflow: hidden;
}


.answer-card::after {

    content: "🌸";

    position: absolute;

    right: 18px;
    bottom: 10px;

    font-size: 27px;

    opacity: 0.22;
}


.answer-label {

    color: #8060CF;

    font-size: 12px;

    font-weight: 850;

    text-transform: uppercase;

    letter-spacing: 1.3px;

    margin-bottom: 10px;
}


.answer-text {

    color: #332C41;

    font-size: 19px;

    line-height: 1.65;

    padding-right: 30px;
}


.confidence-high {

    display: inline-block;

    margin-top: 17px;

    padding: 7px 13px;

    border-radius: 25px;

    background: #EAF9F1;

    border: 1px solid #CDEDDD;

    color: #27865A;

    font-size: 11px;

    font-weight: 800;
}


/* ==========================================================
   SOURCE CARD
   ========================================================== */

.source-card {

    background:
        rgba(255,255,255,0.90);

    border: 1px solid #DED2EF;

    border-radius: 17px;

    padding: 17px 19px;

    margin-bottom: 10px;

    box-shadow:
        0 7px 22px
        rgba(85,65,120,0.065);

    transition:
        transform 0.2s ease;
}


.source-card:hover {

    transform:
        translateX(3px);
}


.source-name {

    color: #493B60;

    font-weight: 750;

    font-size: 14px;
}


.source-meta {

    color: #91869F;

    font-size: 12px;

    margin-top: 6px;
}


/* ==========================================================
   EXPANDER
   ========================================================== */

[data-testid="stExpander"] {

    background:
        rgba(255,255,255,0.72);

    border: 1px solid #DCCFEF;

    border-radius: 15px;
}


/* ==========================================================
   FILE UPLOADER
   ========================================================== */

[data-testid="stFileUploader"] {

    background:
        rgba(255,255,255,0.62);

    border: 1px dashed #BFA9DD;

    border-radius: 15px;

    padding: 8px;
}


/* ==========================================================
   SIDEBAR INFO
   ========================================================== */

.stack-box {

    background:

        linear-gradient(
            135deg,
            rgba(255,255,255,0.82),
            rgba(247,242,255,0.94)
        );

    border: 1px solid #D9CBEA;

    border-radius: 17px;

    padding: 16px;

    color: #7C718A;

    font-size: 12px;

    line-height: 1.9;

    box-shadow:
        0 7px 20px
        rgba(90,65,125,0.07);
}


/* ==========================================================
   EMPTY STATE
   ========================================================== */

.empty-state {

    position: relative;

    background:

        linear-gradient(
            135deg,
            rgba(255,255,255,0.90),
            rgba(246,239,255,0.96)
        );

    border: 1px solid #DDD1EF;

    border-radius: 25px;

    padding: 52px;

    text-align: center;

    box-shadow:
        0 14px 35px
        rgba(84,62,123,0.09);

    overflow: hidden;
}


.empty-state::before {

    content: "🌷";

    position: absolute;

    left: 25px;
    top: 20px;

    font-size: 35px;

    opacity: 0.23;
}


.empty-state::after {

    content: "🌸";

    position: absolute;

    right: 28px;
    bottom: 18px;

    font-size: 35px;

    opacity: 0.23;
}


/* ==========================================================
   DIVIDER
   ========================================================== */

hr {

    border-color: #D8CBEA;
}


/* ==========================================================
   FOOTER
   ========================================================== */

.footer {

    text-align: center;

    color: #9589A5;

    font-size: 12px;

    padding: 30px 10px 10px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD RESOURCES
# ============================================================

@st.cache_resource
def load_resources():

    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    chroma_client = chromadb.PersistentClient(
        path=CHROMA_FOLDER
    )

    collection = chroma_client.get_or_create_collection(
        name="supply_chain"
    )

    groq_api_key = st.secrets.get(
        "GROQ_API_KEY",
        os.getenv("GROQ_API_KEY")
    )
    groq_client = Groq(
        api_key=groq_api_key
    )

    return (
        embedding_model,
        collection,
        groq_client
    )


embedding_model, collection, groq_client = load_resources()


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# DOCUMENT COUNT
# ============================================================

def get_document_count():

    if collection.count() == 0:
        return 0

    data = collection.get(
        include=["metadatas"]
    )

    files = set()

    for metadata in data.get("metadatas", []):

        if metadata and "file" in metadata:

            files.add(
                metadata["file"]
            )

    return len(files)


# ============================================================
# CHUNKING
# ============================================================

def create_chunks(text):

    chunk_size = 1000

    overlap = 150

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:

            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# ============================================================
# INDEX DOCUMENTS
# ============================================================

def index_documents(uploaded_files):

    total_chunks = 0

    progress = st.progress(0)

    for file_index, uploaded_file in enumerate(
        uploaded_files
    ):

        file_path = os.path.join(
            DATA_FOLDER,
            uploaded_file.name
        )

        with open(file_path, "wb") as f:

            f.write(
                uploaded_file.getbuffer()
            )


        reader = PdfReader(file_path)

        all_chunks = []


        if "Policy" in uploaded_file.name:

            document_type = "policy"

        else:

            document_type = "review"


        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):

            text = page.extract_text()

            if not text:
                continue


            chunks = create_chunks(text)


            for chunk_number, chunk in enumerate(
                chunks
            ):

                all_chunks.append({

                    "text": chunk,

                    "file":
                        uploaded_file.name,

                    "page":
                        page_number,

                    "type":
                        document_type,

                    "chunk_number":
                        chunk_number

                })


        if all_chunks:

            texts = [

                item["text"]

                for item in all_chunks

            ]


            vectors = embedding_model.encode(

                texts,

                show_progress_bar=False

            )


            for i, chunk in enumerate(
                all_chunks
            ):

                raw_id = (

                    f"{chunk['file']}_"
                    f"{chunk['page']}_"
                    f"{chunk['chunk_number']}"

                )


                chunk_id = hashlib.md5(

                    raw_id.encode()

                ).hexdigest()


                collection.upsert(

                    ids=[chunk_id],

                    embeddings=[
                        vectors[i].tolist()
                    ],

                    documents=[
                        chunk["text"]
                    ],

                    metadatas=[{

                        "file":
                            chunk["file"],

                        "page":
                            chunk["page"],

                        "type":
                            chunk["type"]

                    }]

                )


            total_chunks += len(
                all_chunks
            )


        progress.progress(

            (file_index + 1) /
            len(uploaded_files)

        )


    return total_chunks


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.html("""
    <div style="
        display:flex;
        align-items:center;
        gap:12px;
    ">

        <div style="
            width:47px;
            height:47px;
            border-radius:15px;

            display:flex;
            align-items:center;
            justify-content:center;

            font-size:25px;

            background:
                linear-gradient(
                    135deg,
                    #C8ADFF,
                    #9272E3
                );

            box-shadow:
                0 8px 18px
                rgba(118,87,200,0.22);
        ">
            📦
        </div>

        <div>

            <div class="brand-title">
                MERIDIAN RAG
            </div>

            <div class="brand-subtitle">
                Supply Chain Intelligence
            </div>

        </div>

    </div>
    """)


    st.write("")

    st.divider()


    # KNOWLEDGE BASE

    st.html("""
    <div class="section-title">
        📚 Knowledge Base
    </div>
    """)


    chunk_count = collection.count()

    document_count = get_document_count()


    col1, col2 = st.columns(2)


    with col1:

        st.html(f"""
        <div class="metric-card">

            <div class="metric-number">
                {document_count}
            </div>

            <div class="metric-label">
                Documents
            </div>

        </div>
        """)


    with col2:

        st.html(f"""
        <div class="metric-card">

            <div class="metric-number">
                {chunk_count}
            </div>

            <div class="metric-label">
                Chunks
            </div>

        </div>
        """)


    st.write("")


    if chunk_count > 0:

        st.html("""
        <span class="status-ready">
            ● System Ready
        </span>
        """)

    else:

        st.warning(
            "No documents indexed yet."
        )


    st.divider()


    # UPLOAD

    st.html("""
    <div class="section-title">
        📤 Add Documents
    </div>
    """)


    uploaded_files = st.file_uploader(

        "Upload PDF files",

        type=["pdf"],

        accept_multiple_files=True,

        label_visibility="collapsed"

    )


    if st.button(
        "✨  Index Documents",
        use_container_width=True
    ):

        if not uploaded_files:

            st.warning(
                "Please upload a PDF first."
            )

        else:

            with st.spinner(
                "Reading and indexing documents..."
            ):

                new_chunks = index_documents(
                    uploaded_files
                )


            st.success(
                "Documents indexed successfully!"
            )


            st.info(
                f"{new_chunks} chunks added."
            )


            st.rerun()


    st.divider()


    # AI STACK

    st.html("""
    <div class="stack-box">

        <div style="
            color:#5C4780;
            font-weight:850;
            margin-bottom:5px;
        ">
            ✨ AI STACK
        </div>

        <b>Embeddings</b><br>
        all-MiniLM-L6-v2

        <br>

        <b>Vector Database</b><br>
        ChromaDB

        <br>

        <b>Language Model</b><br>
        Llama 3.3 70B

        <br>

        <b>Provider</b><br>
        Groq

    </div>
    """)


# ============================================================
# HERO
# ============================================================

st.html("""
<div style="
    display:flex;
    align-items:center;
    gap:18px;
    margin-bottom:25px;
">

    <div class="hero-icon">
        📦
    </div>

    <div>

        <div class="hero-title">
            Supply Chain Intelligence
        </div>

        <div class="hero-subtitle">
            Ask questions, explore documents,
            and uncover insights instantly.
        </div>

    </div>

</div>
""")


# ============================================================
# DASHBOARD CARDS
# ============================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.html("""
    <div class="metric-card">

        <div class="metric-number">
            📄
        </div>

        <div class="metric-label">
            Document Intelligence
        </div>

    </div>
    """)


with col2:

    st.html(f"""
    <div class="metric-card">

        <div class="metric-number">
            {collection.count()}
        </div>

        <div class="metric-label">
            Indexed Knowledge Chunks
        </div>

    </div>
    """)


with col3:

    st.html("""
    <div class="metric-card">

        <div class="metric-number">
            🟢
        </div>

        <div class="metric-label">
            RAG System Online
        </div>

    </div>
    """)


st.write("")

st.divider()


# ============================================================
# QUESTION
# ============================================================

st.html("""
<div class="section-title">
    💬 Ask your supply-chain question
</div>

<div style="
    color:#8C8199;
    font-size:13px;
    margin-bottom:10px;
">
    Search your Meridian documents using natural language.
</div>
""")


question = st.text_input(

    "Question",

    placeholder=
        "Try: Which supplier had the highest Q1 spend?",

    label_visibility="collapsed"

)


ask_button = st.button(

    "🔍  Ask Question",

    use_container_width=True

)


# ============================================================
# RAG PIPELINE
# ============================================================

if ask_button:

    if collection.count() == 0:

        st.error(
            "No documents found. "
            "Please upload and index a PDF first."
        )


    elif not question.strip():

        st.warning(
            "Please enter a question."
        )


    else:

        with st.spinner(
            "🌸 Searching your supply-chain knowledge base..."
        ):

            # QUERY EMBEDDING

            query_vector = (

                embedding_model
                .encode(question)
                .tolist()

            )


            # VECTOR SEARCH

            results = collection.query(

                query_embeddings=[
                    query_vector
                ],

                n_results=5

            )


            documents = results[
                "documents"
            ][0]


            metadatas = results[
                "metadatas"
            ][0]


            # CONTEXT

            context = ""


            for i in range(
                len(documents)
            ):

                context += f"""

SOURCE {i + 1}

File:
{metadatas[i]["file"]}

Page:
{metadatas[i]["page"]}

Document Type:
{metadatas[i]["type"]}

Content:
{documents[i]}

"""


            # PROMPT

            prompt = f"""

You are an internal supply-chain
document assistant.

Answer the user's question ONLY
using the supplied document context.

Do not use outside knowledge.

If the answer is not present in
the context, say:

"I could not find this information
in the provided documents."

Be concise, factual and clear.

USER QUESTION:

{question}

DOCUMENT CONTEXT:

{context}

"""


            # GROQ

            response = (

                groq_client
                .chat
                .completions
                .create(

                    model=
                    "llama-3.3-70b-versatile",

                    messages=[

                        {
                            "role": "system",

                            "content":
                            (
                                "Answer only using "
                                "the supplied "
                                "document context."
                            )
                        },

                        {
                            "role": "user",

                            "content": prompt
                        }

                    ],

                    temperature=0

                )

            )


            answer = (

                response
                .choices[0]
                .message
                .content

            )


        # SAVE HISTORY

        st.session_state.history.append({

            "question":
                question,

            "answer":
                answer,

            "sources":
                metadatas,

            "documents":
                documents

        })


# ============================================================
# DISPLAY ANSWER
# ============================================================

if st.session_state.history:

    st.divider()


    st.html("""
    <div class="section-title">
        💡 AI Insights
    </div>
    """)


    for item_number, item in enumerate(

        reversed(
            st.session_state.history
        ),

        start=1

    ):

        safe_question = html.escape(
            item["question"]
        )


        safe_answer = (

            html.escape(
                item["answer"]
            )

            .replace(
                "\n",
                "<br>"
            )

        )


        # QUESTION

        st.html(f"""

        <div style="
            color:#8A7E98;
            font-size:11px;
            font-weight:850;
            letter-spacing:1.2px;
            margin-bottom:7px;
        ">
            QUESTION {item_number}
        </div>

        <div style="
            color:#443755;
            font-size:16px;
            font-weight:750;
            margin-bottom:12px;
        ">
            {safe_question}
        </div>

        """)


        # ANSWER

        st.html(f"""

        <div class="answer-card">

            <div class="answer-label">
                ✨ AI Answer
            </div>

            <div class="answer-text">
                {safe_answer}
            </div>

            <div class="confidence-high">
                ✓ Grounded in your documents
            </div>

        </div>

        """)


        # SOURCES

        st.html("""
        <div class="section-title">
            📚 Sources
        </div>
        """)


        grouped_sources = {}


        for metadata in item["sources"]:

            filename = metadata["file"]

            page = metadata["page"]


            if filename not in grouped_sources:

                grouped_sources[
                    filename
                ] = set()


            grouped_sources[
                filename
            ].add(page)


        for filename, pages in (
            grouped_sources.items()
        ):

            safe_filename = html.escape(
                str(filename)
            )


            page_list = ", ".join(

                str(page)

                for page in sorted(pages)

            )


            st.html(f"""

            <div class="source-card">

                <div style="
                    display:flex;
                    align-items:center;
                    gap:10px;
                ">

                    <div style="
                        width:37px;
                        height:37px;
                        border-radius:11px;
                        background:#F0E8FF;
                        display:flex;
                        align-items:center;
                        justify-content:center;
                        font-size:18px;
                    ">
                        📄
                    </div>

                    <div>

                        <div class="source-name">
                            {safe_filename}
                        </div>

                        <div class="source-meta">
                            Page(s): {page_list}
                        </div>

                    </div>

                </div>

            </div>

            """)


        # DETAILS

        with st.expander(
            "🔎  View retrieval details"
        ):

            col1, col2 = st.columns(2)


            with col1:

                st.write(
                    f"**Retrieved chunks:** "
                    f"{len(item['documents'])}"
                )

                st.write(
                    "**Vector DB:** ChromaDB"
                )


            with col2:

                st.write(
                    "**Embedding:** "
                    "all-MiniLM-L6-v2"
                )

                st.write(
                    "**LLM:** "
                    "Llama 3.3 70B via Groq"
                )


        st.divider()


# ============================================================
# EMPTY STATE
# ============================================================

if not st.session_state.history:

    st.html("""
    <div class="empty-state">

        <div style="
            font-size:47px;
            margin-bottom:13px;
        ">
            🌸
        </div>

        <div style="
            font-size:23px;
            font-weight:850;
            color:#443655;
        ">
            Your supply-chain assistant is ready
        </div>

        <div style="
            color:#8B8098;
            font-size:14px;
            margin-top:9px;
        ">
            Ask anything about your Meridian
            procurement and supply-chain documents.
        </div>

        <div style="
            margin-top:18px;
            color:#9A8DA8;
            font-size:12px;
        ">
            ✿ Search &nbsp; • &nbsp;
            ✨ Retrieve &nbsp; • &nbsp;
            💡 Understand
        </div>

    </div>
    """)


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div class="footer">

    🌸 Meridian Supply Chain RAG

    &nbsp; • &nbsp;

    Document-Grounded AI Intelligence

    &nbsp; • &nbsp;

    ✿

</div>
""")