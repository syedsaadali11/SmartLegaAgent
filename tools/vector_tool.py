from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.agents import Tool
from config.settings import VECTORSTORE_PATH, EMBEDDING_MODEL

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
vectorstore = Chroma(persist_directory=VECTORSTORE_PATH, embedding_function=embeddings)
retriever = vectorstore.as_retriever()

vector_tool = Tool(
    name="VectorStore",
    func=lambda q: "\n".join([
        doc.page_content for doc in retriever.invoke(q)
        if "pakistan penal code" in doc.page_content.lower() or "peca" in doc.page_content.lower()
    ]),
    description="Provides expert answers from Pakistan law documents."
)
