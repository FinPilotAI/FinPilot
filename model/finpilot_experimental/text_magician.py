############################# Import Modules #############################
import os
from config.secret_keys import OPENAI_API_KEY

# text magician
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

# messages
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph.message import add_messages




############################# Set Environment #############################
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY






############################# Define Agent #############################
llm = ChatOpenAI(
    model = "gpt-4o-mini",
    temperature=0.5,
)

text_magician = llm | StrOutputParser()





############################# Define Nodes #############################
def text_magician_node(state):
    """
    Summary / Expand the given text.

    Args : 
        state (dict) : The current graph state

    Returns :
        state (dict) : New key added to state, generation, that contains LLM generation
    """

    print("[Graph Log] TEXT_MAGICIAN ...")

    question = state["question"]
    updated_messages = add_messages(state["messages"], HumanMessage(content=question))
    state["messages"] = updated_messages

    generation = text_magician.invoke([HumanMessage(content=question)])
    state["generation"] = generation
    updated_messages = add_messages(state["messages"], AIMessage(content=generation))
    state["messages"] = updated_messages

    return state