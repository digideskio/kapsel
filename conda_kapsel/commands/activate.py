# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright © 2016, Continuum Analytics, Inc. All rights reserved.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# ----------------------------------------------------------------------------
"""The ``activate`` command which prepares a project to run and prints commands to source in your shell."""
from __future__ import absolute_import, print_function

import os

try:
    from shlex import quote  # pragma: no cover (py3 only)
except ImportError:  # pragma: no cover (py2 only)
    from pipes import quote

from conda_kapsel.commands.prepare_with_mode import prepare_with_ui_mode_printing_errors
from conda_kapsel.commands.project_load import load_project


def activate(dirname, ui_mode, conda_environment):
    """Prepare project and return lines to be sourced.

    Future direction: should also activate the proper conda env.

    Returns:
        None on failure or a list of lines to print.
    """
    project = load_project(dirname)
    result = prepare_with_ui_mode_printing_errors(project, ui_mode=ui_mode, env_spec_name=conda_environment)
    if result.failed:
        return None

    exports = []
    # sort so we have deterministic output order for tests
    sorted_keys = list(result.environ.keys())
    sorted_keys.sort()
    for key in sorted_keys:
        value = result.environ[key]
        if key not in os.environ or os.environ[key] != value:
            exports.append("export {key}={value}".format(key=key, value=quote(value)))
    return exports


def main(args):
    """Start the activate command and return exit status code."""
    result = activate(args.directory, args.mode, args.env_spec)
    if result is None:
        return 1
    else:
        for line in result:
            print(line)
        return 0
