"""
Command-line interface for document parser MCP server.
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

from document_parser.config.settings import load_settings
from document_parser.mcp.server import DocumentParserServer
from document_parser.utils.file_utils import ensure_directory
from document_parser.utils.logging_utils import setup_logging


async def run_server(config_path: str, debug: bool = False) -> None:
    """
    Run the MCP server.

    Args:
        config_path: Path to configuration file
        debug: Enable debug logging
    """
    # Load configuration
    try:
        settings = load_settings(config_path)
    except Exception as e:
        print(f"Error loading configuration: {e}", file=sys.stderr)
        sys.exit(1)

    # Override log level if debug enabled
    if debug:
        settings.logging.level = "DEBUG"

    # Setup logging
    setup_logging(settings.logging)

    # Ensure directories exist
    ensure_directory(settings.storage.temp_directory)
    ensure_directory(Path(settings.logging.file_path).parent)

    logger = logging.getLogger(__name__)
    logger.info(f"Starting {settings.server.name} v{settings.server.version}")

    # Create and run server
    server = DocumentParserServer(settings)

    try:
        await server.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Document Parser MCP Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start with default config
  document-parser-mcp

  # Start with custom config
  document-parser-mcp --config /path/to/config.yaml

  # Start with debug logging
  document-parser-mcp --debug
        """,
    )

    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to configuration file (default: config.yaml)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    parser.add_argument(
        "--version",
        action="version",
        version="document-parser-mcp 1.0.0",
    )

    args = parser.parse_args()

    # Run server
    asyncio.run(run_server(args.config, args.debug))


if __name__ == "__main__":
    main()
