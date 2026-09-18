import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional


LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_DIR.mkdir(exist_ok=True)


def log_event(event_name: str, payload: Optional[Dict[str, Any]] = None, **extra: Any) -> Dict[str, Any]:
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": event_name,
        "payload": payload or {},
    }
    if extra:
        record.update(extra)

    log_path = LOG_DIR / "events.jsonl"
    with log_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return record


def log_prompt_response(provider: str, model: str, user_input: str, response: str, status: str = "ok") -> Dict[str, Any]:
    return log_event(
        "llm_call",
        {
            "provider": provider,
            "model": model,
            "user_input": user_input,
            "response": response,
            "status": status,
        },
    )
