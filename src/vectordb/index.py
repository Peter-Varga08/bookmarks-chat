from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector

from vectordb.config import DB_CONNECTION


def init_store(collection_name: str = "bookmarks") -> PGVector:
    """
    Initialize a PGVector vectorstore instance with HuggingFace embeddings.
    """
    embeddings = HuggingFaceEmbeddings()
    vectorstore = PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=DB_CONNECTION,
        use_jsonb=True,
    )
    return vectorstore


def delete_store() -> None:
    vectorstore = init_store()
    vectorstore.drop_tables()


if __name__ == "__main__":
    init_store()
    # delete_store()

    # dummy_documents = get_dummy_documents()
    # vectorstore.add_documents(
    #     dummy_documents,
    #     names=[doc.metadata["name"] for doc in dummy_documents],
    # )
    # query_docs = vectorstore.similarity_search_with_score("plant", k=3)
    # results_table = pl.DataFrame(
    #     {
    #         "Name": [d[0].metadata['name'] for d in query_docs],
    #         "Annotation": [d[0].page_content for d in query_docs],
    #         "Similarity": [1-d[1] for d in query_docs],
    #     }
    # )
    # print(results_table)
