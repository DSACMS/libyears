"""Command-line orchestration for Libyears."""

from __future__ import annotations

import argparse
import ssl
import sys
from collections.abc import Sequence
from pathlib import Path

from .output import format_human, format_json
from .scan import NuGetRequest, RubyGroupRequestError, scan_mixed_repository, validate_ruby_groups
from .nuget_sources import NuGetRepositoryRequestError, validate_witnesses
from .snapshot import parse_snapshot


class _ArgumentParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        arguments = list(sys.argv[1:] if args is None else args)
        self.safe_nuget_errors = _nuget_arguments_present(arguments)
        return super().parse_args(arguments, namespace)

    def _get_option_tuples(self, option_string):
        # Exact options bypass this abbreviation hook. Keep ordinary option
        # abbreviations compatible while requiring exact scoped spellings.
        matches = super()._get_option_tuples(option_string)
        if any(match[1] in ("--ruby-group", "--nuget-project", "--nuget-provenance", "--nuget-witness")
               for match in matches):
            return []
        return matches

    def error(self, message: str) -> None:
        if getattr(self, 'safe_nuget_errors', False):
            message = 'invalid NuGet command line arguments'
        self.print_usage(sys.stderr)
        self.exit(1, f"{self.prog}: error: {message}\n")


def build_parser() -> argparse.ArgumentParser:
    parser = _ArgumentParser(prog="libyears", description="Calculate dependency freshness.")
    parser.add_argument("path", nargs="?", default=".", help="repository path (default: .)")
    parser.add_argument("--json", action="store_true", dest="json_output", help="emit JSON")
    parser.add_argument("--ruby-group", metavar="GROUP", action="append",
                        help="select one exact declared Ruby group (repeatable; directory scans only)")
    parser.add_argument("--nuget-project", metavar="NAME.csproj", action="append",
                        help="select one immediate C# project (directory scans only)")
    parser.add_argument("--nuget-provenance", metavar="NAME.json", action="append",
                        help="accept an immediate v1 producer-event or v2 bound snapshot/namespace witness, or v3 fallback population witness; "
                             "stronger event/content assurance is reported separately")
    parser.add_argument("--nuget-witness", metavar="PROJECT=NAME.json", action="append",
                        help="accept one explicit supplier witness per root-relative project in ordinary "
                             "repository mode (repeatable; exactly one =; v1 event, v2 namespace or v3 fallback population assertions)")
    parser.add_argument("--resolved", metavar="FILE", help="exact dependency snapshot")
    parser.add_argument("--ca-bundle", metavar="FILE", help="explicit verified HTTPS CA bundle; see ecosystem trust rules")
    parser.add_argument("--verbose", action="store_true", help="show discovery, evidence, limitations and diagnostics")
    return parser


def _nuget_arguments_present(arguments) -> bool:
    options = ('nuget-project', 'nuget-provenance', 'nuget-witness')
    for argument in arguments:
        # Fold malformed spellings only for privacy; argparse still accepts
        # exclusively the exact lowercase option names registered above.
        option = argument.split('=', 1)[0].lstrip('-').lower()
        if argument.startswith('-') and option and (
                option.startswith('nuget') or any(name.startswith(option) for name in options)):
            return True
    return False


def _nuget_filename(value: str, suffix: str) -> bool:
    return (bool(value) and value.endswith(suffix) and value.isprintable()
            and not any(character in value for character in '/\\:*?[]{};,')
            and not Path(value).is_absolute())


def _nuget_request(args, parser) -> NuGetRequest | None:
    if args.nuget_project is None and args.nuget_provenance is None:
        return None
    if (args.nuget_project is None or len(args.nuget_project) != 1
            or (args.nuget_provenance is not None and len(args.nuget_provenance) != 1)
            or not _nuget_filename(args.nuget_project[0], '.csproj')
            or (args.nuget_provenance is not None
                and (not _nuget_filename(args.nuget_provenance[0], '.json')
                     or args.nuget_provenance[0] == 'packages.lock.json'))):
        parser.error('invalid NuGet selection')
    try:
        directory = Path(args.path).is_dir()
    except (OSError, ValueError):
        parser.error('invalid NuGet selection')
    if not directory:
        parser.error('invalid NuGet selection')
    provenance = args.nuget_provenance[0] if args.nuget_provenance is not None else None
    return NuGetRequest(args.nuget_project[0], provenance)


def main(argv: Sequence[str] | None = None, *, scan=None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        nuget_request = _nuget_request(args, parser)
        witnesses = ()
        if args.nuget_witness is not None:
            if nuget_request is not None or not Path(args.path).is_dir():
                parser.error('invalid NuGet witness mapping')
            if any(value.count('=') != 1 for value in args.nuget_witness):
                parser.error('invalid NuGet witness mapping')
            witnesses = tuple(tuple(value.split('=')) for value in args.nuget_witness)
            try:
                validate_witnesses(witnesses)
            except NuGetRepositoryRequestError:
                parser.error('invalid NuGet witness mapping')
    except SystemExit as error:
        return int(error.code)
    except (OSError, ValueError):
        print('libyears: invalid NuGet request', file=sys.stderr)
        return 1
    scan_function = scan or scan_mixed_repository
    try:
        kwargs = {}
        if nuget_request is not None:
            kwargs['nuget_request'] = nuget_request
        elif Path(args.path).is_dir():
            kwargs['nuget_repository'] = True
            if witnesses:
                kwargs['nuget_witnesses'] = witnesses
        if args.ruby_group is not None:
            kwargs["ruby_groups"] = validate_ruby_groups(args.path, args.ruby_group)
        if args.ca_bundle:
            # Validate the supplied file even when this repository has no registry lookups.
            ssl.create_default_context(cafile=args.ca_bundle)
            kwargs["ca_bundle"] = args.ca_bundle
        if args.resolved is not None:
            kwargs["snapshot"] = parse_snapshot(args.resolved)
        report = scan_function(args.path, **kwargs)
    except (RubyGroupRequestError, NuGetRepositoryRequestError) as error:
        message = 'invalid scoped request' if nuget_request is not None or kwargs.get('nuget_repository') else str(error)
        print(f"libyears: {message}", file=sys.stderr)
        return 1
    except OSError as error:
        message = 'input unavailable' if nuget_request is not None or kwargs.get('nuget_repository') else str(error)
        print(f"libyears: {message}", file=sys.stderr)
        return 1
    except Exception as error:
        message = 'NuGet scan unavailable' if nuget_request is not None or kwargs.get('nuget_repository') else str(error)
        print(f"libyears: systemic scan failure: {message}", file=sys.stderr)
        return 2

    try:
        if args.json_output:
            rendered = format_json(report, args.path)
        else:
            rendered = format_human(report, args.path, verbose=args.verbose)
    except Exception:
        if nuget_request is None and not kwargs.get('nuget_repository'):
            raise
        print('libyears: systemic scan failure: NuGet report unavailable', file=sys.stderr)
        return 2
    print(rendered, end="")
    return 0


__all__ = ["build_parser", "main"]
