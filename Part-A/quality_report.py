import json
import statistics
from collections import Counter
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
RAW_FILE = BASE_DIR / "raw_conversations.jsonl"
CLEAN_FILE = BASE_DIR / "cleaned_conversations.jsonl"
REJECT_FILE = BASE_DIR / "rejected_conversations.jsonl"


def load_dataset(file_path: Path) -> list[dict]:
	rows: list[dict] = []
	with file_path.open("r", encoding="utf-8") as handle:
		for line in handle:
			text = line.strip()
			if not text:
				continue
			rows.append(json.loads(text))
	return rows


def language_distribution(rows: list[dict]) -> Counter:
	values = [item.get("language") for item in rows if item.get("language")]
	return Counter(values)


def outcome_distribution(rows: list[dict]) -> Counter:
	outcomes = []
	for item in rows:
		metadata = item.get("metadata") or {}
		outcome = metadata.get("outcome")
		if outcome:
			outcomes.append(outcome)
	return Counter(outcomes)


def turn_counts(rows: list[dict]) -> list[int]:
	return [len(item.get("turns", [])) for item in rows]


def average_turns(rows: list[dict]) -> float:
	counts = turn_counts(rows)
	if not counts:
		return 0.0
	return statistics.mean(counts)


def median_turns(rows: list[dict]) -> float:
	counts = turn_counts(rows)
	if not counts:
		return 0.0
	return statistics.median(counts)


def max_turns(rows: list[dict]) -> int:
	counts = turn_counts(rows)
	if not counts:
		return 0
	return max(counts)


def average_call_duration(rows: list[dict]) -> float:
	durations = []
	for item in rows:
		metadata = item.get("metadata") or {}
		duration = metadata.get("call_duration_seconds")
		if isinstance(duration, (int, float)):
			durations.append(float(duration))
	if not durations:
		return 0.0
	return statistics.mean(durations)


def rejection_analysis(rejected_rows: list[dict]) -> Counter:
	reasons = [item.get("rejection_reason", "unknown") for item in rejected_rows]
	return Counter(reasons)


def print_distribution(title: str, counter: Counter) -> None:
	print(f"\n{title}")
	print("-" * len(title))

	total = sum(counter.values())
	if total == 0:
		print("  No data")
		return

	for key, value in counter.most_common():
		pct = (value / total) * 100
		print(f"  {key}: {value} ({pct:.1f}%)")


def main() -> None:
	raw = load_dataset(RAW_FILE)
	cleaned = load_dataset(CLEAN_FILE)
	rejected = load_dataset(REJECT_FILE)

	print("DATASET SUMMARY")
	print("---------------")
	print(f"Raw conversations: {len(raw)}")
	print(f"Cleaned conversations: {len(cleaned)}")
	print(f"Rejected conversations: {len(rejected)}")

	print_distribution("Rejection Reasons", rejection_analysis(rejected))
	print_distribution("Language Distribution (Raw)", language_distribution(raw))
	print_distribution("Language Distribution (Cleaned)", language_distribution(cleaned))
	print_distribution("Outcome Distribution (Raw)", outcome_distribution(raw))
	print_distribution("Outcome Distribution (Cleaned)", outcome_distribution(cleaned))

	print("\nAverage Turns Per Conversation")
	print("------------------------------")
	print(f"Raw dataset: {average_turns(raw):.2f}")
	print(f"Cleaned dataset: {average_turns(cleaned):.2f}")

	print("\nBonus Statistics")
	print("----------------")
	print(f"Max turns (raw): {max_turns(raw)}")
	print(f"Max turns (cleaned): {max_turns(cleaned)}")
	print(f"Median turns (raw): {median_turns(raw):.2f}")
	print(f"Median turns (cleaned): {median_turns(cleaned):.2f}")
	print(f"Average call duration (raw): {average_call_duration(raw):.2f} seconds")
	print(f"Average call duration (cleaned): {average_call_duration(cleaned):.2f} seconds")


if __name__ == "__main__":
	main()
