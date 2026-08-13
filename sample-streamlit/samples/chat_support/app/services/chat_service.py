"""チャット全体の制御を担当する。

ユーザー質問 → RAG検索 → LLMによる回答生成 → 回答可能か判定、の流れを実装する。
回答生成は `llm_service.generate_answer()` に委譲しており、`LLM_PROVIDER` 環境変数で
OpenAI / Ollama を切り替えられる(詳細は `llm_repository.py` を参照)。
"""
from models.schemas import ChatResponse
from services import llm_service, rag_service, user_service

GREETING = "何かご質問はありますか?"


def handle_message(user_id: str, message: str) -> ChatResponse:
    user = user_service.get_user(user_id)
    docs = rag_service.search(message)

    if not docs:
        return ChatResponse(
            answer=(
                f"{user.name}様、申し訳ございません。ご質問にお答えできる情報が"
                f"見つかりませんでした。{llm_service.CONTACT_INFO}"
            ),
            resolved=False,
            sources=[],
        )

    try:
        answer = llm_service.generate_answer(message, docs)
    except llm_service.LLMGenerationError:
        return ChatResponse(
            answer=f"回答生成中にエラーが発生しました。{llm_service.CONTACT_INFO}",
            resolved=False,
            sources=[],
        )

    return ChatResponse(
        answer=answer,
        resolved=True,
        sources=[doc.title for doc in docs],
    )
