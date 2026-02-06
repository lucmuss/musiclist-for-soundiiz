# -*- coding: utf-8 -*-
"""Tests for i18n helper."""

from musiclist_for_soundiiz.i18n import I18n


def test_i18n_default_language():
    """Default language should be English."""
    i18n = I18n()
    assert i18n.get("window_title") == "MusicList for Soundiiz"


def test_i18n_formatting():
    """Formatted strings should interpolate values."""
    i18n = I18n()
    text = i18n.get("success_message", count=3, file="output.csv")
    assert "3" in text
    assert "output.csv" in text


def test_i18n_missing_key_returns_key():
    """Missing keys should return the key name."""
    i18n = I18n()
    assert i18n.get("missing_key") == "missing_key"
