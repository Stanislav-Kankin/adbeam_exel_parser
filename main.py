from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from adbeam_excel_parser.audit_runner import attach_output_file_path, run_excel_audit
from adbeam_excel_parser.excel_exporter import export_audit_to_excel
from adbeam_excel_parser.excel_reader import read_excel_summary
from adbeam_excel_parser.gui_app import run_gui


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read an Excel file and run a basic site-audit pass."
    )
    parser.add_argument(
        "--input",
        help="Path to the source Excel file (.xlsx)",
    )
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Run site fetching, rule-based classification and save a new Excel file.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.input:
        run_gui()
        return 0

    input_path = Path(args.input).expanduser().resolve()

    if args.audit:
        audit_summary = run_excel_audit(input_path)
        output_file_path = export_audit_to_excel(input_path, audit_summary)
        attach_output_file_path(audit_summary, output_file_path)
        print(audit_summary.model_dump_json(indent=2, exclude_none=True))
        return 0

    summary = read_excel_summary(input_path)
    print(summary.model_dump_json(indent=2, exclude_none=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
