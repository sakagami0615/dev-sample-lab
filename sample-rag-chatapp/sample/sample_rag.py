import os

from langchain_openai import ChatOpenAI

from app.create_vectorstore import SAMPLE_HTML_DOC_LIST, create_vectorstore_of_url


def main() -> None:
    vectorstore = create_vectorstore_of_url(SAMPLE_HTML_DOC_LIST)
    question = "2025年の参院選の投票日はいつですか？"
    documents = vectorstore.similarity_search(question, k=4)
    context = "\n\n".join(document.page_content for document in documents)
    response = ChatOpenAI(model=os.environ["OPENAI_API_MODEL"]).invoke(
        [
            (
                "system",
                f"次の参考情報だけを根拠に回答してください。\n\n{context}",
            ),
            ("user", question),
        ]
    )
    print(f"質問: {question}")
    print(f"回答: {response.content}")


if __name__ == "__main__":
    main()
