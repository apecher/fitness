# Garmin FIT to CSV

A small Python utility that converts Garmin `.fit` activity files into CSV for easier analysis.

## Requirements

- Python 3.8+
- [`fitparse`](https://pypi.org/project/fitparse/)

Install the dependency:

```bash
python3 -m pip install fitparse
```

## Usage

Convert a single FIT file (writes `activity.csv` by default):

```bash
python3 fit2csv.py activity.fit
```

Convert a single FIT file and choose the output path:

```bash
python3 fit2csv.py activity.fit output.csv
```

Batch convert all `.fit` files in a directory (non-recursive). Output defaults to the input directory:

```bash
python3 fit2csv.py /path/to/folder/with/fits
```

Batch convert with a different output directory:

```bash
python3 fit2csv.py /path/to/folder/with/fits /path/to/output_folder
```

## Notes

- The script extracts `record` messages from the FIT file and writes them as CSV rows.
- If no `record` messages exist, an empty CSV file is created.
