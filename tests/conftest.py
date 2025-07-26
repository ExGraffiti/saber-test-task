# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.config.loader import config_manager


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_config(monkeypatch):
    test_config = {
        "tasks": {
            "task_1": [],
            "task_2": ["task_1"],
            "task_3": ["task_2"],
            "build_teal_leprechauns": [],
            "coloring_aqua_centaurs": ["build_teal_leprechauns"],
            "task_a": ["task_b"],
            "task_b": ["task_a"]
        },
        "builds": {
            "simple_build": ["task_1"],
            "forward_interest": ["build_teal_leprechauns", "coloring_aqua_centaurs"],
            "cyclic_build": ["task_a"]
        }
    }

    # Сохраняем оригинальный конфиг для восстановления
    original_config = config_manager._config

    # Устанавливаем тестовый конфиг
    config_manager._config = test_config

    yield

    # Восстанавливаем оригинальный конфиг
    config_manager._config = original_config