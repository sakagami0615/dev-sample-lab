"""Streamlit UI に専念する。RAG/LLM の具体的な処理は Service 層に委譲する。"""
import streamlit as st

from services import chat_service, user_service

st.set_page_config(page_title="サポートポータル", page_icon="💬", layout="centered")
st.title("サポートポータル")

user = user_service.get_user(user_service.DEFAULT_USER_ID)

st.subheader(f"こんにちは、{user.name}さん")
st.markdown("**あなたに関連する情報**")
for info in user.related_info:
    st.markdown(f"- **{info.title}**: {info.description}")

st.divider()
st.subheader("お問い合わせ")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": chat_service.GREETING}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("質問を入力してください"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = chat_service.handle_message(user.id, prompt)

    with st.chat_message("assistant"):
        st.markdown(response.answer)
        if response.sources:
            st.caption("参照情報: " + ", ".join(response.sources))

    st.session_state.messages.append({"role": "assistant", "content": response.answer})
