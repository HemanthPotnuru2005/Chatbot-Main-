
import streamlit as st 
import os 
import uuid

from langchain_core.messages import HumanMessage

from graph import chatbot
from rag import ingest_file


st.set_page_config(
    page_title="Multipurpse Chatbot",
    layout="wide"
)

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())  # CHANGED: Added () to generate a unique session ID

if 'messages' not in st.session_state:
    st.session_state.messages = []


def ask(question, mode):

    # Create LangGraph configuration
    config = {
        "configurable": {
            "thread_id": st.session_state.session_id
        }
    }

    # Send user message to LangGraph
    response = chatbot.invoke(
        {
            "messages": [HumanMessage(content=question)],
            "mode": mode
        },
        config=config
    )

    answer = response['messages'][-1].content

    sources = response.get("sources", [])

    return answer, sources


def upload_file(uploaded_file):
    os.makedirs("Uploads", exist_ok=True)

    file_path = os.path.join("Uploads", uploaded_file.name)

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    chunks = ingest_file(file_path)

    return chunks


def clear_chat():
    st.session_state.session_id = str(uuid.uuid4())  # CHANGED: Added () to generate a new session ID
    st.session_state.messages = []


with st.sidebar:

    st.title("Multipurpose Chatbot")
    selected_mode = st.radio(
        'Selected Chat Mode',
        ['Normal Chat', 'RAG']
    )

    mode = "normal" if selected_mode == 'Normal Chat' else "rag"


uploaded_file = st.file_uploader(
    "upload your document",
    type=["pdf", "txt"]
)


if st.button("upload"):
    if uploaded_file is not None:
        with st.spinner("Loading..."):
            chunks = upload_file(uploaded_file)  # CHANGED: Renamed upload_file variable to uploaded_file to avoid confusion
        st.success(f"Successful upload! {chunks} chunks added")
    else:
        st.warning("Please select a document first")


if st.button("Clear Chat"):
    clear_chat()
    st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message["content"])

    if message.get("sources"):  # CHANGED: Corrected "Sources" to "sources"
        st.caption(
            "Sources: " + ", ".join(message["sources"])
        )


user_input = st.chat_input("Enter your message here")


if user_input:
    st.session_state.messages.append({
        'role': "user",
        'content': user_input
    })

    with st.chat_message('user'):
        st.write(user_input)

    with st.chat_message("assistant"):  # CHANGED: Corrected "assistent" to "assistant"
        with st.spinner("Answering..."):
            answer, sources = ask(user_input, mode)

        st.write(answer)

        if sources:
            st.caption("Sources: " + ", ".join(sources))

        st.session_state.messages.append({
            "role": 'assistant',
            'content': answer,
            'sources': sources
        })


# CHANGED: Removed the extra try-except block that called ask() a second time.
# This was the reason you were receiving two responses.


if mode == "rag" and not os.path.exists('faiss_index'):
    st.warning("Please upload a file")
