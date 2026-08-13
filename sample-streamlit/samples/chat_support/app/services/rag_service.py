"""RAG(検索)処理を担当する。

データの取得元(現在は `rag_repository.py` のダミー JSON)は意識せず、キーワード
スコアリングによる検索ロジックに専念する。UI やチャット制御からは `search()` の
入出力のみで利用できるようにしている。
"""
from models.schemas import KnowledgeDocument
from services import rag_repository


def _load_documents() -> list[KnowledgeDocument]:
    keywords_by_document_id: dict[str, list[str]] = {}
    for row in rag_repository.load_document_keyword_rows():
        keywords_by_document_id.setdefault(row.document_id, []).append(row.keyword)

    return [
        KnowledgeDocument(
            id=row.id,
            title=row.title,
            answer=row.answer,
            keywords=keywords_by_document_id.get(row.id, []),
        )
        for row in rag_repository.load_document_rows()
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
