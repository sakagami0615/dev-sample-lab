"""Streamlit UI に専念する。ログイン認証・RAG/LLM の具体的な処理は Service 層に委譲する。"""
import streamlit as st
import streamlit_authenticator as stauth
from dotenv import load_dotenv

from services import auth_service, chat_service, llm_repository, user_service

load_dotenv()

st.set_page_config(page_title="サポートポータル", page_icon="💬", layout="centered")
st.title("サポートポータル")

try:
    llm_repository.validate_config()
except RuntimeError as exc:
    st.error(str(exc))
    st.stop()

authenticator = stauth.Authenticate(
    auth_service.build_credentials(),
    cookie_name="chat_support_auth",
    # デモ用の固定キー。本番ではシークレット管理(Key Vault等)から取得する想定。
    cookie_key="chat-support-demo-cookie-key",
    cookie_expiry_days=1,
)
authenticator.login()

if st.session_state.get("authentication_status") is False:
    st.error("ユーザー名またはパスワードが正しくありません。")
    st.stop()
elif st.session_state.get("authentication_status") is None:
    st.warning("ユーザー名とパスワードを入力してください。")
    st.stop()

user_id = auth_service.get_user_id_by_username(st.session_state["username"])
user = user_service.get_user(user_id)

if st.session_state.get("chat_user_id") != user_id:
    st.session_state.chat_user_id = user_id
    st.session_state.messages = [
        {"role": "assistant", "content": chat_service.GREETING}
    ]

with st.sidebar:
    authenticator.logout("ログアウト")

st.subheader(f"こんにちは、{user.name}さん")
st.markdown("**あなたに関連する情報**")
for info in user.related_info:
    st.markdown(f"- **{info.title}**: {info.description}")

st.divider()
st.subheader("お問い合わせ")

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

    st.session_state.messages.append(
        {"role": "assistant", "content": response.answer}
    )
