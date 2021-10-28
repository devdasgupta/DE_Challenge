#!/usr/bin/env python

"""
Setup manual_abstraction_service.

Note: Read RELEASE.md for notes on the release process
"""

from pathlib import Path
from shutil import which

from setuptools import setup

# Only use the SCM version if we have a functional git environment.
use_scm_version = Path('.git').exists() and which('git')

if use_scm_version:
    setup(use_scm_version=True)
else:
    setup()
