# -*- coding: utf-8 -*-
"""Internationalization support for MusicList for Soundiiz."""

from contextlib import suppress

TRANSLATIONS = {
    "en": {
        "window_title": "MusicList for Soundiiz",
        "subtitle": "Extract music metadata and create playlists",
        "input_directories": "Input Directories",
        "output": "Output",
        "options": "Options",
        "progress": "Progress",
        "add_directory": "Add Directory",
        "remove_selected": "Remove Selected",
        "clear_all": "Clear All",
        "tip_add_directory": "Tip: Click 'Add Directory' or drag folders here",
        "output_file": "Output File:",
        "browse": "Browse",
        "format": "Format:",
        "max_songs": "Max songs per file:",
        "scan_recursive": "Scan subdirectories recursively",
        "detect_duplicates": "Detect duplicates",
        "remove_duplicates": "Remove duplicates",
        "strategy": "Strategy:",
        "process_files": "Process Files",
        "clear_log": "Clear Log",
        "help": "Help",
        "about": "About",
        "ready": "Ready",
        "ready_to_process": "Ready to process music files",
        "processing": "Processing...",
        "completed": "Completed successfully",
        "error_occurred": "Error occurred",
        "info": "Info",
        "warning": "Warning",
        "error": "Error",
        "success": "Success",
        "already_added": "Directory already added",
        "processing_in_progress": "Processing already in progress",
        "no_input_dir": "Please add at least one input directory",
        "no_output_file": "Please specify an output file",
        "no_files_found": "No music files found in selected directories",
        "success_message": "Successfully processed {count} songs. Output: {file}",
        "error_message": "An error occurred: {error}",
        "added": "Added:",
        "removed": "Removed:",
        "cleared": "Cleared all directories",
        "starting_processing": "Starting processing",
        "scanning": "Scanning:",
        "found_files": "Found {count} files",
        "total_found": "Total files found: {count}",
        "processing_file": "Processing file {current}/{total}",
        "estimated_time": "Estimated time remaining: {time}",
        "no_music_files": "No music files found",
        "checking_duplicates": "Checking for duplicates",
        "found_duplicates": "Found {groups} duplicate groups ({total} total files)",
        "removed_duplicates": "Removed {count} duplicates",
        "unique_remaining": "{count} unique songs remaining",
        "no_duplicates": "No duplicates found",
        "exporting_to": "Exporting to {format}",
        "export_completed": "Export completed: {file}",
        "help_title": "MusicList for Soundiiz - Help",
        "help_text": (
            "1. Add Directories: Click 'Add Directory' to select folders.\n"
            "2. Choose Output: Select file name and format (CSV, JSON, M3U, TXT).\n"
            "3. Options: Recursive scan, duplicate detection, max songs.\n"
            "4. Process: Click 'Process Files' to start.\n\n"
            "Supported Formats: AAC, AU, FLAC, MP3, OGG, M4A, WAV, WMA\n\n"
            "More info: https://github.com/lucmuss/musiclist-for-soundiiz"
        ),
        "about_title": "About",
        "about_text": (
            "MusicList for Soundiiz\n"
            "Version 1.0.8\n\n"
            "Tool for extracting music metadata and creating playlists.\n\n"
            "Features:\n"
            "- Multi-format support\n"
            "- Duplicate detection\n"
            "- Batch processing\n"
            "- Multiple export formats\n\n"
            "GitHub: github.com/lucmuss/musiclist-for-soundiiz\n"
            "License: MIT"
        ),
    }
}


class I18n:
    """Simple internationalization class."""

    def __init__(self, language="en"):
        """Initialize with default language."""
        self.set_language(language)

    def set_language(self, language):
        """Set the current language."""
        if language in TRANSLATIONS:
            self.current_lang = language
            self.trans = TRANSLATIONS[language]
        else:
            self.current_lang = "en"
            self.trans = TRANSLATIONS["en"]

    def get(self, key, **kwargs):
        """Get translated string, fall back to English if not found."""
        text = self.trans.get(key)

        if text is None:
            text = TRANSLATIONS["en"].get(key, key)

        if kwargs:
            with suppress(KeyError):
                text = text.format(**kwargs)

        return text

    def __call__(self, key, **kwargs):
        """Shortcut for get()."""
        return self.get(key, **kwargs)
