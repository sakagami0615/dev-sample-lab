from uuid import uuid4

import streamlit as st
from langchain.agents import create_agent
from langchain_chroma import Chroma
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.checkpoint.memory import InMemorySaver

from app.setting import MODE, OPENAI_API_MODEL, OPENAI_API_TEMPERATURE, Mode


@st.cache_resource
def create_vectorstore() -> Chroma:
    return Chroma(
        collection_name="example_collection",
        embedding_function=OpenAIEmbeddings(),
        persist_directory="./chroma_db",
    )


def create_chat_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=OPENAI_API_MODEL,
        temperature=OPENAI_API_TEMPERATURE,
        streaming=True,
    )


def create_search_agent():
    return create_agent(
        model=create_chat_model(),
        tools=[
            DuckDuckGoSearchRun(),
            WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
        ],
        checkpointer=InMemorySaver(),
        system_prompt="必要に応じてWeb検索を使い、日本語で簡潔に回答してください。",
    )


def prepare_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid4())
    if "search_agent" not in st.session_state:
        st.session_state.search_agent = create_search_agent()


def render_chat_history() -> None:
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])


def is_question_for_document(vectorstore: Chroma, question: str) -> bool:
    results = vectorstore.similarity_search_with_relevance_scores(question, k=1)
    return bool(results and results[0][1] >= 0.7)


def answer_with_search(prompt: str) -> str:
    result = st.session_state.search_agent.invoke(
        {"messages": [{"role": "user", "content": prompt}]},
        {"configurable": {"thread_id": st.session_state.thread_id}},
    )
    return str(result["messages"][-1].content)


def answer_with_rag(vectorstore: Chroma, prompt: str) -> str:
    documents = vectorstore.similarity_search(prompt, k=4)
    context = "\n\n".join(document.page_content for document in documents)
    conversation = [
        (message["role"], message["content"])
        for message in st.session_state.messages
    ]
    response = create_chat_model().invoke(
        [
            (
                "system",
                "次の参考情報だけを根拠に日本語で回答してください。"
                "情報が不足している場合は、その旨を回答してください。\n\n"
                f"参考情報:\n{context}",
            ),
            *conversation,
            ("user", prompt),
        ]
    )
    return str(response.content)


def select_answer(vectorstore: Chroma, prompt: str) -> tuple[str, str | None]:
    if MODE == Mode.AGENT:
        return answer_with_search(prompt), None
    if MODE == Mode.RAG or is_question_for_document(vectorstore, prompt):
        return answer_with_rag(vectorstore, prompt), "📖"
    return answer_with_search(prompt), None


def main() -> None:
    st.title("LangChain RAGチャット")
    prepare_session_state()
    render_chat_history()

    prompt = st.chat_input("質問を入力してください")
    if not prompt:
        return

    with st.chat_message("user"):
        st.markdown(prompt)

    response, avatar = select_answer(create_vectorstore(), prompt)
    with st.chat_message("assistant", avatar=avatar):
        st.markdown(response)
    st.session_state.messages.extend(
        [
            {"role": "user", "content": prompt},
            {"role": "assistant", "avatar": avatar, "content": response},
        ]
    )


if __name__ == "__main__":
    main()
