import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List


FACTS_PATH = Path(__file__).resolve().parents[1] / "data" / "school_facts.json"
STOP_WORDS = {
    "anh", "bạn", "cho", "có", "của", "đang", "được", "em", "hỏi", "khi",
    "không", "là", "mình", "nào", "này", "ngày", "nhé", "như", "ở", "thì",
    "theo", "trình", "viên", "về", "với", "xin", "học", "ạ", "lab",
}

with FACTS_PATH.open(encoding="utf-8") as facts_file:
    SCHOOL_FACTS = json.load(facts_file).get("facts", [])


def _normalize(text: str) -> str:
    normalized = unicodedata.normalize("NFD", text.lower())
    normalized = "".join(char for char in normalized if unicodedata.category(char) != "Mn")
    normalized = normalized.replace("đ", "d")
    return re.sub(r"[^a-z0-9\s]", " ", normalized)


def _tokens(text: str) -> set[str]:
    return {
        token
        for token in _normalize(text).split()
        if len(token) > 1 and token not in {_normalize(word) for word in STOP_WORDS}
    }


def find_relevant_facts(question: str, limit: int = 8) -> List[Dict[str, Any]]:
    """Return the highest-overlap facts without treating them as instructions."""
    question_tokens = _tokens(question)
    if not question_tokens:
        return []

    ranked = []
    for fact in SCHOOL_FACTS:
        searchable = " ".join(
            str(fact.get(field, ""))
            for field in ("topic", "statement", "context_question", "status")
        )
        fact_tokens = _tokens(searchable)
        overlap = question_tokens & fact_tokens
        if not overlap:
            continue

        topic_tokens = _tokens(str(fact.get("topic", "")).replace("_", " "))
        topic_overlap = question_tokens & topic_tokens
        confidence_bonus = {
            "curated_digest": 1,
            "watch_list_unresolved": 0,
            "community_reply": -1,
        }.get(fact.get("confidence"), 0)
        score = len(overlap) + (3 * len(topic_overlap)) + confidence_bonus
        ranked.append((score, fact))

    ranked.sort(key=lambda item: item[0], reverse=True)
    return [fact for _, fact in ranked[:limit]]


def format_facts_for_prompt(facts: List[Dict[str, Any]]) -> str:
    if not facts:
        return "Không tìm thấy fact liên quan trong school_facts.json."

    lines = []
    for fact in facts:
        lines.append(
            " | ".join(
                [
                    f"id={fact.get('id', 'unknown')}",
                    f"confidence={fact.get('confidence', 'unknown')}",
                    f"statement={fact.get('statement', '')}",
                    f"source={fact.get('source', 'unknown')}",
                    f"status={fact.get('status', 'n/a')}",
                ]
            )
        )
    return "\n".join(lines)
