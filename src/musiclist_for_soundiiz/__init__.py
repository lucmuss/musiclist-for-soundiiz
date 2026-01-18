"""MusicList for Soundiiz - Extract music file metadata for Soundiiz import."""

__version__ = "1.0.0"
__author__ = "Your Name"
__license__ = "MIT"

from .cli import main
from .extractor import MusicFileExtractor
from .exporter import CSVExporter, JSONExporter, M3UExporter

__all__ = [
    "main",
    "MusicFileExtractor",
    "CSVExporter",
    "JSONExporter",
    "M3UExporter",
]
