from app.infrastructure.config import RootConfig
from typing import Dict
from yaml import safe_load


def load_yaml_file(file_path: str) -> Dict:
    try:
        with open(file_path, "r") as stream:
            return safe_load(stream) or {}
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file {file_path} not found.")
    except Exception as e:
        raise RuntimeError(f"Error loading YAML file {file_path}: {e}")


def get_config(
    app_config: str,
    database_config: str,
) -> RootConfig:
    app_data = load_yaml_file(app_config).get('app', {})
    database_data = load_yaml_file(database_config).get('database', {})

    config_data = {
        "app": app_data,
        "database": database_data,
    }

    return RootConfig(**config_data)
