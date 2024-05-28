import os
import tempfile
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from streamlit_chat import message
from llm import PDFQuery

st.set_page_config(page_title="新建智能体",layout="wide")

big_button_style = """
    <style>
        .stButton>button {
            width: 200px;
            height: 50px;
            background-color: #D1FFBD;
            color: black;
            border: none;
            padding: 15px 32px;
            text-align: center;
            font-size: 20px;
            font-weight: bold;
            transition: 0.3s;
            cursor: pointer;
        }
        .stButton>button:hover {
    background-color: #CCE8CC; /* 用于鼠标悬停时的反馈 */
        }
    </style>
    """
def none():
    1
def delete_agent():
    1
def edit_agent():
    1


def on_sure_click():
    st.session_state["Chapter_Name"].append(st.session_state["Chapter_Name_input"])
    st.session_state["prompt"].append(st.session_state["prompt_input"])

def display_chapter():
    st.divider()
    col1, col2, col3, col4, col5 = st.columns([2, 5, 2, 2, 1])
    with col1:
        st.write(" ")
        st.subheader("已创建智能体：")
    with col3:
        st.markdown(big_button_style, unsafe_allow_html=True)
        st.button("编辑", key="edit", on_click=edit_agent)
    with col4:
        st.markdown(big_button_style, unsafe_allow_html=True)
        st.button("➖ 删除智能体", key="delete_chapter", on_click=delete_agent)
    st.write(" ")
    for i, (name) in enumerate(st.session_state["Chapter_Name"]):
        col0,col1, col2, col3 = st.columns([0.3,1.7,9,1])
        with col1:
            st.write(" ")
            st.markdown("<p style='font-size: 24px;font-weight: bold;'>名称：</p>", unsafe_allow_html=True)
            st.write(" ")
            st.write(" ")
            st.markdown("<p style='font-size: 24px;font-weight: bold;'>提示词：</p>", unsafe_allow_html=True)
            st.write(" ")
            st.markdown("<p style='font-size: 24px;font-weight: bold;'>知识库：</p>", unsafe_allow_html=True)

        with col2:
            st.info(name)
            if st.session_state["prompt"][i] == "default" or st.session_state["prompt"][i] =="":
                prompt = "You are an AI teaching assistant, and you need to answer students' questions based on the content in the local knowledge base.Remember to answer questions in Chinese."
            else:
                prompt=st.session_state["prompt"][i]
            st.info(prompt)
            st.info(st.session_state["file"])
        #st.secrets["agent"]=[name,prompt,file_path]



def read_and_save_file():
    for file in st.session_state["file_uploader"]:
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            tf.write(file.getbuffer())
            file_path = tf.name
            st.session_state["file_path"].append(file_path)
        os.remove(file_path)



def initialize():
    st.session_state["file_path"] = []
    st.session_state["Chapter_Name"]=[]
    st.session_state["prompt"]=[]

def main():
    initialize()
    st.header("🤖创建智能体")
    st.divider()
    with st.container():
        col1, col2,col3 = st.columns([2, 9, 1])
        with col1:
            st.write(" ")
            st.write(" ")
            st.markdown("<p style='font-size: 24px;font-weight: bold;'>🏷️命名智能体</p>", unsafe_allow_html=True)
            st.write(" ")
            st.markdown("<p style='font-size: 24px;font-weight: bold;'>📄上传知识库</p>", unsafe_allow_html=True)
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.write(" ")
            st.markdown("<p style='font-size: 24px;font-weight: bold;'>⚙️输入提示词</p>", unsafe_allow_html=True)
        with col2:
            st.text_input("Chapter_Name:", key="Chapter_Name_input")
            file = st.file_uploader(
                "Upload document",
                type=["pdf"],
                key="file_uploader",
                on_change=read_and_save_file,
                label_visibility="collapsed",
                accept_multiple_files=True,
            )
            formatted_filenames = []
            if file:  # 检查是否有文件被上传
                for index, uploaded_file in enumerate(file):
                    if uploaded_file is not None:  # 确保文件不为空
                        formatted_filenames.append(f"{index + 1}.{uploaded_file.name}")

            st.session_state["file"] = ", ".join(formatted_filenames)
            st.text_area("在下方输入提示词", height=120, placeholder="default：You are an AI teaching assistant, and you need to answer students' questions based on the content in the local knowledge base."
                          ,key="prompt_input")

        st.markdown(big_button_style, unsafe_allow_html=True)
        col1,col2,col3,col4,col5 = st.columns(5)
        with col3:
            sure_button = st.button("确定", key="sure")
        if sure_button:
            on_sure_click()
            display_chapter()
        st.divider()

if __name__ == "__main__":
    main()
