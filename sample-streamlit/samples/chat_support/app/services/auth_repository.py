"""認証情報データへのアクセスを担当する(デモ用のダミー実装)。

デモ段階では、DWH のファクトテーブルを模したローカル JSON(`user_credentials`)
を読み込む。本番で実際の ID プロバイダ(Azure AD/Entra ID 等)へ差し替える場合は、
このファイルの中身だけを差し替えれば良い(呼び出し元の `auth_service.py` は変更
不要な想定)。
"""
import json
from pathlib import Path

from models.schemas import UserCredentialRow

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
USER_CREDENTIALS_PATH = DATA_DIR / "user_credentials.json"


def load_user_credential_rows(path: Path = USER_CREDENTIALS_PATH) -> list[UserCredentialRow]:
    with open(path, encoding="utf-8") as f:
        return [UserCredentialRow(**item) for item in json.load(f)]
