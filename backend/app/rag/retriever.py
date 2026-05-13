from langchain_community.embeddings import (
    HuggingFaceEmbeddings
)

from langchain_community.vectorstores import (
    Chroma
)


CHROMA_PATH = (
    "app/chroma_db"
)


embeddings = HuggingFaceEmbeddings(

    model_name=
    "sentence-transformers/all-MiniLM-L6-v2"
)


vectordb = Chroma(

    persist_directory=CHROMA_PATH,

    embedding_function=embeddings
)


def retrieve_policy(
    query
):

    docs = vectordb.similarity_search(

        query,

        k=3
    )

    context = "\n\n".join(

        [
            doc.page_content
            for doc in docs
        ]
    )

    return context