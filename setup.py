from setuptools import setup, find_packages
from codecs import open
from pathlib import Path

HOME = Path(__file__).parent

with open(HOME / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="type-check",
    version="0.1.8",
    description="Type check decorator for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    keywords="type check safe",
    packages=find_packages(),
)
