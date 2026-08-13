import pytest

from models.schemas import KnowledgeDocument
from services import llm_repository, llm_service

DOCS = [
    KnowledgeDocument(
        id="doc-1",
        title="商品Aについて",
        answer="商品Aは月額980円のサブスクリプションサービスです。",
        keywords=["商品A"],
    ),
]


def test_generate_answer_calls_repository_with_grounded_prompt(monkeypatch):
    captured = {}

    def fake_generate(system_prompt: str, user_prompt: str) -> str:
        captured["system_prompt"] = system_prompt
        captured["user_prompt"] = user_prompt
        return "モック回答"

    monkeypatch.setattr(llm_repository, "generate", fake_generate)

    answer = llm_service.generate_answer("商品Aについて教えて", DOCS)

    assert answer == "モック回答"
    assert "参照情報の範囲内" in captured["system_prompt"]
    assert "商品Aについて" in captured["user_prompt"]
    assert "商品Aは月額980円のサブスクリプションサービスです。" in captured["user_prompt"]
    assert "商品Aについて教えて" in captured["user_prompt"]


def test_generate_answer_wraps_repository_errors(monkeypatch):
    def fake_generate(system_prompt: str, user_prompt: str) -> str:
        raise RuntimeError("boom")

    monkeypatch.setattr(llm_repository, "generate", fake_generate)

    with pytest.raises(llm_service.LLMGenerationError):
        llm_service.generate_answer("商品Aについて教えて", DOCS)
