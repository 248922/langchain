from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import create_retriever_tool


def create_agent(input_prompt:str,db,llm):
    prompt = ChatPromptTemplate.from_messages([
        (
        "system", input_prompt),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user", "{input}"),
    ])
    retriever_tool = create_retriever_tool(
        db,
        "retriever_tool",
        "You should try to use this tool !",
    )
    tools = [retriever_tool]
    agent = create_openai_functions_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor
