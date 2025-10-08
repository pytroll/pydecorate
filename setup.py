"""Package building definition and script."""

import sys

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

tests_require = ["pytest", "pytest-cov", "trollimage"]
if sys.platform.startswith("win"):
    tests_require.append("freetype-py")

setup(
    name="pydecorate",
    description="Decorating PIL images: logos, texts, pallettes",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author="Hrobjartur Thorsteinsson",
    author_email="thorsteinssonh@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
    ],
    url="https://github.com/pytroll/pydecorate",
    license="Apache-2.0",
    license_files=["LICENSE.txt"],
    packages=["pydecorate"],
    include_package_data=True,
    package_data={"pydecorate": ["fonts/*.ttf"]},
    install_requires=["pillow", "aggdraw", "numpy"],
    setup_requires=["setuptools_scm", "setuptools_scm_git_archive"],
    scripts=[],
    data_files=[],
    python_requires=">=3.9",
    extras_require={
        "tests": tests_require,
        "docs": [
            "sphinx",
            "sphinx_rtd_theme",
            "sphinxcontrib-apidoc",
            "trollimage",
            "pytest",
        ],
    },
    zip_safe=False,
)
