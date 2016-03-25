# -*- coding: utf-8 -*-

import os
import re
from setuptools import setup

HERE = os.path.dirname(os.path.realpath(__file__))


def read(*parts):
    with open(os.path.join(HERE, *parts)) as f:
        return f.read()


def version():
    return re.findall(r"__version__ = ['\"]([\d.]+)[\"']",
                      read({{project_name|repr}}, "__init__.py"))[0]


setup(
    name={{project_name|repr}},
    version=version(),
    description={{project_description|repr}},
    author={{author|repr}},
    author_email={{author_email|repr}},
    license={{license|repr}},
    install_requires=[],
    tests_require=[],
{% if executable %}
    entry_points="""
      [console_scripts]
      {{executable_name}} = {{executable_entry_point}}
    """,
{% endif %}
)

