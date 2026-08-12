"""チャット全体の制御を担当する。

ユーザー質問 → RAG検索 → 回答生成 → 回答可能か判定、の流れを実装する。
デモ段階では LLM 呼び出しの代わりに RAG のヒット結果からテンプレート的に回答を
組み立てる。後から実際の LLM 呼び出しに差し替えても、この関数のインターフェース
(引数・戻り値)は変わらない想定。
"""
from models.schemas import ChatResponse
from services import rag_service, user_service

GREETING = "何かご質問はありますか?"

CONTACT_INFO = "サポート窓口(support@example.com / 0120-000-000)までご連絡ください。"


def handle_message(user_id: str, message: str) -> ChatResponse:
    user = user_service.get_user(user_id)
    docs = rag_service.search(message)

    if not docs:
        return ChatResponse(
            answer=(
                f"{user.name}様、申し訳ございません。ご質問にお答えできる情報が"
                f"見つかりませんでした。{CONTACT_INFO}"
            ),
            resolved=False,
            sources=[],
        )

    return ChatResponse(
        answer=_generate_answer(docs),
        resolved=True,
        sources=[doc["title"] for doc in docs],
    )


def _generate_answer(docs: list[dict]) -> str:
    best = docs[0]
    return best["answer"]
