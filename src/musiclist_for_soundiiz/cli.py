"""Command-line interface for MusicList for Soundiiz."""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

from . import __version__
from .extractor import MusicFileExtractor
from .exporter import get_exporter

logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """
    Configure logging.

    Args:
        verbose: Enable verbose (DEBUG) logging
    """
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def parse_args(args: Optional[list] = None) -> argparse.Namespace:
    """
    Parse command-line arguments.

    Args:
        args: Arguments to parse (defaults to sys.argv)

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="Extract music file metadata for Soundiiz import",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract metadata from directory to CSV (default)
  musiclist-for-soundiiz -i /path/to/music -o output.csv

  # Export to JSON format
  musiclist-for-soundiiz -i /path/to/music -o output.json -f json

  # Only scan MP3 and FLAC files
  musiclist-for-soundiiz -i /path/to/music -e .mp3 .flac

  # Non-recursive scan (current directory only)
  musiclist-for-soundiiz -i /path/to/music --no-recursive

  # Export to multiple formats
  musiclist-for-soundiiz -i /path/to/music -o output.csv -f csv
  musiclist-for-soundiiz -i /path/to/music -o output.json -f json

Supported audio formats:
  AAC (.aac), AU (.au), FLAC (.flac), MP3 (.mp3), OGG (.ogg),
  M4A (.m4a), WAV (.wav), WMA (.wma)
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    # Input/Output arguments
    io_group = parser.add_argument_group("Input/Output")
    io_group.add_argument(
        "-i",
        "--input",
        required=True,
        help="Path to music directory to scan",
    )
    io_group.add_argument(
        "-o",
        "--output",
        default="output.csv",
        help="Output file path (default: output.csv)",
    )
    io_group.add_argument(
        "-f",
        "--format",
        choices=["csv", "json", "m3u", "txt"],
        default="csv",
        help="Output format (default: csv)",
    )

    # Scan options
    scan_group = parser.add_argument_group("Scan Options")
    scan_group.add_argument(
        "-e",
        "--extensions",
        nargs="+",
        help="File extensions to include (e.g., .mp3 .flac). Default: all supported formats",
    )
    scan_group.add_argument(
        "--no-recursive",
        action="store_true",
        help="Don't scan subdirectories recursively",
    )

    # Export options
    export_group = parser.add_argument_group("Export Options")
    export_group.add_argument(
        "--max-songs-per-file",
        type=int,
        default=500,
        help="Maximum songs per CSV file (default: 500)",
    )
    export_group.add_argument(
        "--no-pretty-json",
        action="store_true",
        help="Disable pretty-printing for JSON output",
    )

    # Logging options
    log_group = parser.add_argument_group("Logging")
    log_group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose (DEBUG) logging",
    )
    log_group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress all output except errors",
    )

    parsed_args = parser.parse_args(args)

    # Validate arguments
    if parsed_args.quiet and parsed_args.verbose:
        parser.error("Cannot use --quiet and --verbose together")

    return parsed_args


def main(argv: Optional[list] = None) -> int:
    """
    Main entry point for the CLI.

    Args:
        argv: Command-line arguments (defaults to sys.argv)

    Returns:
        Exit code (0 for success, non-zero for failure)
    """
    args = parse_args(argv)

    # Setup logging
    if args.quiet:
        logging.basicConfig(level=logging.ERROR)
    else:
        setup_logging(args.verbose)

    logger.info(f"MusicList for Soundiiz v{__version__}")
    logger.info(f"Scanning directory: {args.input}")

    try:
        # Validate input directory
        input_path = Path(args.input)
        if not input_path.exists():
            logger.error(f"Input directory does not exist: {args.input}")
            return 1

        if not input_path.is_dir():
            logger.error(f"Input path is not a directory: {args.input}")
            return 1

        # Initialize extractor
        extractor = MusicFileExtractor(include_extensions=args.extensions)

        # Extract metadata
        logger.info(
            f"Extracting metadata (recursive: {not args.no_recursive})..."
        )
        metadata_list = extractor.extract_all(
            directory=str(input_path),
            recursive=not args.no_recursive,
        )

        if not metadata_list:
            logger.warning("No music files found!")
            return 0

        logger.info(f"Successfully extracted metadata from {len(metadata_list)} files")

        # Initialize exporter
        exporter_kwargs = {}
        if args.format == "csv":
            exporter_kwargs["max_songs_per_file"] = args.max_songs_per_file
        elif args.format == "json":
            exporter_kwargs["pretty"] = not args.no_pretty_json

        exporter = get_exporter(args.format, **exporter_kwargs)

        # Export metadata
        logger.info(f"Exporting to {args.format.upper()} format: {args.output}")
        exporter.export(metadata_list, args.output)

        logger.info("✓ Export completed successfully!")
        return 0

    except KeyboardInterrupt:
        logger.error("\nOperation cancelled by user")
        return 130

    except Exception as e:
        logger.error(f"Error: {e}", exc_info=args.verbose)
        return 1


if __name__ == "__main__":
    sys.exit(main())
