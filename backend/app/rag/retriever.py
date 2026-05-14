import os

try:
    from langchain_community.vectorstores import (
        Chroma
    )

    from app.rag.custom_embeddings import (
        GenAIEmbeddings
    )
except Exception:
    Chroma = None
    GenAIEmbeddings = None


CHROMA_PATH = (
    "app/chroma_db"
)


def _load_vector_db():
    if os.getenv("ENABLE_POLICY_RAG", "false").lower() != "true":
        return None

    if not Chroma or not GenAIEmbeddings:
        return None

    try:
        return Chroma(
            persist_directory=CHROMA_PATH,
            embedding_function=GenAIEmbeddings()
        )
    except BaseException as exc:
        print("\nPOLICY RETRIEVER LOAD ERROR:\n")
        print(exc)
        return None


vectordb = None


def retrieve_policy(query):
    global vectordb

    if vectordb is None:
        vectordb = _load_vector_db()

    if not vectordb:
        return (
            "Policy retriever unavailable. Use conservative defaults: "
            "economy flights, business hotels, manager approval for violations."
        )

    try:
        docs = vectordb.similarity_search(
            query,
            k=3
        )
        return "\n\n".join(
            getattr(doc, "page_content", str(doc))
            for doc in docs
        )
    except BaseException as exc:
        print("\nPOLICY RETRIEVER ERROR:\n")
        print(exc)
        vectordb = None
        return (
            "Policy retrieval failed. Use conservative defaults: "
            "economy flights, business hotels, manager approval for violations."
        )
