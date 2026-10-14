"""LWE chat ollama provider integration."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from langchain_core.messages import BaseMessage
from langchain_ollama import ChatOllama
from typing_extensions import override
import requests

from lwe.core.provider import PresetValue, Provider

CHAT_OLLAMA_DEFAULT_MODEL = "tinyllama"


class CustomChatOllama(ChatOllama):
    """Keep an LWE default model for the maintained Ollama integration."""

    model: str = CHAT_OLLAMA_DEFAULT_MODEL

    @property
    @override
    def _llm_type(self) -> str:
        """Return type of llm."""
        return "chat_ollama"


class ProviderChatOllama(Provider):
    """
    Access to Ollama chat models.
    """

    @property
    @override
    def model_property_name(self) -> str:
        return "model"

    @property
    @override
    def capabilities(self) -> dict[str, bool]:
        return {
            "chat": True,
            "validate_models": True,
        }

    @property
    @override
    def default_model(self) -> str:
        return CHAT_OLLAMA_DEFAULT_MODEL

    def fetch_models(self) -> dict[str, dict[str, int | None]]:
        llm = ChatOllama(model=CHAT_OLLAMA_DEFAULT_MODEL)
        base_url = llm.base_url or "http://localhost:11434"
        models_url = f"{base_url}/api/tags"
        model_info_url = f"{base_url}/api/show"
        headers = {
            "content-type": "application/json",
        }
        try:
            response = requests.get(models_url, headers=headers)
            response.raise_for_status()
            models_data = response.json()
            models_list = models_data.get("models")
            if not models_list:
                raise ValueError("Could not retrieve models")
            models = {}
            for model in models_list:
                name = model["name"]
                data = {"name": name}
                response = requests.post(model_info_url, headers=headers, json=data)
                response.raise_for_status()
                model_data = response.json()
                context_length = next(
                    (
                        value
                        for key, value in model_data["model_info"].items()
                        if key.endswith(".context_length")
                    ),
                    None,
                )
                if context_length:
                    models[name] = {"max_tokens": context_length}
            return models
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Could not retrieve models: {e}")

    @override
    def prepare_messages_method(
        self,
    ) -> Callable[[list[dict[str, Any]]], list[BaseMessage]]:
        return self.prepare_messages_for_llm_chat

    @override
    def llm_factory(self) -> type[CustomChatOllama]:
        return CustomChatOllama

    @override
    def customization_config(self) -> dict[str, Any]:
        return {
            "model": PresetValue(str, options=self.available_models),
            "temperature": PresetValue(float, min_value=0.0, max_value=2.0),
            "top_p": PresetValue(float, min_value=0.0, max_value=1.0),
            "top_k": PresetValue(int, min_value=1, max_value=40),
            "verbose": PresetValue(bool),
            "base_url": PresetValue(str, include_none=True),
        }
