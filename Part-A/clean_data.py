import json
import re
from collections import Counter
from pathlib import Path


VALID_LANGUAGES = {"hindi", "hinglish", "english"}
VALID_OUTCOMES = {
	"payment_committed",
	"callback_scheduled",
	"escalated",
	"no_resolution",
}

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "raw_conversations.jsonl"
CLEAN_FILE = BASE_DIR / "cleaned_conversations.jsonl"
REJECT_FILE = BASE_DIR / "rejected_conversations.jsonl"

# Simple script/keyword heuristics for language mismatch detection.
DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")
LATIN_RE = re.compile(r"[A-Za-z]")
GARBLED_RE = re.compile(r"(?:Ã|ï»¿|�|\?\?\?|â|ê|û)")

HINGLISH_HINTS = {
	"aap",
	"hai",
	"nahi",
	"kar",
	"kal",
	"thoda",
	"payment",
	"emi",
	"sir",
	"maam",
	"ji",
}

ENGLISH_HINTS = {
	"please",
	"today",
	"tomorrow",
	"call",
	"payment",
	"overdue",
	"installment",
	"account",
	"thanks",
	"confirm",
}


def load_data(path: Path) -> list[dict]:
	rows: list[dict] = []
	with path.open("r", encoding="utf-8") as handle:
		for line_number, line in enumerate(handle, start=1):
			text = line.strip()
			if not text:
				continue
			try:
				payload = json.loads(text)
			except json.JSONDecodeError:
				payload = {
					"conversation_id": f"invalid_json_line_{line_number}",
					"turns": [],
					"metadata": {},
					"_parse_error": True,
				}
			rows.append(payload)
	return rows


def detect_empty_turn(turns: list[dict]) -> bool:
	for turn in turns:
		if not isinstance(turn, dict):
			return True
		text = turn.get("text", "")
		if not isinstance(text, str) or not text.strip():
			return True
	return False


def detect_duplicate_turn(turns: list[dict]) -> bool:
	for index in range(1, len(turns)):
		prev = turns[index - 1]
		curr = turns[index]
		if prev.get("role") == curr.get("role") and prev.get("text") == curr.get("text"):
			return True
	return False


def detect_short_conversation(turns: list[dict]) -> bool:
	return len(turns) < 2


def detect_invalid_metadata(metadata: dict | None) -> tuple[bool, str | None]:
	if not isinstance(metadata, dict):
		return True, "invalid_metadata"

	if "call_duration_seconds" not in metadata:
		return True, "invalid_metadata"
	if "outcome" not in metadata:
		return True, "missing_outcome"

	duration = metadata.get("call_duration_seconds")
	outcome = metadata.get("outcome")

	if not isinstance(duration, (int, float)):
		return True, "invalid_metadata"
	if duration <= 0:
		return True, "negative_call_duration"

	if not outcome:
		return True, "missing_outcome"
	if outcome not in VALID_OUTCOMES:
		return True, "invalid_metadata"

	return False, None


def detect_garbled_characters(turns: list[dict]) -> bool:
	for turn in turns:
		text = turn.get("text", "")
		if not isinstance(text, str):
			return True
		if GARBLED_RE.search(text):
			return True
	return False


def infer_language(turns: list[dict]) -> str:
	joined = " ".join(str(turn.get("text", "")) for turn in turns).strip()
	if not joined:
		return "unknown"

	has_devanagari = bool(DEVANAGARI_RE.search(joined))
	has_latin = bool(LATIN_RE.search(joined))

	lowered_tokens = re.findall(r"[a-zA-Z]+", joined.lower())
	hinglish_hits = sum(1 for token in lowered_tokens if token in HINGLISH_HINTS)
	english_hits = sum(1 for token in lowered_tokens if token in ENGLISH_HINTS)

	if has_devanagari and has_latin:
		return "hinglish"
	if has_devanagari and not has_latin:
		return "hindi"

	# Mostly Latin script: use keyword hints to split English vs Hinglish.
	if has_latin:
		if hinglish_hits > english_hits:
			return "hinglish"
		return "english"

	return "unknown"


def detect_language_mismatch(label: str, turns: list[dict]) -> bool:
	if label not in VALID_LANGUAGES:
		return True
	predicted = infer_language(turns)
	if predicted == "unknown":
		return True
	return predicted != label


def validate_conversation(conversation: dict) -> tuple[bool, str | None]:
	if conversation.get("_parse_error"):
		return False, "invalid_json"

	turns = conversation.get("turns")
	metadata = conversation.get("metadata")
	language = conversation.get("language")

	if not isinstance(turns, list):
		return False, "too_few_turns"
	if detect_short_conversation(turns):
		return False, "too_few_turns"
	if detect_empty_turn(turns):
		return False, "empty_turn"
	if detect_duplicate_turn(turns):
		return False, "duplicate_turn"

	invalid_metadata, metadata_reason = detect_invalid_metadata(metadata)
	if invalid_metadata:
		return False, metadata_reason

	if detect_garbled_characters(turns):
		return False, "garbled_text"
	if detect_language_mismatch(language, turns):
		return False, "language_mismatch"

	return True, None


def process_dataset(rows: list[dict]) -> tuple[list[dict], list[dict], Counter]:
	cleaned: list[dict] = []
	rejected: list[dict] = []
	rejection_stats: Counter = Counter()

	for item in rows:
		valid, reason = validate_conversation(item)
		if valid:
			cleaned.append(item)
			continue

		rejected_item = dict(item)
		rejected_item["rejection_reason"] = reason
		rejected.append(rejected_item)
		rejection_stats[reason] += 1

	return cleaned, rejected, rejection_stats


def write_jsonl(path: Path, rows: list[dict]) -> None:
	with path.open("w", encoding="utf-8") as handle:
		for row in rows:
			handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def main() -> None:
	rows = load_data(INPUT_FILE)
	cleaned, rejected, rejection_stats = process_dataset(rows)

	write_jsonl(CLEAN_FILE, cleaned)
	write_jsonl(REJECT_FILE, rejected)

	print("Cleaning complete")
	print(f"Raw conversations: {len(rows)}")
	print(f"Cleaned conversations: {len(cleaned)}")
	print(f"Rejected conversations: {len(rejected)}")
	print(f"Rejection reasons: {dict(rejection_stats)}")


if __name__ == "__main__":
	main()
