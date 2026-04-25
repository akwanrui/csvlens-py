"""Column statistics computation for CSV data."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import statistics


@dataclass
class ColumnStats:
    """Statistics for a single CSV column."""

    name: str
    count: int = 0
    null_count: int = 0
    unique_count: int = 0
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    mean: Optional[float] = None
    median: Optional[float] = None
    is_numeric: bool = False

    @property
    def non_null_count(self) -> int:
        return self.count - self.null_count

    @property
    def null_rate(self) -> float:
        if self.count == 0:
            return 0.0
        return self.null_count / self.count


class ColumnStatsError(Exception):
    """Raised when column statistics cannot be computed."""


class ColumnStatsComputer:
    """Computes statistics for each column in a CSV dataset."""

    def __init__(self, headers: List[str], rows: List[Dict[str, str]]) -> None:
        self._headers = headers
        self._rows = rows

    def compute(self) -> Dict[str, ColumnStats]:
        """Compute statistics for all columns."""
        stats: Dict[str, ColumnStats] = {}
        for col in self._headers:
            stats[col] = self._compute_column(col)
        return stats

    def _compute_column(self, col: str) -> ColumnStats:
        raw_values = [row.get(col, "") for row in self._rows]
        count = len(raw_values)
        null_count = sum(1 for v in raw_values if v.strip() == "")
        non_null = [v for v in raw_values if v.strip() != ""]
        unique_count = len(set(non_null))

        numeric_values: List[float] = []
        for v in non_null:
            try:
                numeric_values.append(float(v))
            except ValueError:
                pass

        is_numeric = len(numeric_values) == len(non_null) and len(non_null) > 0

        min_value: Optional[Any] = None
        max_value: Optional[Any] = None
        mean: Optional[float] = None
        median: Optional[float] = None

        if is_numeric and numeric_values:
            min_value = min(numeric_values)
            max_value = max(numeric_values)
            mean = statistics.mean(numeric_values)
            median = statistics.median(numeric_values)
        elif non_null:
            min_value = min(non_null)
            max_value = max(non_null)

        return ColumnStats(
            name=col,
            count=count,
            null_count=null_count,
            unique_count=unique_count,
            min_value=min_value,
            max_value=max_value,
            mean=mean,
            median=median,
            is_numeric=is_numeric,
        )
