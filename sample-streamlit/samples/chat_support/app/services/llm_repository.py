"""LLM(OpenAI / Ollama)への実APIコールを担当する。

`LLM_PROVIDER` 環境変数で呼び出し先を切り替える。Ollama は OpenAI 互換の
`/v1/chat/completions` エンドポイントを提供しているため、`openai` パッケージ1つで
両プロバイダに対応する。設定不備(未設定の環境変数)は暗黙のデフォルトで動き続けず、
`RuntimeError` を送出して即座に失敗させる。
"""
import os

from openai import OpenAI


def validate_config() -> None:
    """`LLM_PROVIDER` 等の設定を検証する(クライアントは作らない)。アプリ起動時に
    呼び出し、設定不備を最初のチャット送信を待たずに検知するために使う。
    """
    provider = os.environ.get("LLM_PROVIDER")

    if provider == "openai":
        if not os.environ.get("OPENAI_API_KEY"):
            raise RuntimeError(
                "OPENAI_API_KEY が設定されていません。LLM_PROVIDER=openai を使う場合は必須です。"
            )
        if not os.environ.get("OPENAI_MODEL"):
            raise RuntimeError(
                "OPENAI_MODEL が設定されていません。LLM_PROVIDER=openai を使う場合は必須です。"
            )
        return

    if provider == "ollama":
        if not os.environ.get("OLLAMA_BASE_URL"):
            raise RuntimeError(
                "OLLAMA_BASE_URL が設定されていません。LLM_PROVIDER=ollama を使う場合は必須です。"
            )
        if not os.environ.get("OLLAMA_API_KEY"):
            raise RuntimeError(
                "OLLAMA_API_KEY が設定されていません。LLM_PROVIDER=ollama を使う場合は必須です。"
            )
        if not os.environ.get("OLLAMA_MODEL"):
            raise RuntimeError(
                "OLLAMA_MODEL が設定されていません。LLM_PROVIDER=ollama を使う場合は必須です。"
            )
        return

    raise RuntimeError(
        f"LLM_PROVIDER には 'openai' または 'ollama' を指定してください(現在の値: {provider!r})。"
    )


def _build_client_and_model() -> tuple[OpenAI, str]:
    validate_config()
    provider = os.environ.get("LLM_PROVIDER")

    if provider == "openai":
        api_key = os.environ.get("OPENAI_API_KEY")
        model = os.environ.get("OPENAI_MODEL")
        return OpenAI(api_key=api_key, timeout=30.0), model

    model = os.environ.get("OLLAMA_MODEL")
    base_url = os.environ.get("OLLAMA_BASE_URL")
    api_key = os.environ.get("OLLAMA_API_KEY")

    client = OpenAI(api_key=api_key, base_url=base_url, timeout=30.0)
    return client, model


def generate(system_prompt: str, user_prompt: str) -> str:
    client, model = _build_client_and_model()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content
