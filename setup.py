"""Setup script for the ChainDB Python client."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chain-db",
    version="1.0.0",
    author="Wenderson Pires",
    author_email="wendersonpdas@gmail.com",
    description="A Python client for ChainDB, a secure database system with built-in history tracking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wpdas/chain-db-py",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "websockets>=10.0",
    ],
)
