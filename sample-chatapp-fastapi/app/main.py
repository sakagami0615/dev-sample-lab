import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field, field_validator

from .database import ChatRepository


class MessageRequest(BaseModel):
    message: str = Field(max_length=2000)

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("message must not be blank")
        return value


def create_app(database_path: Path | None = None) -> FastAPI:
    repository = ChatRepository(
        database_path or Path(os.getenv("CHAT_DB_PATH", "chat.db"))
    )

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        repository.initialize()
        yield

    app = FastAPI(title="SQLite Chat History API", lifespan=lifespan)

    def require_session(session_id: str) -> None:
        if not repository.session_exists(session_id):
            raise HTTPException(status_code=404, detail="Session not found")

    @app.post("/sessions", status_code=status.HTTP_201_CREATED)
    def create_session() -> dict[str, str]:
        return {"session_id": repository.create_session()}

    @app.post(
        "/sessions/{session_id}/messages",
        status_code=status.HTTP_201_CREATED,
    )
    def post_message(session_id: str, request: MessageRequest) -> dict:
        require_session(session_id)
        user_message = repository.add_message(session_id, "user", request.message)
        user_message_count = sum(
            message["role"] == "user"
            for message in repository.list_messages(session_id)
        )
        reply = (
            f"{user_message_count}件目のメッセージ"
            f"「{request.message}」を受け取りました。"
        )
        assistant_message = repository.add_message(
            session_id, "assistant", reply
        )
        return {
            "session_id": session_id,
            "user_message": user_message,
            "assistant_message": assistant_message,
        }

    @app.get("/sessions/{session_id}/messages")
    def get_messages(session_id: str) -> dict:
        require_session(session_id)
        return {
            "session_id": session_id,
            "messages": repository.list_messages(session_id),
        }

    @app.delete(
        "/sessions/{session_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    def delete_session(session_id: str) -> Response:
        if not repository.delete_session(session_id):
            raise HTTPException(status_code=404, detail="Session not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return app


app = create_app()
