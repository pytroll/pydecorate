#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2013, 2016 Adam Dybbroe

# Author(s):

#   Hrobjartur Thorsteinsson <thorsteinssonh@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from setuptools import setup

try:
    # HACK: https://github.com/pypa/setuptools_scm/issues/190#issuecomment-351181286
    # Stop setuptools_scm from including all repository files
    import setuptools_scm.integration
    setuptools_scm.integration.find_files = lambda _: []
except ImportError:
    pass

with open("./README.rst", "r") as fd:
    long_description = fd.read()


setup(name='pydecorate',
      description='Decorating PIL images: logos, texts, pallettes',
      long_description=long_description,
      author='Hrobjartur Thorsteinsson',
      author_email='thorsteinssonh@gmail.com',
      classifiers=["Development Status :: 4 - Beta",
                   "Intended Audience :: Science/Research",
                   "License :: OSI Approved :: GNU General Public License v3 " +
                   "or later (GPLv3+)",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Scientific/Engineering"],
      url="https://github.com/pytroll/pydecorate",
      license='GPLv3',
      packages=['pydecorate'],
      include_package_data=True,
      package_data={'pydecorate': ['fonts/*.ttf']},
      # Project should use reStructuredText, so ensure that the docutils get
      # installed or upgraded on the target machine
      install_requires=['pillow', 'aggdraw'],
      setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
      scripts=[],
      data_files=[],
      # test_suite="",
      tests_require=['pytest'],
      python_requires='>=3.6',
      use_scm_version={'write_to': 'pydecorate/version.py'},
      zip_safe=False)
