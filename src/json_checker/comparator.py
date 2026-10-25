"""
Module xử lý trích xuất key đa tầng và so sánh sự khác biệt giữa hai tập dữ liệu JSON.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Set


def flatten_keys(data: Any, prefix: str = "") -> Set[str]:
    """Lấy toàn bộ key trong file JSON nhiều lớp, hỗ trợ cả dict và list lồng nhau."""
    keys: Set[str] = set()

    if isinstance(data, dict):
        for key, value in data.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            keys.add(path)
            keys.update(flatten_keys(value, path))
    elif isinstance(data, list):
        for i, item in enumerate(data):
            path = f"{prefix}[{i}]" if prefix else f"[{i}]"
            keys.add(path)
            keys.update(flatten_keys(item, path))
    return keys


@dataclass
class ComparisonResult:
    source_keys: Set[str]
    dest_keys: Set[str]
    missing_in_dest: List[str]
    extra_in_dest: List[str]

    @property
    def total_source(self) -> int:
        return len(self.source_keys)

    @property
    def total_dest(self) -> int:
        return len(self.dest_keys)

    @property
    def missing_count(self) -> int:
        return len(self.missing_in_dest)

    @property
    def extra_count(self) -> int:
        return len(self.extra_in_dest)


def compare_json_data(source_data: Any, dest_data: Any) -> ComparisonResult:
    """So sánh hai đối tượng dữ liệu JSON và trả về kết quả chi tiết."""
    source_keys = flatten_keys(source_data)
    dest_keys = flatten_keys(dest_data)

    missing = sorted(source_keys - dest_keys)
    extra = sorted(dest_keys - source_keys)

    return ComparisonResult(
        source_keys=source_keys,
        dest_keys=dest_keys,
        missing_in_dest=missing,
        extra_in_dest=extra,
    )
