"""Command-line orchestration for Libyears."""

from __future__ import annotations

import argparse
import ssl
import sys
from collections.abc import Sequence

from .output import format_human, format_json
from .scan import RubyGroupRequestError, scan_mixed_repository, validate_ruby_groups
from .snapshot import parse_snapshot


class _ArgumentParser(argparse.ArgumentParser):
    def _get_option_tuples(self, option_string):
        # Exact options bypass this abbreviation hook. Keep ordinary option
        # abbreviations compatible while requiring the sole scoped spelling.
        matches = super()._get_option_tuples(option_string)
        if any(match[1] == "--ruby-group" for match in matches):
            return []
        return matches

    def error(self, message: str) -> None:
        self.print_usage(sys.stderr)
        self.exit(1, f"{self.prog}: error: {message}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = _ArgumentParser(prog="libyears", description="Calculate dependency freshness.")
    parser.add_argument("path", nargs="?", default=".", help="repository path (default: .)")
    parser.add_argument("--json", action="store_true", dest="json_output", help="emit JSON")
    parser.add_argument("--ruby-group", metavar="GROUP", action="append",
                        help="select one exact declared Ruby group (repeatable; directory scans only)")
    parser.add_argument("--resolved", metavar="FILE", help="exact dependency snapshot")
    parser.add_argument("--ca-bundle", metavar="FILE", help="verified CA bundle for PyPI HTTPS")
    parser.add_argument("--verbose", action="store_true", help="show concise registry failure diagnostics")
    return parser


def main(argv: Sequence[str] | None = None, *, scan=None) -> int:
    try:
        args = build_parser().parse_args(argv)
    except SystemExit as error:
        return int(error.code)
    scan_function = scan or scan_mixed_repository
    try:
        kwargs = {}
        if args.ruby_group is not None:
            kwargs["ruby_groups"] = validate_ruby_groups(args.path, args.ruby_group)
        if args.ca_bundle:
            # Validate the supplied file even when this repository has no registry lookups.
            ssl.create_default_context(cafile=args.ca_bundle)
            kwargs["ca_bundle"] = args.ca_bundle
        if args.resolved is not None:
            kwargs["snapshot"] = parse_snapshot(args.resolved)
        report = scan_function(args.path, **kwargs)
    except RubyGroupRequestError as error:
        print(f"libyears: {error}", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"libyears: {error}", file=sys.stderr)
        return 1
    except Exception as error:
        print(f"libyears: systemic scan failure: {error}", file=sys.stderr)
        return 2

    rendered = format_json(report, args.path) if args.json_output else format_human(report, args.path, verbose=args.verbose)
    print(rendered, end="")
    return 0


__all__ = ["build_parser", "main"]
