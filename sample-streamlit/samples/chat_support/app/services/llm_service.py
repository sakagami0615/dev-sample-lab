"""LLMによる回答生成のロジックを担当する。

ヒットしたナレッジ(`KnowledgeDocument`)からプロンプトを組み立て、`llm_repository.generate()` を
呼び出す。参照情報の範囲内でのみ回答させることでハルシネーションを抑制する。`llm_repository` 由来の
例外はここで `LLMGenerationError` にラップし、呼び出し元(`chat_service`)がOpenAI SDKの例外詳細を
知らずに済むようにする。
"""
import logging

from models.schemas import KnowledgeDocument
from services import llm_repository

logger = logging.getLogger(__name__)

CONTACT_INFO = "サポート窓口(support@example.com / 0120-000-000)までご連絡ください。"

SYSTEM_PROMPT = (
    "あなたはサポート窓口のアシスタントです。\n"
    "以下の参照情報の範囲内で質問に回答してください。\n"
    f"参照情報だけでは判断できない場合は、正直にその旨を伝え、{CONTACT_INFO}"
)


class LLMGenerationError(Exception):
    """LLM呼び出しに失敗したことを表すドメインレベルの例外。"""


def _build_context(docs: list[KnowledgeDocument]) -> str:
    return "\n\n".join(f"[{doc.title}] {doc.answer}" for doc in docs)


def _build_user_prompt(message: str, docs: list[KnowledgeDocument]) -> str:
    return f"参照情報:\n{_build_context(docs)}\n\n質問:\n{message}"


def generate_answer(message: str, docs: list[KnowledgeDocument]) -> str:
    user_prompt = _build_user_prompt(message, docs)
    try:
        return llm_repository.generate(SYSTEM_PROMPT, user_prompt)
    except Exception as exc:
        logger.exception("LLM呼び出しに失敗しました")
        raise LLMGenerationError(str(exc)) from exc
