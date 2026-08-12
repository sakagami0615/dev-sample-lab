"""ナレッジベースデータへのアクセスを担当する(デモ用のダミー実装)。

デモ段階では、DWH のディメンション/ブリッジテーブルを模したローカル JSON
(`kb_documents` / `kb_document_keywords`)を読み込む。本番で Azure AI Search 等
の検索基盤へ差し替える場合は、このファイルの中身だけを差し替えれば良い
(呼び出し元の `rag_service.py` は変更不要な想定)。
"""
import json
from pathlib import Path

from models.schemas import KnowledgeDocumentKeywordRow, KnowledgeDocumentRow

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DOCUMENTS_PATH = DATA_DIR / "kb_documents.json"
DOCUMENT_KEYWORDS_PATH = DATA_DIR / "kb_document_keywords.json"


def load_document_rows(path: Path = DOCUMENTS_PATH) -> list[KnowledgeDocumentRow]:
    with open(path, encoding="utf-8") as f:
        return [KnowledgeDocumentRow(**item) for item in json.load(f)]


def load_document_keyword_rows(path: Path = DOCUMENT_KEYWORDS_PATH) -> list[KnowledgeDocumentKeywordRow]:
    with open(path, encoding="utf-8") as f:
        return [KnowledgeDocumentKeywordRow(**item) for item in json.load(f)]
