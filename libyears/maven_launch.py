"""The finite Feature 007 retained-launch grammar; values are never evaluated."""

import re

from .maven_input import relative_parts
from .maven_model import MavenReason
from .maven_policy import PolicyFailure

_INERT = frozenset({
    '-B', '--batch-mode', '-V', '--show-version', '-q', '--quiet', '-X', '--debug',
    '-e', '--errors', '-ntp', '--no-transfer-progress', '-U', '--update-snapshots',
})
_RELEVANT = frozenset({
    'maven.repo.central', 'maven.settings', 'maven.user.settings',
    'maven.global.settings', 'maven.ext.class.path',
    'maven.multiModuleProjectDirectory', 'user.home', 'maven.home',
})
_FILTER_PREFIXES = ('aether.remoteRepositoryFilter.', 'maven.resolver.remoteRepositoryFilter.')
_KEY = re.compile(r'[A-Za-z][A-Za-z0-9_.-]{0,127}', re.ASCII)
_GOAL = re.compile(r'[A-Za-z0-9_.:-]+', re.ASCII)
_PROFILE = re.compile(r'[+!-]?[A-Za-z0-9_.-]+', re.ASCII)
_MEMORY = re.compile(r'(?:-Xm[sx]|-XX:(?:MaxMetaspaceSize|MetaspaceSize|'
                     r'ReservedCodeCacheSize|MaxDirectMemorySize)=)[0-9]+[kKmMgG]?', re.ASCII)


def relevant_property(key):
    return key in _RELEVANT or key.startswith(_FILTER_PREFIXES)


def _property(argument):
    key = argument[2:].split('=', 1)[0]
    if not _KEY.fullmatch(key) or relevant_property(key):
        raise PolicyFailure()
    # Deliberately do not extract, interpolate, log or follow the value.


def _text(data):
    if type(data) is not bytes or len(data) > 64 * 1024:
        raise PolicyFailure(MavenReason.POLICY_BUDGET_EXCEEDED)
    try:
        text = data.decode('utf-8-sig')
    except UnicodeError:
        raise PolicyFailure() from None
    if any(ord(c) < 32 and c not in '\t\r\n' for c in text):
        raise PolicyFailure()
    if len(text.splitlines()) > 1024:
        raise PolicyFailure(MavenReason.POLICY_BUDGET_EXCEEDED)
    return text


def _argument(argument):
    if len(argument) > 2048:
        raise PolicyFailure(MavenReason.POLICY_BUDGET_EXCEEDED)
    if any(c in argument for c in ('"', "'", '`', '\\')):
        raise PolicyFailure()


def launch_arguments(data, *, allow_settings):
    arguments = [line.strip() for line in _text(data).splitlines()
                 if line.strip() and not line.strip().startswith('#')]
    for argument in arguments:
        _argument(argument)
    selected = None
    index = 0
    while index < len(arguments):
        argument = arguments[index]
        index += 1
        if argument in ('-s', '--settings') or argument.startswith('--settings='):
            if not allow_settings or selected is not None:
                raise PolicyFailure()
            if argument.startswith('--settings='):
                path = argument[len('--settings='):]
            else:
                if index == len(arguments):
                    raise PolicyFailure()
                path = arguments[index]
                index += 1
            relative_parts(path)
            selected = path
        elif argument in ('-P', '--activate-profiles'):
            if index == len(arguments):
                raise PolicyFailure()
            profiles = arguments[index].split(',')
            index += 1
            if len(profiles) > 128 or not all(_PROFILE.fullmatch(p) for p in profiles):
                raise PolicyFailure()
        elif argument in ('-o', '--offline'):
            raise PolicyFailure(MavenReason.COMPARATOR_REFUSED)
        elif argument in _INERT:
            continue
        elif argument.startswith('-D'):
            _property(argument)
        elif argument.startswith('-') or not _GOAL.fullmatch(argument):
            raise PolicyFailure()
    return selected


def jvm_arguments(data):
    arguments = _text(data).split()
    if len(arguments) > 1024:
        raise PolicyFailure(MavenReason.POLICY_BUDGET_EXCEEDED)
    for argument in arguments:
        _argument(argument)
        if argument.startswith('-D'):
            _property(argument)
        elif not _MEMORY.fullmatch(argument):
            raise PolicyFailure()
