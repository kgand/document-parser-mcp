.PHONY: help install install-dev test lint format clean run

help:
	@echo "Document Parser MCP - Available Commands"
	@echo ""
	@echo "  make install       Install production dependencies"
	@echo "  make install-dev   Install development dependencies"
	@echo "  make test          Run test suite"
	@echo "  make lint          Run linters"
	@echo "  make format        Format code with black and isort"
	@echo "  make clean         Clean build artifacts"
	@echo "  make run           Run the MCP server"
	@echo ""

install:
	pip install -r requirements.txt
	pip install docling

install-dev:
	pip install -r requirements-dev.txt
	pip install -e .

test:
	pytest

test-cov:
	pytest --cov=document_parser --cov-report=html --cov-report=term

lint:
	ruff check document_parser tests
	mypy document_parser

format:
	black document_parser tests
	isort document_parser tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

run:
	python -m document_parser

run-debug:
	python -m document_parser --debug
