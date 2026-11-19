# Multipurpose AI Chatbot

## Overview

The **Multipurpose AI Chatbot** is an AI-powered chatbot application that supports two different conversation modes:

1. **Normal Chat:** Interact with an AI assistant and ask general questions.
2. **RAG (Retrieval-Augmented Generation):** Upload PDF or TXT documents and ask questions based on their content.

The project uses LangChain for LLM integration, LangGraph for workflow management, and Streamlit for the user interface.

For document-based question answering, it uses Google Gemini embeddings and FAISS vector storage to retrieve relevant information from uploaded documents.

## Features

- **Normal Chat:** Have general conversations with an AI assistant.
- **Document Upload:** Upload PDF and TXT files.
- **RAG-Based Question Answering:** Ask questions using information from uploaded documents.
- **Semantic Search:** Retrieve relevant document chunks using FAISS.
- **Source Tracking:** Identify the source documents used to generate answers.
- **Conversation Memory:** Store conversation checkpoints using SQLite.
- **Chat Management:** Clear the current conversation and start a new session.
- **Interactive Interface:** Use a Streamlit-based chatbot interface.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| LangChain | LLM integration and document processing |
| LangGraph | Chatbot workflow and state management |
| Groq | LLM inference |
| OpenAI GPT-OSS 20B | Language model used through Groq |
| Streamlit | User interface |
| FAISS | Vector database and similarity search |
| Google Gemini Embeddings | Text embedding generation |
| SQLite | Conversation checkpoint storage |
| PyPDFLoader | PDF document loading |
| TextLoader | Text file loading |
| RecursiveCharacterTextSplitter | Document chunking |
| python-dotenv | Environment variable management |

## Project Architecture

The application follows a modular architecture:

1. **Streamlit Interface:** Handles user interactions, chat messages, document uploads, and chat mode selection.
2. **LangGraph Workflow:** Routes user queries to the appropriate processing node.
3. **Normal Chat Node:** Sends user messages to the language model.
4. **RAG Node:** Retrieves relevant document chunks and generates context-based answers.
5. **FAISS Vector Store:** Stores document embeddings and performs similarity searches.
6. **SQLite Checkpointer:** Saves conversation state using thread-based identifiers.

## How It Works

### Normal Chat Workflow

1. The user selects Normal Chat mode.
2. The user enters a question.
3. LangGraph routes the request to the chat node.
4. The chat node sends the conversation to the Groq-hosted language model.
5. The AI-generated response is displayed in Streamlit.

### RAG Workflow

1. The user uploads a PDF or TXT document.
2. The document loader extracts its content.
3. The text splitter divides the content into smaller chunks.
4. Google Gemini generates embeddings for the chunks.
5. FAISS stores the embeddings for similarity search.
6. The user asks a question about the uploaded document.
7. The retriever finds relevant document chunks.
8. LangGraph sends the retrieved context to the language model.
9. The model generates an answer using the provided context.
10. The application displays the answer and its source documents.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/HemanthPotnuru2005/multipurpose-ai-chatbot.git
```

```bash
cd multipurpose-ai-chatbot
```

### 2. Create a Virtual Environment

```bash
python -m venv myenv
```

Activate the environment:

**Windows:**

```bash
myenv\Scripts\activate
```

**Linux / macOS:**

```bash
source myenv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root directory.

Add your API keys:

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

Never upload your actual API keys to GitHub.

### 5. Run the Application

```bash
streamlit run app.py
```

The Streamlit application will open in your browser.

## Usage

1. Launch the application.
2. Select Normal Chat or RAG from the sidebar.
3. For document-based questions, upload a PDF or TXT file.
4. Click the upload button to process the document.
5. Enter your question in the chat input.
6. View the AI-generated response and available source information.
7. Use Clear Chat to start a new conversation.

## Future Improvements

- Support additional document formats.
- Improve conversation history management.
- Add support for multiple document collections.
- Display retrieved document chunks alongside answers.
- Improve the user interface and user experience.
- Add streaming responses.
- Deploy the application to a cloud platform.

## Author

**Hemanth Potnuru**

- GitHub: [HemanthPotnuru2005](https://github.com/HemanthPotnuru2005)

---

If you find this project useful, consider giving the repository a star.
