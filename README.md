# ai-data-restoration-pipeline

Short take-home assignment repository for Kapture CX AI/ML internship.

## What Is Completed

Part A is implemented end-to-end:

- Synthetic messy dataset generation
- Data cleaning and rejection pipeline
- Quality analysis report
- Writeup with assumptions and scaling notes

## Repository Structure

- Part-A
- Part-B
- reflections

## Part A File Structure

```text
repo/
├── part_a/
│   ├── generate_dataset.py        # dataset generator
│   ├── raw_conversations.jsonl    # generated messy dataset
│   ├── clean_data.py              # cleaning pipeline
│   ├── quality_report.py          # analysis script
│   ├── cleaned_conversations.jsonl
│   ├── rejected_conversations.jsonl
│   └── writeup.md
```

Note: In this repository, the folder is named `Part-A` (same content as shown above in assignment format).

## Part A Quick Run

Run from repository root:

```bash
python Part-A/generate_dataset.py
python Part-A/clean_data.py
python Part-A/quality_report.py
```

## Part A Files

- `Part-A/raw_conversations.jsonl` - generated noisy source dataset
- `Part-A/clean_data.py` - validation and cleaning pipeline
- `Part-A/cleaned_conversations.jsonl` - training-ready output
- `Part-A/rejected_conversations.jsonl` - rejected records with reasons
- `Part-A/quality_report.py` - summary statistics and quality analysis
- `Part-A/writeup.md` - assumptions, hardest issue, scaling approach