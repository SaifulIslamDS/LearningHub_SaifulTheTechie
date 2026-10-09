import pytest

from csv_cleaner.config import ConfigError, load_config


def test_loads_project_config():
    cfg = load_config("config.toml")
    assert cfg.date_format == "%d/%m/%Y"
    assert cfg.rename["Qty"] == "quantity"


def test_invalid_toml_raises_config_error(tmp_path):
    bad = tmp_path / "bad.toml"
    bad.write_text("this is = = not toml", encoding="utf-8")
    with pytest.raises(ConfigError):
        load_config(bad)
