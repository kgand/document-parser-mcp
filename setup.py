"""
Setup configuration for document-parser-mcp
"""

from pathlib import Path
from setuptools import setup, find_packages

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, "r", encoding="utf-8") as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#") and not line.startswith("-r")
        ]

setup(
    name="document-parser-mcp",
    version="1.0.0",
    author="Document Parser Team",
    author_email="team@documentparser.dev",
    description="MCP server for intelligent document processing using Docling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/document-parser-mcp",
    packages=find_packages(exclude=["tests*", "docs*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: General",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    extras_require={
        "mlx": ["docling[mlx]"],
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "document-parser-mcp=document_parser.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
