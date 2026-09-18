import os
from pathlib import Path
from typing import Any, Dict, List, Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


ROOT_DIR = Path(__file__).resolve().parent.parent


def _load_local_env() -> None:
    env_path = ROOT_DIR / ".env"
    if not env_path.exists():
        return

    if load_dotenv is not None:
        load_dotenv(env_path, override=False)
        return

    with env_path.open("r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


_load_local_env()


PROVIDER_CONFIG = {
    "gpt": {
        "label": "OpenAI GPT",
        "env": "OPENAI_API_KEY",
        "models": ["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini"],
        "default_model": "gpt-4o-mini",
    },
    "gemini": {
        "label": "Google Gemini",
        "env": "GEMINI_API_KEY",
        "models": ["gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-2.5-flash", "antigravity", "gemini-3.1-flash-lite"],
        "default_model": "gemini-3.1-flash-lite",
    },
    "anthropic": {
        "label": "Anthropic Claude",
        "env": "ANTHROPIC_API_KEY",
        "models": ["claude-3-5-sonnet-latest", "claude-3-5-haiku-latest"],
        "default_model": "claude-3-5-sonnet-latest",
    },
    "azure-openai": {
        "label": "Azure OpenAI",
        "env": "AZURE_OPENAI_API_KEY",
        "models": ["gpt-4o-mini", "gpt-4o"],
        "default_model": "gpt-4o-mini",
    },
}


def get_available_providers() -> List[str]:
    providers = []
    for provider_name, config in PROVIDER_CONFIG.items():
        api_key = os.getenv(config["env"])
        if api_key:
            providers.append(provider_name)
    return providers


def get_models_for_provider(provider_name: str) -> List[str]:
    provider_name = provider_name.lower().strip()
    config = PROVIDER_CONFIG.get(provider_name)
    if not config:
        return []
    return config["models"]


def get_default_model(provider_name: str) -> str:
    provider_name = provider_name.lower().strip()
    config = PROVIDER_CONFIG.get(provider_name)
    if not config:
        return ""
    return config["default_model"]


def ensure_provider_ready(provider_name: str) -> None:
    provider_name = provider_name.lower().strip()
    config = PROVIDER_CONFIG.get(provider_name)
    if not config:
        raise ValueError(f"Unsupported provider: {provider_name}")

    api_key = os.getenv(config["env"])
    if not api_key:
        raise RuntimeError(f"Missing environment variable: {config['env']}")


def _messages_to_payload(messages: Optional[List[Dict[str, str]]]) -> List[Dict[str, str]]:
    if not messages:
        return [{"role": "user", "content": "Hello"}]
    return messages


def call_llm(
    provider_name: str,
    model: str,
    user_input: str,
    system_prompt: str = "",
    history: Optional[List[Dict[str, str]]] = None,
) -> Dict[str, Any]:
    provider_name = provider_name.lower().strip()
    ensure_provider_ready(provider_name)

    messages = list(history or [])
    if system_prompt:
        messages.insert(0, {"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_input})
    messages = _messages_to_payload(messages)

    if provider_name in {"gpt", "azure-openai"}:
        try:
            import openai
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install openai package: pip install openai") from exc

        api_key = os.getenv("OPENAI_API_KEY")
        if provider_name == "azure-openai":
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
            client = openai.AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=endpoint,
            )
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
        else:
            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )

        content = response.choices[0].message.content
        return {
            "provider": provider_name,
            "model": model,
            "response": content,
            "raw": response.model_dump() if hasattr(response, "model_dump") else str(response),
        }

    if provider_name == "gemini":
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install google-genai: pip install google-genai") from exc

        client = genai.Client(
            api_key=os.getenv("GEMINI_API_KEY"),
            http_options=types.HttpOptions(timeout=30000),
        )
        prompt = "\n".join(f"{msg['role']}: {msg['content']}" for msg in messages)
        result = client.models.generate_content(model=model, contents=prompt)
        return {
            "provider": provider_name,
            "model": model,
            "response": result.text or "",
            "raw": str(result),
        }

    if provider_name == "anthropic":
        try:
            import anthropic
        except ImportError as exc:  # pragma: no cover
            raise RuntimeError("Install anthropic package: pip install anthropic") from exc

        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        response = client.messages.create(
            model=model,
            max_tokens=512,
            system=system_prompt or None,
            messages=[{"role": msg["role"], "content": msg["content"]} for msg in messages if msg["role"] != "system"],
        )
        text = "".join(block.text for block in response.content if getattr(block, "type", None) == "text")
        return {
            "provider": provider_name,
            "model": model,
            "response": text,
            "raw": response.model_dump() if hasattr(response, "model_dump") else str(response),
        }

    raise RuntimeError(f"Provider not implemented: {provider_name}")
