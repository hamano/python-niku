#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name='niku',
    version='2.0.1',
    description="PID Controller for sous vide",
    url="http://www.cuspy.org/diary/raspberrypi-roastbeef/",
    author = "Tsukasa Hamano",
    author_email = "code@cuspy.org",
    entry_points="""
[console_scripts]
niku = niku:main
""",
    py_modules=['niku'],
    license="BSD",
)
