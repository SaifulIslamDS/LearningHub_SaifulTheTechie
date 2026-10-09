"""Load and validate the cleaning rules from a TOML file."""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


class ConfigError(Exception):
    """Raised when the config file is missing or invalid."""


@dataclass
class Config:
    required_columns: list[str] = field(default_factory=list)
    encoding: str = "utf-8"
    trim: list[str] = field(default_factory=list)
    title_case: list[str] = field(default_factory=list)
    integers: list[str] = field(default_factory=list)
    decimals: list[str] = field(default_factory=list)
    date_column: str | None = None
    date_format: str = "%Y-%m-%d"
    drop_duplicates: bool = True
    rename: dict[str, str] = field(default_factory=dict)


def load_config(path: str | Path) -> Config:
    """Read a TOML config file and return a Config object."""
    path = Path(path)
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")
    try:
        with path.open("rb") as f:
            raw = tomllib.load(f)
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"Config file is not valid TOML: {exc}") from exc

    inp, clean, out = raw.get("input", {}), raw.get("clean", {}), raw.get("output", {})
    cfg = Config(
        required_columns=list(inp.get("required_columns", [])),
        encoding=inp.get("encoding", "utf-8"),
        trim=list(clean.get("trim", [])),
        title_case=list(clean.get("title_case", [])),
        integers=list(clean.get("integers", [])),
        decimals=list(clean.get("decimals", [])),
        date_column=clean.get("date_column"),
        date_format=clean.get("date_format", "%Y-%m-%d"),
        drop_duplicates=bool(clean.get("drop_duplicates", True)),
        rename=dict(out.get("rename", {})),
    )
    if not isinstance(cfg.drop_duplicates, bool):
        raise ConfigError("clean.drop_duplicates must be true or false")
    return cfg
