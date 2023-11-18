from setuptools import find_packages, setup
import re
from os import path

FILE_DIR = path.dirname(path.abspath(path.realpath(__file__)))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    install_requirement = f.readlines()

with open(path.join(FILE_DIR, 'lwe_plugin_provider_chat_ollama', 'version.py')) as f:
    version = re.match(r'^__version__ = "([\w\.]+)"$', f.read().strip())[1]

setup(
    name="lwe-plugin-provider-chat-ollama",
    version=version,
    author="Chad Phillips",
    author_email="chad@apartmentlines.com",
    description="LWE plugin: Chat Ollama Provider plugin",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/llm-workflow-engine/lwe-plugin-provider-chat-ollama",
    packages=find_packages(),
    install_requires=install_requirement,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "lwe_plugins": [
            "lwe_plugin_provider_chat_ollama = lwe_plugin_provider_chat_ollama.plugin:ProviderChatOllama"
        ]
    },
)
