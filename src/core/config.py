# src/core/config.py
"""
Centralized configuration management for the CMF application.

Loads settings from a YAML file and provides them as a singleton object.
"""
import yaml
from pathlib import Path
from typing import Any, Dict

class Config:
    """A singleton class to hold application configuration."""
    _instance = None
    _config_data: Dict[str, Any] = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Config, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def load_config(self, config_path: Path) -> None:
        """
        Loads configuration from a YAML file.

        Args:
            config_path: The path to the configuration file.
        """
        if not self._config_data:
            try:
                with open(config_path, 'r') as f:
                    self._config_data = yaml.safe_load(f)
                print(f"Configuration loaded successfully from {config_path}")
            except FileNotFoundError:
                print(f"Error: Configuration file not found at {config_path}")
                raise
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file: {e}")
                raise

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieves a configuration value.

        Args:
            key: The configuration key (e.g., 'trading.exchange').
            default: The default value to return if the key is not found.

        Returns:
            The configuration value.
        """
        keys = key.split('.')
        value = self._config_data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

# Create a single instance of the config to be used across the application
config = Config()

# Usage:
# from src.core.config import config
# config.load_config(Path('configs/config.yaml'))
# api_key = config.get('api.binance.api_key')