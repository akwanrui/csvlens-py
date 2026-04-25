"""CSV loading and parsing module for csvlens-py."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Generator


class CSVLoadError(Exception):
    """Raised when a CSV file cannot be loaded or parsed."""


class CSVLoader:
    """Loads and holds CSV data with headers and rows."""

    def __init__(self, filepath: str | Path, delimiter: str = ",") -> None:
        self.filepath = Path(filepath)
        self.delimiter = delimiter
        self.headers: list[str] = []
        self.rows: list[dict[str, str]] = []
        self._load()

    def _load(self) -> None:
        """Read the CSV file and populate headers and rows."""
        if not self.filepath.exists():
            raise CSVLoadError(f"File not found: {self.filepath}")
        if not self.filepath.is_file():
            raise CSVLoadError(f"Path is not a file: {self.filepath}")

        try:
            with self.filepath.open(newline="", encoding="utf-8") as fh:
                reader = csv.DictReader(fh, delimiter=self.delimiter)
                if reader.fieldnames is None:
                    raise CSVLoadError("CSV file appears to be empty or has no header row.")
                self.headers = list(reader.fieldnames)
                self.rows = [dict(row) for row in reader]
        except csv.Error as exc:
            raise CSVLoadError(f"Failed to parse CSV: {exc}") from exc

    @property
    def num_rows(self) -> int:
        return len(self.rows)

    @property
    def num_columns(self) -> int:
        return len(self.headers)

    def iter_column(self, column: str) -> Generator[str, None, None]:
        """Yield all values for a given column name."""
        if column not in self.headers:
            raise KeyError(f"Column '{column}' not found in headers.")
        for row in self.rows:
            yield row.get(column, "")

    def __repr__(self) -> str:  # pragma: no cover
        return (
            f"CSVLoader(filepath={self.filepath!r}, "
            f"rows={self.num_rows}, columns={self.num_columns})"
        )
