# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup

HERE = os.path.dirname(os.path.realpath(__file__))


def read(*parts):
    with open(os.path.join(HERE, *parts)) as f:
        return f.read()


def version():
    return re.findall(r"__version__ = \"([\d.]+)\"",
                      read("sppt", "__init__.py"))[0]


setup(
    name="sppt",
    version=version(),
    description="Simple Python Project Template creator",
    author="Julien Pagès",
    author_email="j.parkouss@gmail.com",
    license="GPL",
    install_requires=["jinja2", "colorama", "configobj"],
    tests_require=[],
    entry_points="""
      [console_scripts]
      sppt = sppt.main:main
    """,
)
