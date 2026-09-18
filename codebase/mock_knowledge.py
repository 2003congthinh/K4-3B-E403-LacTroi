import json
import re
from pathlib import Path
from typing import Dict, Optional


KNOWLEDGE_PATH = Path(__file__).resolve().parents[1] / "data" / "mock_discord_knowledge.json"


with KNOWLEDGE_PATH.open(encoding="utf-8") as knowledge_file:
    MOCK_KNOWLEDGE = json.load(knowledge_file)


def normalize_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\sàáạảãâầấậẩẫăằắặẳẵèéẹẻẽêềếệểễìíịỉĩòóọỏõôồốộổỗơờớợởỡùúụủũưừứựửữỳýỵỷỹđ\-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def find_mock_answer(question: str) -> Optional[Dict[str, str]]:
    if not question:
        return None
    normalized = normalize_text(question)
    best_match: Optional[Dict[str, str]] = None
    best_score = 0

    for item in MOCK_KNOWLEDGE:
        score = 0
        for kw in item["keywords"]:
            normalized_keyword = normalize_text(kw)
            if normalized_keyword in normalized:
                score += max(2, len(normalized_keyword.split()))
        if score > best_score:
            best_score = score
            best_match = item

    if best_score == 0:
        return None
    return best_match
