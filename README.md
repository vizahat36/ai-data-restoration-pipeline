# ai-data-restoration-pipeline

Project workspace initialized and connected to GitHub.

## Structure

- Part-A
- Part-B
- reflections

## How To Run Part A

From the repository root, run:

1. Step 1: Generate dataset

```bash
python Part-A/generate_dataset.py
```

2. Step 2: Run cleaning pipeline

```bash
python Part-A/clean_data.py
```

3. Step 3: Generate quality report

```bash
python Part-A/quality_report.py
```

These scripts implement the full Part A workflow:

- `generate_dataset.py` -> data creation
- `clean_data.py` -> data validation and rejection handling
- `quality_report.py` -> data quality analysis