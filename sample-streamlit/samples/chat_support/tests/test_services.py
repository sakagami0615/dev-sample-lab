import pytest

from services import chat_service, rag_service, user_service


def test_get_user_returns_known_user():
    user = user_service.get_user("user-001")
    assert user.name == "山田 太郎"


def test_get_user_unknown_raises():
    with pytest.raises(ValueError):
        user_service.get_user("unknown-id")


def test_rag_search_matches_keyword():
    docs = rag_service.search("商品Aについて教えてください")
    assert docs
    assert docs[0]["title"] == "商品Aについて"


def test_rag_search_no_match_returns_empty():
    assert rag_service.search("今日の天気は?") == []


def test_chat_service_resolved_for_known_topic():
    response = chat_service.handle_message("user-001", "商品Aについて教えて")
    assert response.resolved is True
    assert "商品A" in response.answer
    assert response.sources == ["商品Aについて"]


def test_chat_service_unresolved_for_unknown_topic():
    response = chat_service.handle_message("user-001", "今日の天気は?")
    assert response.resolved is False
    assert response.sources == []
    assert "山田 太郎" in response.answer
