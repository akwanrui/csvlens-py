"""Tests for csvlens.csv_loader module."""

import csv
import textwrap
from pathlib import Path

import pytest

from csvlens.csv_loader import CSVLoadError, CSVLoader


@pytest.fixture()
def sample_csv(tmp_path: Path) -> Path:
    """Create a small sample CSV file for testing."""
    data = textwrap.dedent("""\
        name,age,city
        Alice,30,New York
        Bob,25,Los Angeles
        Charlie,35,Chicago
    """)
    filepath = tmp_path / "sample.csv"
    filepath.write_text(data, encoding="utf-8")
    return filepath


def test_loads_headers(sample_csv: Path) -> None:
    loader = CSVLoader(sample_csv)
    assert loader.headers == ["name", "age", "city"]


def test_loads_correct_row_count(sample_csv: Path) -> None:
    loader = CSVLoader(sample_csv)
    assert loader.num_rows == 3


def test_loads_correct_column_count(sample_csv: Path) -> None:
    loader = CSVLoader(sample_csv)
    assert loader.num_columns == 3


def test_row_values(sample_csv: Path) -> None:
    loader = CSVLoader(sample_csv)
    assert loader.rows[0] == {"name": "Alice", "age": "30", "city": "New York"}


def test_iter_column(sample_csv: Path) -> None:
    loader = CSVLoader(sample_csv)
    ages = list(loader.iter_column("age"))
    assert ages == ["30", "25", "35"]


def test_iter_column_unknown_raises(sample_csv: Path) -> None:
    loader = CSVLoader(sample_csv)
    with pytest.raises(KeyError, match="salary"):
        list(loader.iter_column("salary"))


def test_file_not_found_raises(tmp_path: Path) -> None:
    with pytest.raises(CSVLoadError, match="File not found"):
        CSVLoader(tmp_path / "nonexistent.csv")


def test_empty_file_raises(tmp_path: Path) -> None:
    empty = tmp_path / "empty.csv"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(CSVLoadError, match="empty or has no header row"):
        CSVLoader(empty)


def test_custom_delimiter(tmp_path: Path) -> None:
    tsv = tmp_path / "data.tsv"
    tsv.write_text("col1\tcol2\nfoo\tbar\n", encoding="utf-8")
    loader = CSVLoader(tsv, delimiter="\t")
    assert loader.headers == ["col1", "col2"]
    assert loader.rows[0] == {"col1": "foo", "col2": "bar"}
