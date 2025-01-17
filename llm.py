from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from create_utils import create_agent
from base_prompt import get_base_prompt


class PDFQuery:
    def __init__(self, openai_api_key = None) -> None:
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
        self.llm = ChatOpenAI(api_key=openai_api_key,model="gpt-3.5-turbo", temperature=0)
        self.chain = None
        self.db = None
        self.system_prompt=get_base_prompt()

    def ask(self, question: str,chat_history: str) -> str:
        if self.chain is None:
            output = "Please, add a document."
        else:
            response = self.chain.invoke({
            "chat_history": chat_history,
            "input": question
            })
            output = response["output"]
        return output

    def ingest(self, file_path: os.PathLike) -> None:
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        splitted_documents = self.text_splitter.split_documents(documents)
        self.db = FAISS.from_documents(splitted_documents, self.embeddings).as_retriever(search_type="similarity", search_kwargs={"k": 6})

    def create_prompt(self, prompt_input: str)-> None:
        self.chain = create_agent(input_prompt=prompt_input, db=self.db, llm=self.llm)

    def forget(self) -> None:
        self.db = None
        self.chain = None