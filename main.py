from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from adbeam_excel_parser.excel_reader import read_excel_summary


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read an Excel file and print a JSON summary for site-audit parsing."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the source Excel file (.xlsx)",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    summary = read_excel_summary(input_path)

    print(summary.model_dump_json(indent=2, exclude_none=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
