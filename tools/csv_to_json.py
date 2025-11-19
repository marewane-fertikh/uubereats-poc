import csv
import json
import sys
from pathlib import Path

def csv_to_json(csv_file, json_file):
    csv_path = Path(csv_file)
    json_path = Path(json_file)

    if not csv_path.exists():
        print(f"Fichier introuvable : {csv_file}")
        return

    rows = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=4, ensure_ascii=False)

    print(f"[OK] JSON généré : {json_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage : python tools/csv_to_json.py <input.csv> <output.json>")
        exit(1)

    csv_to_json(sys.argv[1], sys.argv[2])
