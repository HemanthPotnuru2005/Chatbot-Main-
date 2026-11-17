import sqlite3
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_core.messages import SystemMessage,AIMessage,HumanMessage
from llm import chat_llm

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

def chat_node(state : ChatState):
    messages = state['messages']
    response = chat_llm(messages)

    return {
        'messages' : [AIMessage(content=response)],
        "sources": []
        }

conn = sqlite3.connect("database/chat_history.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)


graph_builder = StateGraph(ChatState)

graph_builder.add_node(chat_node)

graph_builder.add_edge(START, "chat_node")
graph_builder.add_edge("chat_node", END)



chatbot = graph_builder.compile(checkpointer=checkpointer)

if __name__ == "__main__":

    # First message
    response1 = chatbot.invoke(
        {"messages": [HumanMessage(content="My name is Hemanth")]},
        config={"configurable": {"thread_id": "t1"}}
    )

    print(response1["messages"][-1].content)

    # Second message using the same thread
    response2 = chatbot.invoke(
        {"messages": [HumanMessage(content="What is my name?")]},
        config={"configurable": {"thread_id": "t1"}}
    )

    print(response2["messages"][-1].content)
