from langchain_community.chat_models import ChatOllama

from lwe.core.provider import Provider, PresetValue

CHAT_OLLAMA_DEFAULT_MODEL = "tinyllama"


class CustomChatOllama(ChatOllama):

    @property
    def _llm_type(self):
        """Return type of llm."""
        return "chat_ollama"


class ProviderChatOllama(Provider):
    """
    Access to Ollama chat models.
    """

    @property
    def model_property_name(self):
        return 'model'

    @property
    def capabilities(self):
        return {
            "chat": True,
            'validate_models': False,
            'models': {
                'llama2': {
                    'max_tokens': 4096,
                },
                'llama2:7b-chat': {
                    'max_tokens': 4096,
                },
                'llama2:13b-chat': {
                    'max_tokens': 4096,
                },
                'llama2:70b-chat': {
                    'max_tokens': 4096,
                },
                'llama2:7b-code': {
                    'max_tokens': 4096,
                },
                'llama2:13b-code': {
                    'max_tokens': 4096,
                },
                'llama2:34b-code': {
                    'max_tokens': 4096,
                },
                'orca-mini:7b': {
                    'max_tokens': 4096,
                },
                'orca-mini:13b': {
                    'max_tokens': 4096,
                },
                'orca-mini:70b': {
                    'max_tokens': 4096,
                },
                'vicuna:7b': {
                    'max_tokens': 4096,
                },
                'vicuna:13b': {
                    'max_tokens': 4096,
                },
                'vicuna:33b': {
                    'max_tokens': 4096,
                },
                'wizardcoder:7b-python': {
                    'max_tokens': 4096,
                },
                'wizardcoder:13b-python': {
                    'max_tokens': 4096,
                },
                'wizardcoder:34b-python': {
                    'max_tokens': 4096,
                },
                'starcoder:7b': {
                    'max_tokens': 4096,
                },
                'starcoder:15b': {
                    'max_tokens': 4096,
                },
                'sqlcoder:7b': {
                    'max_tokens': 4096,
                },
                'sqlcoder:15b': {
                    'max_tokens': 4096,
                },
                'zephyr:7b-beta': {
                    'max_tokens': 131072,
                },
                'tinyllama': {
                    'max_tokens': 2048,
                },
                'tinyllama:chat': {
                    'max_tokens': 2048,
                },
            }
        }

    @property
    def default_model(self):
        return CHAT_OLLAMA_DEFAULT_MODEL

    def prepare_messages_method(self):
        return self.prepare_messages_for_llm_chat

    def llm_factory(self):
        return CustomChatOllama

    def customization_config(self):
        return {
            'model': PresetValue(str, options=self.available_models),
            'temperature': PresetValue(float, min_value=0.0, max_value=2.0),
            'top_p': PresetValue(float, min_value=0.0, max_value=1.0),
            'top_k': PresetValue(int, min_value=1, max_value=40),
            "verbose": PresetValue(bool),
            "base_url": PresetValue(str, include_none=True),
        }
