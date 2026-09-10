#!/usr/bin/env python3
"""Generate one SCAD file per CSV row using the master lid model."""

import argparse
import csv
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent
BOUNDARY = "module __Customizer_Limit__"
ASSIGNMENT = re.compile(r"^(\s*([A-Za-z_]\w*)\s*=\s*)([^;\n]+)(;)", re.MULTILINE)
NUMBER = re.compile(r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?")


def generate(csv_path: Path, template_path: Path, output_dir: Path) -> list[Path]:
    template = template_path.read_text(encoding="utf-8")
    header, boundary, body = template.partition(BOUNDARY)
    if not boundary:
        raise ValueError(f"Template must contain {BOUNDARY!r}")
    parameters = [match.group(2) for match in ASSIGNMENT.finditer(header)]
    if not parameters or len(parameters) != len(set(parameters)):
        raise ValueError("Template must have unique parameter assignments above the boundary")

    outputs = []
    seen = set()
    with csv_path.open(newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields = reader.fieldnames or []
        if (not fields or fields[0] != "name" or len(fields) != len(set(fields))
                or set(fields[1:]) != set(parameters)):
            raise ValueError("CSV header must be name followed by these parameters: "
                             + ", ".join(parameters))
        for row in reader:
            line = reader.line_num
            if None in row or any(value is None for value in row.values()):
                raise ValueError(f"CSV line {line}: wrong number of columns")
            name = row["name"].strip()
            if name.endswith(".scad"):
                name = name[:-5]
            if not name or name in {".", ".."} or any(c in name for c in '/\\\x00'):
                raise ValueError(f"CSV line {line}: name must be a filename without a directory")
            destination = output_dir / (name + ".scad")
            resolved = destination.resolve()
            if resolved in {template_path.resolve(), csv_path.resolve(), Path(__file__).resolve()}:
                raise ValueError(f"CSV line {line}: output would overwrite an input or the script")
            if resolved in seen:
                raise ValueError(f"CSV line {line}: duplicate output filename {destination.name!r}")
            seen.add(resolved)
            values = {key: row[key].strip() for key in parameters}
            for key, value in values.items():
                if not NUMBER.fullmatch(value):
                    raise ValueError(f"CSV line {line}: {key} must contain a number, got {value!r}")
            rendered = ASSIGNMENT.sub(
                lambda match: match.group(1) + values[match.group(2)] + match.group(4),
                header,
            ) + boundary + body
            outputs.append((destination, rendered))
    if not outputs:
        raise ValueError("CSV must contain at least one data row")

    # Validate every row before writing any files.
    output_dir.mkdir(parents=True, exist_ok=True)
    for destination, rendered in outputs:
        destination.write_text(rendered, encoding="utf-8")
    return [destination for destination, _ in outputs]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", nargs="?", type=Path, default=ROOT / "parameters.csv")
    parser.add_argument("--template", type=Path, default=ROOT / "jar_lids.scad")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "generated")
    args = parser.parse_args()
    try:
        paths = generate(args.csv, args.template, args.output_dir)
    except (OSError, ValueError, csv.Error) as error:
        parser.exit(1, f"Error: {error}\n")
    for path in paths:
        print(f"Created {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
