import pytest
from streamlit_authenticator import Hasher

from services import auth_service


def test_build_credentials_contains_known_usernames():
    credentials = auth_service.build_credentials()
    assert credentials["usernames"]["hoge"]["name"] == "山田 太郎"
    assert credentials["usernames"]["fuga"]["name"] == "佐藤 花子"


def test_get_user_id_by_username_known():
    assert auth_service.get_user_id_by_username("hoge") == "user-001"
    assert auth_service.get_user_id_by_username("fuga") == "user-002"


def test_get_user_id_by_username_unknown_raises():
    with pytest.raises(ValueError):
        auth_service.get_user_id_by_username("unknown-user")


def test_demo_passwords_match_stored_hashes():
    """README記載のデモ用パスワードと、保存されているハッシュが一致することを保証する。"""
    credentials = auth_service.build_credentials()
    assert Hasher.check_pw("demo-pass-001", credentials["usernames"]["hoge"]["password"])
    assert Hasher.check_pw("demo-pass-002", credentials["usernames"]["fuga"]["password"])
