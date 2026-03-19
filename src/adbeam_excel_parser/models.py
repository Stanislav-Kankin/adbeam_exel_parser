from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class RowPreview(BaseModel):
    row_index: int = Field(description="1-based Excel row index")
    website: str | None = None
    values: dict[str, Any] = Field(default_factory=dict)


class ExcelReadSummary(BaseModel):
    file_path: str
    sheet_name: str
    total_rows: int
    headers: list[str]
    website_columns: list[str] = Field(default_factory=list)
    rows_with_websites: int = 0
    preview: list[RowPreview] = Field(default_factory=list)
