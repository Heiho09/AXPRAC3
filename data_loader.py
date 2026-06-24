import json
from pathlib import Path

QTYPE_LABELS = {1: "객관식", 2: "단답형", 3: "서술형"}


def load_qa_data(data_dir=None):
    if data_dir is None:
        data_dir = Path(__file__).parent / "data" / "라벨링데이터"

    records = []
    for json_file in sorted(Path(data_dir).rglob("*.json")):
        department = json_file.parent.name
        try:
            with open(json_file, encoding="utf-8-sig") as f:
                item = json.load(f)
            records.append({
                "qa_id": item.get("qa_id"),
                "q_type": item.get("q_type"),
                "q_type_label": QTYPE_LABELS.get(item.get("q_type"), "기타"),
                "question": item.get("question", ""),
                "answer": item.get("answer", ""),
                "department": department,
            })
        except Exception:
            continue

    return records
