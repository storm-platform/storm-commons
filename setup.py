# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-commons is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Common utilities, schemas and other stuffs for the Storm web-services."""

import os

from setuptools import find_packages, setup

readme = open("README.rst").read()
history = open("CHANGES.rst").read()

tests_require = [
    "pytest-invenio>=1.4.0",
]

invenio_db_version = ">=1.0.9,<2.0.0"
invenio_search_version = ">=1.4.2,<2.0.0"

extras_require = {
    "docs": [
        "Sphinx>=3,<4",
    ],
    "tests": tests_require,
    # Elasticsearch
    "elasticsearch7": [
        f"invenio-search[elasticsearch7]{invenio_search_version}",
    ],
    # Databases
    "mysql": [
        f"invenio-db[mysql,versioning]{invenio_db_version}",
    ],
    "postgresql": [
        f"invenio-db[postgresql,versioning]{invenio_db_version}",
    ],
    "sqlite": [
        f"invenio-db[versioning]{invenio_db_version}",
    ],
}

extras_require["all"] = [req for _, reqs in extras_require.items() for req in reqs]


setup_requires = []

install_requires = [
    "pydash>=5.1.0,<6.0",
    "jinja2>=3.0.3,<4.0.0",
    "invenio-drafts-resources>=0.14.0,<0.15.0",
    "invenio-records-resources>=0.17.0,<0.18",
]

packages = find_packages()

# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join("storm_commons", "version.py"), "rt") as fp:
    exec(fp.read(), g)
    version = g["__version__"]

setup(
    name="storm-commons",
    version=version,
    description=__doc__,
    long_description=readme + "\n\n" + history,
    keywords=["Storm Platform", "Common utilities"],
    license="MIT",
    author="Felipe Menino Carlos",
    author_email="felipe.carlos@inpe.br",
    url="https://github.com/storm-platform/storm-commons",
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms="any",
    entry_points={},
    extras_require=extras_require,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 1 - Planning",
    ],
)
