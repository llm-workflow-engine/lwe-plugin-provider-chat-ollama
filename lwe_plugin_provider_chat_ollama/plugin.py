import requests

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
            'validate_models': True,
        }

    @property
    def default_model(self):
        return CHAT_OLLAMA_DEFAULT_MODEL

    def fetch_models(self):
        llm = ChatOllama()
        models_url = f"{llm.base_url}/api/tags"
        model_info_url = f"{llm.base_url}/api/show"
        headers = {
            "content-type": "application/json",
        }
        try:
            response = requests.get(models_url, headers=headers)
            response.raise_for_status()
            models_data = response.json()
            models_list = models_data.get('models')
            if not models_list:
                raise ValueError('Could not retrieve models')
            models = {}
            for model in models_list:
                name = model["name"]
                data = {"name": name}
                response = requests.post(model_info_url, headers=headers, json=data)
                response.raise_for_status()
                model_data = response.json()
                context_length = next((value for key, value in model_data["model_info"].items() if key.endswith(".context_length")), None)
                if context_length:
                    models[name] = {'max_tokens': context_length}
            return models
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Could not retrieve models: {e}")

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
