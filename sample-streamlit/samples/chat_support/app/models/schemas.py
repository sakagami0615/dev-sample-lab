"""Service間で共有するデータ型定義。"""
from pydantic import BaseModel


class RelatedInfo(BaseModel):
    title: str
    description: str


class User(BaseModel):
    id: str
    name: str
    related_info: list[RelatedInfo]


class ChatResponse(BaseModel):
    answer: str
    resolved: bool
    sources: list[str]
