
from langchain_core.messages import systemessage
from langchain_core.messages import SystemMessage,HumanMessage
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os

load_dotenv()

llm = ChatGroq(model = "openai/gpt-oss-20b",temperateure = 0.3)

def chat_llm(messages, system_message = "You are a helpful assistant"):

    system_message = SystemMessage(system_message)
    all_message = [system_message] + messages
    response = llm.invoke(all_message)

    return response.content