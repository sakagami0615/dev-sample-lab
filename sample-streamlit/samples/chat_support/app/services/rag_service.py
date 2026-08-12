"""RAG(検索)処理を担当する。

デモ段階ではローカルのダミーナレッジベース(JSON)をキーワード一致で検索する。
後から Azure AI Search 等の検索基盤に置き換えられるよう、UI やチャット制御からは
`search()` の入出力のみで利用できるようにしている。
"""
import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "knowledge_base.json"


def _load_documents(path: Path = DATA_PATH) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def search(query: str, top_k: int = 3) -> list[dict]:
    """クエリに含まれるキーワード数でナレッジベースをスコアリングし、上位を返す。"""
    scored = []
    for doc in _load_documents():
        score = sum(1 for keyword in doc["keywords"] if keyword in query)
        if score > 0:
            scored.append((score, doc))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [doc for _, doc in scored[:top_k]]
