"""RAG(検索)処理を担当する。

デモ段階では DWH のディメンション/ブリッジテーブルを模したダミー JSON
(`kb_documents` / `kb_document_keywords`)を `document_id` で結合してキーワード
一致検索する。後から Azure AI Search 等の検索基盤に置き換えられるよう、UI やチャ
ット制御からは `search()` の入出力のみで利用できるようにしている。
"""
import json
from pathlib import Path

from models.schemas import KnowledgeDocument, KnowledgeDocumentKeywordRow, KnowledgeDocumentRow

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DOCUMENTS_PATH = DATA_DIR / "kb_documents.json"
DOCUMENT_KEYWORDS_PATH = DATA_DIR / "kb_document_keywords.json"


def _load_document_rows(path: Path = DOCUMENTS_PATH) -> list[KnowledgeDocumentRow]:
    with open(path, encoding="utf-8") as f:
        return [KnowledgeDocumentRow(**item) for item in json.load(f)]


def _load_document_keyword_rows(path: Path = DOCUMENT_KEYWORDS_PATH) -> list[KnowledgeDocumentKeywordRow]:
    with open(path, encoding="utf-8") as f:
        return [KnowledgeDocumentKeywordRow(**item) for item in json.load(f)]


def _load_documents() -> list[KnowledgeDocument]:
    keywords_by_document_id: dict[str, list[str]] = {}
    for row in _load_document_keyword_rows():
        keywords_by_document_id.setdefault(row.document_id, []).append(row.keyword)

    return [
        KnowledgeDocument(
            id=row.id,
            title=row.title,
            answer=row.answer,
            keywords=keywords_by_document_id.get(row.id, []),
        )
        for row in _load_document_rows()
    ]


def search(query: str, top_k: int = 3) -> list[KnowledgeDocument]:
    """クエリに含まれるキーワード数でナレッジベースをスコアリングし、上位を返す。"""
    scored = []
    for doc in _load_documents():
        score = sum(1 for keyword in doc.keywords if keyword in query)
        if score > 0:
            scored.append((score, doc))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]
