import pytest

from services import llm_repository


def test_generate_raises_when_provider_unset(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER", raising=False)

    with pytest.raises(RuntimeError):
        llm_repository.generate("system", "user")


def test_generate_raises_when_provider_invalid(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "unknown-provider")

    with pytest.raises(RuntimeError):
        llm_repository.generate("system", "user")


def test_generate_raises_when_openai_api_key_missing(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError):
        llm_repository.generate("system", "user")


def test_generate_raises_when_ollama_base_url_missing(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.delenv("OLLAMA_BASE_URL", raising=False)

    with pytest.raises(RuntimeError):
        llm_repository.generate("system", "user")


def test_generate_raises_when_ollama_api_key_missing(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    monkeypatch.delenv("OLLAMA_API_KEY", raising=False)

    with pytest.raises(RuntimeError):
        llm_repository.generate("system", "user")


def test_generate_raises_when_openai_model_missing(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    with pytest.raises(RuntimeError):
        llm_repository.generate("system", "user")


def test_generate_raises_when_ollama_model_missing(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "ollama")
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    monkeypatch.setenv("OLLAMA_API_KEY", "test-key")
    monkeypatch.delenv("OLLAMA_MODEL", raising=False)

    with pytest.raises(RuntimeError):
        llm_repository.generate("system", "user")
