from langchain_community.document_loaders import (
    PyPDFLoader
)

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from langchain_community.vectorstores import (
    Chroma
)

from app.rag.custom_embeddings import (
    GenAIEmbeddings
)


PDF_PATH = (
    "app/policies/company_policy.pdf"
)

CHROMA_PATH = (
    "app/chroma_db"
)


def ingest_policy_documents():

    print("\nLoading PDF...\n")

    loader = PyPDFLoader(
        PDF_PATH
    )

    documents = loader.load()

    print(
        f"Loaded {len(documents)} pages."
    )

    # =========================
    # CHUNKING
    # =========================

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200
    )

    chunks = splitter.split_documents(
        documents
    )

    print(
        f"Created {len(chunks)} chunks."
    )

    # =========================
    # ENTERPRISE EMBEDDINGS
    # =========================

    embeddings = GenAIEmbeddings()

    # =========================
    # CHROMA VECTOR STORE
    # =========================

    vectordb = Chroma.from_documents(

        documents=chunks,

        embedding=embeddings,

        persist_directory=CHROMA_PATH
    )

    vectordb.persist()

    print(
        "\nPolicy RAG ingestion completed.\n"
    )


if __name__ == "__main__":

    ingest_policy_documents()