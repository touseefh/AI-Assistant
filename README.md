# Ahdus Technology AI Assistant

## Overview
Ahdus Technology AI Assistant is a **Streamlit-based chatbot** that provides structured and informative answers about Ahdus Technology. It scrapes real-time data from the company's website using **Selenium**, stores the extracted information in a **FAISS vector database**, and leverages **Google Gemini AI** for generating detailed responses. The chatbot also features an interactive UI with chat history, a stylish design, and real-time response generation.

## Features
- **Real-time Web Scraping**: Uses Selenium to extract website content dynamically.
- **Vector Search (FAISS)**: Stores and retrieves relevant information efficiently.
- **Google Gemini AI Integration**: Generates structured and detailed responses.
- **Interactive Chat UI**:
  - Displays chat history in a sidebar.
  - Shows the latest question on top.
  - Provides answers in a structured, easy-to-read format.
  - Includes buttons to get an answer or clear history.
- **Custom Styling**: Enhanced user experience with CSS-based design.
- **Caching for Performance**: Scraped data is cached for efficiency.

---

## Installation Guide
### 1️⃣ Prerequisites
Ensure you have the following installed:
- **Python 3.8+**
- **Google Chrome & ChromeDriver**

### 2️⃣ Clone the Repository
```bash
git clone https://github.com/touseefh/AI-Assistant.git
cd AI-Assistant
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Google Gemini API Key
### Configure API Key for Google Gemini AI
You need a **Google Gemini API key** for AI feedback generation. Replace the placeholder API key in the code with your actual key.
```python
import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY_HERE")
```


### 5️⃣ Run the Application
Start the Streamlit app with:
```bash
streamlit run app.py
```

---

## How It Works
### 🔍 Web Scraping
- The app uses **Selenium** to scrape text data from multiple pages of Ahdus Technology's website.
- Extracted data is **split into chunks** using LangChain's **CharacterTextSplitter**.
- The processed text is **stored in FAISS** for similarity-based retrieval.

### 📡 Query Processing & Response Generation
- When a user submits a query, **FAISS searches** for the most relevant text chunks.
- The **retrieved text is sent to Google Gemini AI**, which generates a structured answer.
- The AI's response is displayed in the chat UI.

### 💬 Chat UI & Interaction
- Users can **ask questions** through a text input field.
- The assistant **retrieves answers in real time**.
- The **chat history is stored in session state**, allowing users to revisit previous queries.
- A **clear history button** resets the conversation.


---

## Troubleshooting
### ❌ Common Issues & Fixes
1. **Chromedriver Errors:** Ensure the correct version of ChromeDriver is installed:
   ```bash
   pip install chromedriver-autoinstaller
   ```
2. **Google Gemini API Key Issues:**
   - Verify the API key is correctly set in `.env` or the script.
   - Check your **Google Cloud Console** for quota limits.
3. **FAISS Module Not Found:**
   ```bash
   pip install faiss-cpu
   ```

---

## Future Enhancements
🔹 Improve UI with real-time updates and animations.  
🔹 Support multi-language queries and responses.  
🔹 Add voice input & output functionality.  
🔹 Enhance search accuracy with additional NLP techniques.  

---

## Author
Developed by **HireSync.ai** 🚀

