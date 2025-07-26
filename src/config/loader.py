# src/config/loader.py
import yaml
from pathlib import Path
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)
BUILDS_DIR = Path(__file__).parent.parent.parent / "builds"


class ConfigManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._config = None
        return cls._instance

    @property
    def config(self):
        if self._config is None:
            self.reload()
        return self._config

    def reload(self):
        try:
            builds = {
                build["name"]: build["tasks"]
                for build in self._load_yaml("builds.yaml")["builds"]
            }
            tasks = {
                task["name"]: task.get("dependencies", [])
                for task in self._load_yaml("tasks.yaml")["tasks"]
            }
            self._config = {"builds": builds, "tasks": tasks}
        except Exception as e:
            logger.error(f"Config load failed: {str(e)}")
            raise

    def _load_yaml(self, filename: str) -> dict:
        file_path = BUILDS_DIR / filename
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            logger.error(f"Config file not found: {file_path}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Config file not found: {file_path}"
            )
        except yaml.YAMLError as e:
            logger.error(f"Invalid YAML in {file_path}: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Invalid YAML in {file_path}"
            )


config_manager = ConfigManager()