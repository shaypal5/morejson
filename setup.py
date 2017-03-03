"""Setup for the morejson package."""

#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import versioneer

with open('README.rst') as f:
    README = f.read()

setup(
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    long_description=README,
    packages=find_packages(),
    install_requires=[],
    test_suite='nose.collector',
    tests_require=['nose'],
)
