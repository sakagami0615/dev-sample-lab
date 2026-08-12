"""ユーザー情報および、そのユーザーに関連する情報の取得を担当する。

データの取得元(現在は `user_repository.py` のダミー JSON)は意識せず、`User`
ドメインモデルを組み立てるロジックに専念する。
"""
from models.schemas import RelatedInfo, User
from services import user_repository


def get_user(user_id: str) -> User:
    user_row = next((row for row in user_repository.load_user_rows() if row.id == user_id), None)
    if user_row is None:
        raise ValueError(f"user not found: {user_id}")

    related_info = [
        RelatedInfo(title=row.title, description=row.description)
        for row in user_repository.load_user_related_info_rows()
        if row.user_id == user_id
    ]
    return User(id=user_row.id, name=user_row.name, related_info=related_info)
