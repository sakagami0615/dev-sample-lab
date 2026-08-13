"""ユーザーデータへのアクセスを担当する(デモ用のダミー実装)。

デモ段階では、DWH のディメンション/ファクトテーブルを模したローカル JSON
(`users` / `user_related_info`)を読み込む。本番でデータ取得元を実際の DWH 等
へ差し替える場合は、このファイルの中身だけを差し替えれば良い
(呼び出し元の `user_service.py` は変更不要な想定)。
"""
import json
from pathlib import Path

from models.schemas import UserRelatedInfoRow, UserRow

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
USERS_PATH = DATA_DIR / "users.json"
USER_RELATED_INFO_PATH = DATA_DIR / "user_related_info.json"


def load_user_rows(path: Path = USERS_PATH) -> list[UserRow]:
    with open(path, encoding="utf-8") as f:
        return [UserRow(**item) for item in json.load(f)]


def load_user_related_info_rows(path: Path = USER_RELATED_INFO_PATH) -> list[UserRelatedInfoRow]:
    with open(path, encoding="utf-8") as f:
        return [UserRelatedInfoRow(**item) for item in json.load(f)]
