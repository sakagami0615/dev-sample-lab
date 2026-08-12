"""Service間で共有するデータ型定義。

Row系のモデルは DWH のディメンション/ファクトテーブルを模したダミーデータ
(`data/*.json`)の1行に対応する。Service層はこれらを外部キー(`user_id` /
`document_id`)で結合し、UIが扱う集約済みのドメインモデル(`User` /
`KnowledgeDocument`)を組み立てる。
"""
from datetime import datetime

from pydantic import BaseModel


class UserRow(BaseModel):
    """`users` ディメンションテーブルの1行。"""

    id: str
    name: str
    source_system: str
    updated_at: datetime


class UserRelatedInfoRow(BaseModel):
    """`user_related_info` ファクトテーブルの1行(`user_id` で `users` に紐づく)。"""

    user_id: str
    title: str
    description: str
    source_system: str
    updated_at: datetime


class KnowledgeDocumentRow(BaseModel):
    """`kb_documents` ディメンションテーブルの1行。"""

    id: str
    title: str
    answer: str
    source_system: str
    updated_at: datetime


class KnowledgeDocumentKeywordRow(BaseModel):
    """`kb_document_keywords` ブリッジテーブルの1行(`document_id` で `kb_documents` に紐づく)。"""

    document_id: str
    keyword: str


class RelatedInfo(BaseModel):
    title: str
    description: str


class User(BaseModel):
    id: str
    name: str
    related_info: list[RelatedInfo]


class KnowledgeDocument(BaseModel):
    id: str
    title: str
    answer: str
    keywords: list[str]


class ChatResponse(BaseModel):
    answer: str
    resolved: bool
    sources: list[str]
