"""Tests for ColumnStatsComputer."""

import pytest
from csvlens.column_stats import ColumnStats, ColumnStatsComputer


HEADERS = ["name", "age", "score", "notes"]

ROWS = [
    {"name": "Alice", "age": "30", "score": "95.5", "notes": "good"},
    {"name": "Bob", "age": "25", "score": "80.0", "notes": ""},
    {"name": "Charlie", "age": "35", "score": "88.0", "notes": "average"},
    {"name": "Alice", "age": "", "score": "72.5", "notes": ""},
]


@pytest.fixture
def stats():
    computer = ColumnStatsComputer(HEADERS, ROWS)
    return computer.compute()


def test_all_columns_present(stats):
    assert set(stats.keys()) == set(HEADERS)


def test_count_equals_row_count(stats):
    for col in HEADERS:
        assert stats[col].count == len(ROWS)


def test_null_count_name_column(stats):
    assert stats["name"].null_count == 0


def test_null_count_age_column(stats):
    assert stats["age"].null_count == 1


def test_null_count_notes_column(stats):
    assert stats["notes"].null_count == 2


def test_null_rate(stats):
    assert stats["age"].null_rate == pytest.approx(0.25)


def test_unique_count_name(stats):
    # Alice appears twice
    assert stats["name"].unique_count == 3


def test_numeric_detection_age(stats):
    # age has one null, three numeric — non-null values are all numeric
    assert stats["age"].is_numeric is True


def test_numeric_detection_name(stats):
    assert stats["name"].is_numeric is False


def test_mean_score(stats):
    expected_mean = (95.5 + 80.0 + 88.0 + 72.5) / 4
    assert stats["score"].mean == pytest.approx(expected_mean)


def test_median_score(stats):
    import statistics
    expected_median = statistics.median([95.5, 80.0, 88.0, 72.5])
    assert stats["score"].median == pytest.approx(expected_median)


def test_min_max_numeric(stats):
    assert stats["score"].min_value == pytest.approx(72.5)
    assert stats["score"].max_value == pytest.approx(95.5)


def test_min_max_string(stats):
    # lexicographic comparison for non-numeric columns
    assert stats["name"].min_value == "Alice"
    assert stats["name"].max_value == "Charlie"


def test_non_null_count(stats):
    assert stats["notes"].non_null_count == 2


def test_empty_rows():
    computer = ColumnStatsComputer(["x"], [])
    result = computer.compute()
    assert result["x"].count == 0
    assert result["x"].null_rate == 0.0
    assert result["x"].is_numeric is False
