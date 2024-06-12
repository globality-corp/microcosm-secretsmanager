#!/usr/bin/env python
from setuptools import find_packages, setup

project = "microcosm-secretsmanager"
version = "2.0.0"

setup(
    name=project,
    version=version,
    description="Secrets storage using AWS SecretsManager",
    author="Globality Engineering",
    author_email="engineering@globality.com",
    url="https://github.com/globality-corp/microcosm-secretsmanager",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.11",
    install_requires=[
        "microcosm>=4.0.0",
        "boto3>=1.7.9",
    ],
    extras_require={
        "test": [
            "coverage>=3.7.1",
            "PyHamcrest>=1.8.5",
            "pytest-cov>=5.0.0",
            "pytest>=6.2.5",
        ],
        "lint": [
            "flake8",
            "flake8-print",
            "flake8-isort",
            "PyHamcrest>=1.8.5",
        ],
        "typehinting": [
            "mypy",
            "types-boto3",
            "types-python-dateutil",
            "PyHamcrest>=1.8.5",
        ],
    },
    setup_requires=[
    ],
    dependency_links=[
    ],
    entry_points={
    },
    tests_require=[
        "coverage>=3.7.1",
        "PyHamcrest>=1.8.5",
        "pytest-cov>=5.0.0",
    ],
)
