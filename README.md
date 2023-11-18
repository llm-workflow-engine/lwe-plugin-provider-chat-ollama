# LLM Workflow Engine (LWE) Chat Ollama Provider plugin

Chat Ollama Provider plugin for [LLM Workflow Engine](https://github.com/llm-workflow-engine/llm-workflow-engine)

Access to [Ollama](https://ollama.ai/library) chat models.

## Installation

### Ollama local server

Follow the [installation instructions](https://github.com/jmorganca/ollama) for Ollama, and make sure the server is running on port `11434`.

### Plugin

#### From packages

Install the latest version of this software directly from github with pip:

```bash
pip install git+https://github.com/llm-workflow-engine/lwe-plugin-provider-chat-ollama
```

#### From source (recommended for development)

Install the latest version of this software directly from git:

```bash
git clone https://github.com/llm-workflow-engine/lwe-plugin-provider-chat-ollama.git
```

Install the development package:

```bash
cd lwe-plugin-provider-chat-ollama
pip install -e .
```

## Configuration

Add the following to `config.yaml` in your profile:

```yaml
plugins:
  enabled:
    - provider_chat_ollama
    # Any other plugins you want enabled...
```

## Usage

From a running LWE shell:

```
/provider chat_ollama
/model model llama2
```
