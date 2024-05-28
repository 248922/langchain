import os
import tempfile
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from streamlit_chat import message
from llm import PDFQuery
from base_prompt import get_base_prompt

st.set_page_config(page_title="AI学习助手",layout="wide")

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

def create_agent(agent_name:str):
    if "create" not in st.session_state:
        if agent_name=="计算机组成与体系结构":
            #name,prompt,file_path=st.secrets["agent"]
            name, prompt, file_path=["计算机组成与体系结构","default","计算机组成与系统结构（第二版）裘雪红 西电出版社.pdf"]
            base_prompt = get_base_prompt()
            if prompt=="default" or prompt=="":
                prompt="You are an AI teaching assistant, and you need to answer students' questions based on the content in the local knowledge base.Remember to answer questions in Chinese."
            combined_prompt = f"{base_prompt}{prompt}"
            st.session_state["pdfquery"].create_prompt(combined_prompt)
            st.session_state["pdfquery"].ingest("计算机组成与系统结构（第二版）裘雪红 西电出版社.pdf")
        st.session_state["create"]="ok"

def delete_agent():
    del st.session_state["create"]

def read_and_save_file():
    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name

        st.session_state["pdfquery"].ingest(file_path)
        os.remove(file_path)


def new_chat():
    st.session_state["messages"] = []
    st.session_state["chat_history"] = []
    st.session_state["messages"].append(("你好，很高兴遇见你！我是你的AI学习助手，请告诉我你的问题。", False))

def initialize():
    if "init" not in st.session_state:
        st.session_state["OPENAI_API_KEY"] =st.secrets["OPENAI_API_KEY"]
        st.session_state["pdfquery"] = PDFQuery(st.session_state["OPENAI_API_KEY"])
        st.session_state["ingestion_spinner"] = st.empty()
        new_chat()
        st.session_state["init"] = "ok"

def main():
    initialize()
    with st.sidebar:
        st.title(":blue[📝 AI 学习助手]")
        content = st.selectbox(
            '选择课程',
            (
            '计算机组成与体系结构', '数据结构', '计算机操作系统'),on_change=delete_agent)
        create_agent(content)
        st.subheader("上传文件")
        st.sidebar.file_uploader(
            "Upload document",
            type=["pdf"],
            key="file_uploader",
            on_change=read_and_save_file,
            label_visibility="collapsed",
            accept_multiple_files=True,
        )
        st.button("开始新对话", key="new_chat_button", on_click=new_chat)


    col1,col2,col3=st.columns([5,2,5])
    with col1:
        st.markdown('<p style="text-align: center;font-size: 24px;">计算机组成与系统结构（第二版）裘雪红 西电出版社</p>', unsafe_allow_html=True)
        pdf_url = "https://248922.github.io/langchain/计算机组成原理与系统结构课程教学改革探讨_郭玉峰.pdf"
        pdfjs_viewer_url = f"https://mozilla.github.io/pdf.js/web/viewer.html?file={pdf_url}"
        st.components.v1.iframe(pdfjs_viewer_url, width=500, height=700)
    with col3:
        st.subheader("📝 AI 学习助手")
        st.caption("🚀 A streamlit AI learning assistant powered by OpenAI")
        display_messages()
        st.divider()
        st.chat_input("请输入你的问题", key="user_input",on_submit=process_input)

if __name__ == "__main__":
    main()
