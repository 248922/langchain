import os
import tempfile
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from streamlit_chat import message
from llm import PDFQuery
st.set_page_config(page_title="AI学习助手")

def display_messages():
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()

def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        chat_history = st.session_state["chat_history"]
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking"):
            query_text = st.session_state["pdfquery"].ask(user_text,chat_history)

        st.session_state["chat_history"].append(HumanMessage(content=user_text))
        st.session_state["chat_history"].append(AIMessage(content=query_text))

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((query_text, False))

def create_agent():
    if st.session_state["prompt_input"]=="default":
        st.session_state["prompt_input"]="You are an AI teaching assistant, and you need to answer students' questions based on the content in the local knowledge base.Remember to answer questions in Chinese."
        st.session_state["pdfquery"].create_prompt(st.session_state["prompt_input"])
    else:
        st.session_state["pdfquery"].create_prompt(st.session_state["prompt_input"])
    new_chat()

def read_and_save_file():
    st.session_state["pdfquery"].forget()  # to reset the knowledge base

    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        with st.session_state["ingestion_spinner"], st.spinner(f"Ingesting {file.name}"):
            st.session_state["pdfquery"].ingest(file_path)
        os.remove(file_path)

def new_chat():
    st.session_state["messages"] = []
    st.session_state["chat_history"] = []
    st.session_state["user_input"] = ""
    st.session_state["messages"].append(("您好，很高兴遇见您！我是您的AI学习助手，请告诉我你的问题。", False))

def is_openai_api_key_set() -> bool:
    return len(st.session_state["OPENAI_API_KEY"]) > 0


def main():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["OPENAI_API_KEY"] = "sk-proj-z3EGPdku8gAI5IiUX87ZT3BlbkFJ8L2fp7nSzWpI2vapGajc"
        if is_openai_api_key_set():
            st.session_state["pdfquery"] = PDFQuery(st.session_state["OPENAI_API_KEY"])
        else:
            st.session_state["pdfquery"] = None
    st.header("🎓 AI学习助手")
    st.caption("我是一个AI学习助手，提交文档并给出你的问题，我将在文档中检索答案")
    st.subheader("上传知识库（pdf）")
    st.file_uploader(
        "Upload document",
        type=["pdf"],
        key="file_uploader",
        on_change=read_and_save_file,
        label_visibility="collapsed",
        accept_multiple_files=True,
        disabled=not is_openai_api_key_set(),
    )
    st.session_state["ingestion_spinner"] = st.empty()

    st.subheader("教师输入提示词创建智能体")
    st.text_input("在下方输入提示词",key="prompt_input",on_change=create_agent)
    st.divider()
    display_messages()
    st.chat_input("请输入你的问题", key="user_input",on_submit=process_input)
    st.button("开始新对话", key="new_chat_button",on_click=new_chat)
    st.divider()
    #st.page_link("streamlitui.py", label="Home")
    #st.page_link("pages/🧑‍🏫 teachers.py", label="🧑‍🏫 teachers")
    #st.page_link("pages/🧑 Students.py", label="🧑 Students")

if __name__ == "__main__":
    main()
