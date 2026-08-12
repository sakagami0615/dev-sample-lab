"""ユーザー情報および、そのユーザーに関連する情報の取得を担当する。

デモ段階では DWH のディメンション/ファクトテーブルを模したダミー JSON
(`users` / `user_related_info`)を `user_id` で結合して取得する。将来的には、
ログインユーザー情報・アクセス権・契約情報・サイトアクセス情報などを実際の DWH
から取得する構造を想定している。
"""
import json
from pathlib import Path

from models.schemas import RelatedInfo, User, UserRelatedInfoRow, UserRow

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
USERS_PATH = DATA_DIR / "users.json"
USER_RELATED_INFO_PATH = DATA_DIR / "user_related_info.json"


def _load_user_rows(path: Path = USERS_PATH) -> list[UserRow]:
    with open(path, encoding="utf-8") as f:
        return [UserRow(**item) for item in json.load(f)]


def _load_user_related_info_rows(path: Path = USER_RELATED_INFO_PATH) -> list[UserRelatedInfoRow]:
    with open(path, encoding="utf-8") as f:
        return [UserRelatedInfoRow(**item) for item in json.load(f)]


def get_user(user_id: str) -> User:
    user_row = next((row for row in _load_user_rows() if row.id == user_id), None)
    if user_row is None:
        raise ValueError(f"user not found: {user_id}")

    related_info = [
        RelatedInfo(title=row.title, description=row.description)
        for row in _load_user_related_info_rows()
        if row.user_id == user_id
    ]
    return User(id=user_row.id, name=user_row.name, related_info=related_info)
