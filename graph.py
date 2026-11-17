import sqlite3
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage

from llm import chat_llm
from rag import retrieve

class ChatState(MessagesState):
    mode : str
    sources : list[str]

# easy explaination and simple the code can be written like this also 
# both will work the same (i have learnined in this base that's all ) (what does the code about this mean ! )

# CODE
# class ChatState(TypedDict):
#     messages: Annotated[list[AnyMessage], add_messages]
#     mode: str
#     sources: list[str]


# this is for normal chat
def chat_node(state : ChatState):
    messages = state['messages']
    response = chat_llm(messages)

    return {
        'messages' : [AIMessage(content=response)],
        "sources": []
        }

# this is for rag based chat
def rag_node(state: ChatState):
    question = state["messages"][-1].content

    docs = retrieve(question)

    if not docs:
        return {
            "messages": [
                AIMessage(content="No documents found. Please upload a file first.")
            ],
            "sources": []
        }
    
    context = "\n\n".join(
        f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}"
        for doc in docs
    )
  
    system_message = (
        "Answer using only the provided context. "
        "If the answer is not available in the context, say 'I don't know'.\n\n"
        f"Context:\n{context}"
    )

    response = chat_llm(
        state["messages"],
        system_message=system_message
    )

    sources = list({
        doc.metadata.get("source", "Unknown")
        for doc in docs
    })

    return {
        "messages": [AIMessage(content=response)],
        "sources": sources
    }

conn = sqlite3.connect("database/chat_history.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)

def router(state: ChatState):
    if state['mode'] == 'rag':
        return "rag"

    return "chat"


graph_builder = StateGraph(ChatState)

graph_builder.add_node("chat_node",chat_node)
graph_builder.add_node('rag_node',rag_node)

graph_builder.add_conditional_edges(START,router,{"chat": "chat_node","rag": "rag_node"})
graph_builder.add_edge("rag_node", END)
graph_builder.add_edge("chat_node", END)

chatbot = graph_builder.compile(checkpointer=checkpointer)

