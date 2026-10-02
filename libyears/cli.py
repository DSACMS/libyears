"""Command-line orchestration for Libyears."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from .output import format_human, format_json
from .scan import scan_repository


class _ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(1, f"{self.prog}: error: {message}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = _ArgumentParser(prog="libyears", description="Calculate dependency freshness.")
    parser.add_argument("path", nargs="?", default=".", help="repository path (default: .)")
    parser.add_argument("--json", action="store_true", dest="json_output", help="emit JSON")
    return parser


def main(argv: Sequence[str] | None = None, *, scan=None) -> int:
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as error:
        return int(error.code)
    scan_function = scan or scan_repository
    try:
        report = scan_function(args.path)
    except OSError as error:
        print(f"libyears: {error}", file=sys.stderr)
        return 1
    except Exception as error:
        print(f"libyears: systemic scan failure: {error}", file=sys.stderr)
        return 2

    rendered = format_json(report, args.path) if args.json_output else format_human(report, args.path)
    print(rendered, end="")
    return 0


__all__ = ["build_parser", "main"]
