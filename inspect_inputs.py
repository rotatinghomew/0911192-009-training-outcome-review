"""检查交接资料的表头、记录形状和关联编号。"""
import argparse
import csv
import json
from pathlib import Path


def load_tables(folder):
    schema = json.loads((folder / "schema.json").read_text(encoding="utf-8"))
    tables = {}
    for name, columns in schema["tables"].items():
        with (folder / f"{name}.csv").open(encoding="utf-8", newline="") as stream:
            reader = csv.reader(stream, strict=True)
            if next(reader, None) != columns:
                raise ValueError(f"{name}: 表头不符")
            records = []
            for line, row in enumerate(reader, 2):
                if len(row) != len(columns):
                    raise ValueError(f"{name}:{line}: 字段数量不符")
                records.append(dict(zip(columns, row)))
            tables[name] = records
    for child, field, parent, key in schema["references"]:
        allowed = {row[key] for row in tables[parent]}
        for line, row in enumerate(tables[child], 2):
            if row[field] and row[field] not in allowed:
                raise ValueError(f"{child}:{line}: {field} 不在 {parent}.{key} 中")
    return tables


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder", type=Path, nargs="?", default=Path(__file__).parent / "data")
    args = parser.parse_args()
    try:
        tables = load_tables(args.folder)
    except (ValueError, OSError, csv.Error) as error:
        parser.exit(2, f"资料校验失败：{error}\n")
    for name, rows in tables.items():
        print(f"{name}: {len(rows)} 条")


if __name__ == "__main__":
    main()
