from pathlib import Path

from fastapi.testclient import TestClient

from app import create_app


def make_client(tmp_path: Path) -> TestClient:
    return TestClient(create_app(tmp_path / "test-chat.db"))


def test_conversation_history_is_persisted_by_session(tmp_path: Path) -> None:
    with make_client(tmp_path) as client:
        created = client.post("/sessions")
        assert created.status_code == 201
        session_id = created.json()["session_id"]

        first = client.post(
            f"/sessions/{session_id}/messages",
            json={"message": "こんにちは"},
        )
        second = client.post(
            f"/sessions/{session_id}/messages",
            json={"message": "さっき何と言いましたか？"},
        )
        history = client.get(f"/sessions/{session_id}/messages")

    assert first.status_code == 201
    assert second.status_code == 201
    assert history.status_code == 200
    messages = history.json()["messages"]
    assert [message["role"] for message in messages] == [
        "user",
        "assistant",
        "user",
        "assistant",
    ]
    assert messages[0]["content"] == "こんにちは"
    assert "2件目" in messages[-1]["content"]


def test_unknown_session_returns_not_found(tmp_path: Path) -> None:
    with make_client(tmp_path) as client:
        response = client.get("/sessions/missing/messages")

    assert response.status_code == 404


def test_blank_message_is_rejected(tmp_path: Path) -> None:
    with make_client(tmp_path) as client:
        session_id = client.post("/sessions").json()["session_id"]
        response = client.post(
            f"/sessions/{session_id}/messages",
            json={"message": "   "},
        )

    assert response.status_code == 422


def test_session_can_be_deleted(tmp_path: Path) -> None:
    with make_client(tmp_path) as client:
        session_id = client.post("/sessions").json()["session_id"]
        deleted = client.delete(f"/sessions/{session_id}")
        history = client.get(f"/sessions/{session_id}/messages")

    assert deleted.status_code == 204
    assert history.status_code == 404
