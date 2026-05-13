from langchain_community.vectorstores import (
    Chroma
)

from app.rag.custom_embeddings import (
    GenAIEmbeddings
)


CHROMA_PATH = (
    "app/chroma_db"
)


embeddings = GenAIEmbeddings()


vectordb = Chroma(

    persist_directory=CHROMA_PATH,

    embedding_function=embeddings
)


def retrieve_policy(query):

    docs = vectordb.similarity_search(

        query,

        k=3
    )

    return docs