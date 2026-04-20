# test_app.py

import pytest
from app import get_strategy


def test_crash_strategy():
    assert get_strategy(2, "Normal") == "Crash Preparation"


def test_revision_strategy():
    assert get_strategy(5, "Normal") == "Focused Revision"


def test_balanced_strategy():
    assert get_strategy(15, "Normal") == "Balanced Study Plan"


def test_last_minute_override():
    assert get_strategy(10, "Last-Minute") == "Emergency Strategy (focus only on high-priority topics and revision)"


def test_invalid_input():
    # Edge case
    result = get_strategy(0, "Normal")
    assert result in ["Crash Preparation", "Emergency Strategy (focus only on high-priority topics and revision)"]