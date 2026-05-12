from app.rag.retriever import (
    retrieve_policy
)


query = """
hotel budget policy
"""

docs = retrieve_policy(query)

print("\nRETRIEVED DOCUMENTS:\n")

for doc in docs:

    print(doc.page_content)

    print("\n=================\n")