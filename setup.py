#!/usr/bin/env python

from setuptools import setup

"""Usage in the terminal: python setup.py py2app"""

__author__ = 'Salman_M_Rahman'


setup(
    app=["sreboard.py"],
    data_files=["cord_attr.json"],
    version="2.1",
    author=["Salman M Rahman(Samie)"],
    author_email=["salman.rahman@service-now.com"],
    description=["Monitoring applications initializer automation for SRE Operations"],
    url=["https://gitlab.service-now.com/salman.rahman/sreboard"],
    setup_requires=["py2app"],
)
