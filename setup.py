# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 John Woolsey for Woolsey Workshop
#
# SPDX-License-Identifier: MIT

"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    # Community Bundle Information
    name="woolseyworkshop-circuitpython-74hc165",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="CircuitPython driver for 74HC165 shift register.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # The project's main homepage.
    url="https://github.com/WoolseyWorkshop/WoolseyWorkshop_CircuitPython_74HC165.git",
    # Author details
    author="John Woolsey",
    author_email="",
    install_requires=[
        "Adafruit-Blinka",
        "adafruit-circuitpython-busdevice",
    ],
    # Choose your license
    license="MIT",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    ],
    # What does your project relate to?
    keywords="adafruit blinka circuitpython micropython 74hc165 shift register",
    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    py_modules=["wws_74hc165"],
)
