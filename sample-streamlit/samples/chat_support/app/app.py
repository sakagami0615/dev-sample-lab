"""Streamlit UI に専念する。RAG/LLM の具体的な処理は Service 層に委譲する。"""
import os

import streamlit as st

from services import chat_service, user_service

USER_ID_ENV = "CHAT_SUPPORT_USER_ID"

st.set_page_config(page_title="サポートポータル", page_icon="💬", layout="centered")
st.title("サポートポータル")

user_id = os.environ.get(USER_ID_ENV)
if not user_id:
    st.error(
        f"ユーザーIDが設定されていません。環境変数 `{USER_ID_ENV}` にユーザーID"
        "(例: user-001)を設定して起動してください。"
        "\n\n本来はログイン認証から取得する値ですが、デモではこの環境変数で代替しています。"
    )
    st.stop()

user = user_service.get_user(user_id)

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
