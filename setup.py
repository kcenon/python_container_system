"""
Setup script for python_container_system

BSD 3-Clause License
Copyright (c) 2021, 🍀☀🌕🌥 🌊
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="python-container-system",
    version="1.0.0",
    author="kcenon",
    author_email="kcenon@naver.com",
    description="A high-performance type-safe container framework for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kcenon/python_container_system",
    packages=find_packages(exclude=["tests", "examples", "docs"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
            "pylint>=2.17.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    package_data={
        "container_module": ["py.typed"],
    },
    zip_safe=False,
    project_urls={
        "Bug Reports": "https://github.com/kcenon/python_container_system/issues",
        "Source": "https://github.com/kcenon/python_container_system",
        "Documentation": "https://github.com/kcenon/python_container_system/blob/main/README.md",
    },
)
