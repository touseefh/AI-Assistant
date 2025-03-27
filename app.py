import streamlit as st
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
import time

# 🎨 Streamlit Config
st.set_page_config(page_title="Ahdus Technology AI Assistant", layout="wide")

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* Chat History Panel */
        .chat-history {
            width: 250px;
            background-color: #1E1E1E;
            padding: 15px;
            border-radius: 10px;
            position: fixed;
            left: 10px;
            top: 70px;
            bottom: 10px;
            overflow-y: auto;
            color: white;
        }
        /* Answer Box */
        .answer-box {
            background-color: #232b2b;
            color: white;
            padding: 10px;
            border-radius: 8px;
            margin-top: 10px;
        }
        /* Question Box */
        .question-box {
            font-weight: bold;
            margin-top: 15px;
        }
        /* Buttons */
        .stButton>button {
            background-color: #007bff;
            color: white;
            border-radius: 8px;
        }
        /* Clear History Button */
        .clear-history {
            background-color: #dc3545 !important;
            color: white !important;
            border-radius: 8px;
            margin-top: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Heading
st.markdown("<h1 style='text-align: center;'>🤖 Ahdus Technology AI Assistant</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Ask anything about Ahdus Technology</h3>", unsafe_allow_html=True)

# 🌐 Website URLs for scraping
urls = [
    "https://ahdustechnology.com/",
    "https://ahdustechnology.com/about-us",
    "https://ahdustechnology.com/software-product-development",
    "https://ahdustechnology.com/computer-vision-ai",
    "https://ahdustechnology.com/case-studies",
    "https://ahdustechnology.com/data-annotation-labeling",
    "https://ahdustechnology.com/cross-platform-app-development",
    "https://ahdustechnology.com/innovation-product-development",
    "https://ahdustechnology.com/shopify-e-commerce-development",
    "https://ahdustechnology.com/devops-agile-excellence",
    "https://ahdustechnology.com/blog",
    "https://ahdustechnology.com/careers",
    "https://ahdustechnology.com/pricing-model",
    "https://ahdustechnology.com/contact-us"
]

@st.cache_data
def scrape_and_store():
    """Scrapes website using Selenium and stores data in FAISS."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    all_texts = []

    for url in urls:
        try:
            driver.get(url)
            time.sleep(3)  # Allow JavaScript to load
            text = driver.find_element(By.TAG_NAME, "body").text.strip()
            if text:
                all_texts.append(text)
                print(f"✅ Extracted text from {url}")
            else:
                print(f"⚠️ No text found at {url}")

        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")

    driver.quit()

    if not all_texts:
        return None

    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=200)
    text_chunks = [text_splitter.split_text(text) for text in all_texts]
    flattened_chunks = [chunk for sublist in text_chunks for chunk in sublist]

    if not flattened_chunks:
        return None

    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_texts(flattened_chunks, embeddings)
    print(f"✅ Indexed {len(flattened_chunks)} text chunks in FAISS")

    return vectorstore

# 📌 Load Data
vectorstore = scrape_and_store()

# 🔑 Google Gemini API
genai.configure(api_key="YOUR_API_KEY_HERE")

def generate_response(query):
    """Retrieves relevant data and generates a detailed response using Gemini AI."""
    if vectorstore is None:
        return "⚠️ Error: No indexed website data available."

    retrieved_docs = vectorstore.similarity_search(query, k=4)  # Fetch more context
    context = " ".join([doc.page_content for doc in retrieved_docs])

    if not context.strip():
        return "❌ No relevant information found."

    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(
        f"""You are an AI assistant providing **detailed and structured answers**.  
        Answer the following question in a **long, well-explained, and step-by-step** manner.
        
        **Question:** {query}  
        **Context (from website):** {context}  
        
        - Provide an **in-depth explanation**.
        - Use **bullet points, steps, and examples** where needed.
        - Include **technical details** if relevant.
        - Structure the answer **logically and clearly**.
        """,
        generation_config=genai.types.GenerationConfig(
            temperature=0.7,  # Adjusts creativity
            max_output_tokens=1024,  # Allows longer responses
            top_p=0.9,  # Controls randomness
        )
    )

    return response.text if response else "⚠️ Unable to generate an answer."


# 🎤 Chat UI
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "selected_question" not in st.session_state:
    st.session_state.selected_question = ""

query = st.text_input("💬 Type your question here:", value=st.session_state.selected_question)

# Buttons Layout
col1, col2 = st.columns([0.2, 0.2])

if col1.button("🔎 Get Answer"):
    if query:
        answer = generate_response(query)
        st.session_state.chat_history.insert(0, {"question": query, "answer": answer})
        st.session_state.selected_question = ""  # Reset after answering
        st.rerun()  # ✅ Refresh to show the new answer

if col2.button("🗑️ Clear History", key="clear", help="Clear chat history", use_container_width=True):
    st.session_state.chat_history = []
    st.session_state.selected_question = ""
    st.rerun()  # ✅ Refresh to show empty history

# 📌 Left Panel for Chat History
with st.sidebar:
    st.markdown("### 📜 Chat History")
    for i, chat in enumerate(st.session_state.chat_history):
        if st.button(f"🔹 {chat['question']}", key=f"hist_{i}"):
            st.session_state.selected_question = chat["question"]
            st.rerun()  # ✅ Refresh to update input field and fetch answer

# 📌 Display latest question and answer
if st.session_state.chat_history:
    latest_chat = st.session_state.chat_history[0]
    st.markdown(f"<div class='question-box'>❓ <b>Question:</b> {latest_chat['question']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='answer-box'>{latest_chat['answer']}</div>", unsafe_allow_html=True)
