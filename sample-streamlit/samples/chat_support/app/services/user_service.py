"""ユーザー情報および、そのユーザーに関連する情報の取得を担当する。

デモ段階ではダミーの JSON データを参照する。将来的には、ログインユーザー情報・
アクセス権・契約情報・サイトアクセス情報などからパーソナライズ情報を取得する
構造を想定している。
"""
import json
from pathlib import Path

from models.schemas import User

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "users.json"

DEFAULT_USER_ID = "user-001"


def _load_users(path: Path = DATA_PATH) -> list[User]:
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return [User(**item) for item in raw]


def get_user(user_id: str = DEFAULT_USER_ID) -> User:
    for user in _load_users():
        if user.id == user_id:
            return user
    raise ValueError(f"user not found: {user_id}")
