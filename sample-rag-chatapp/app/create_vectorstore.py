from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter

SAMPLE_HTML_DOC_LIST = [
    "https://www.nhk.or.jp/senkyo/database/sangiin/",
    "https://www.soumu.go.jp/2025senkyo/",
    "https://www.asahi.com/senkyo/saninsen/",
]


def create_vectorstore_of_url(url_list: list[str]) -> Chroma:
    raw_docs = WebBaseLoader(web_paths=url_list).load()
    docs = CharacterTextSplitter(chunk_size=300, chunk_overlap=30).split_documents(
        raw_docs
    )
    vectorstore = Chroma(
        collection_name="example_collection",
        embedding_function=OpenAIEmbeddings(),
        persist_directory="./chroma_db",
    )
    vectorstore.add_documents(docs)
    return vectorstore


if __name__ == "__main__":
    create_vectorstore_of_url(SAMPLE_HTML_DOC_LIST)
