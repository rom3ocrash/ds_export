#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Improved .DS_Store parser for local analysis with CSV and JSON output options.
"""

import os
import sys
import argparse
import csv
import json
from ds_store import DSStore

def parse_ds_store(local_path: str) -> list:
    """
    Parse the .DS_Store file and return a sorted list of entries.
    """
    if not os.path.isfile(local_path):
        print(f'[ERROR] File not found: {local_path}')
        return []

    print(f'[INFO] Parsing: {local_path}\n')
    entries = set()

    try:
        with open(local_path, 'rb') as f:
            d = DSStore.open(f)
            for entry in d._traverse(None):
                entries.add(entry.filename)
            d.close()
    except Exception as e:
        print(f'[ERROR] Unable to read the .DS_Store file: {e}')
        return []

    sorted_entries = sorted(entries)
    if sorted_entries:
        print('[INFO] .DS_Store content found:')
        for entry in sorted_entries:
            print(f' - {entry}')
    else:
        print('[INFO] No files or directories found in .DS_Store.')
    return sorted_entries

def write_csv(entries: list, csv_path: str) -> None:
    """
    Write the entries to a CSV file.
    """
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['filename'])
            for entry in entries:
                writer.writerow([entry])
        print(f'[INFO] CSV output written to: {csv_path}')
    except Exception as e:
        print(f'[ERROR] Unable to write CSV file: {e}')

def write_json(entries: list, json_path: str) -> None:
    """
    Write the entries to a JSON file.
    """
    try:
        with open(json_path, 'w', encoding='utf-8') as jsonfile:
            json.dump(entries, jsonfile, indent=2, ensure_ascii=False)
        print(f'[INFO] JSON output written to: {json_path}')
    except Exception as e:
        print(f'[ERROR] Unable to write JSON file: {e}')

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Local .DS_Store parser with optional CSV and JSON output.')
    parser.add_argument('input_file', type=str, help='Path to the .DS_Store file')
    parser.add_argument('--csv', type=str, help='Output CSV file path')
    parser.add_argument('--json', type=str, help='Output JSON file path')
    args = parser.parse_args()

    entries = parse_ds_store(args.input_file)

    if args.csv:
        write_csv(entries, args.csv)
    if args.json:
        write_json(entries, args.json)

if __name__ == '__main__':
    main()
