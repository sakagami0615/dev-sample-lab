"""ログイン認証を担当する。

`auth_repository`(認証情報)と `user_repository`(ユーザー情報)を `user_id` で
結合し、`streamlit_authenticator` が要求する資格情報の形に組み立てる。ログイン後は
`username` を内部の `user_id` に変換して、他の Service (`user_service` /
`chat_service`) へ引き渡す。
"""
from services import auth_repository, user_repository


def build_credentials() -> dict:
    """`streamlit_authenticator.Authenticate` に渡す資格情報辞書を組み立てる。"""
    users_by_id = {row.id: row for row in user_repository.load_user_rows()}

    usernames = {}
    for credential in auth_repository.load_user_credential_rows():
        user = users_by_id.get(credential.user_id)
        if user is None:
            continue
        usernames[credential.username] = {"name": user.name, "password": credential.password_hash}

    return {"usernames": usernames}


def get_user_id_by_username(username: str) -> str:
    """ログイン成功時に得られる `username` を内部の `user_id` に変換する。"""
    for credential in auth_repository.load_user_credential_rows():
        if credential.username == username:
            return credential.user_id
    raise ValueError(f"username not found: {username}")
