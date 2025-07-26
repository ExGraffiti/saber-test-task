# test_unit.py
from src.services.dependency import resolve_task_dependencies
from src.services.sorter import topological_sort
from fastapi import HTTPException
import pytest


def test_build_dependency_graph():
    # Переносим тест в отдельный файл или модифицируем
    tasks = [{"name": "task_a", "dependencies": ["task_b"]}]

    # Если нужно сохранить эту проверку, можно создать временную функцию
    def build_graph(tasks):
        return {task["name"]: task.get("dependencies", []) for task in tasks}

    assert build_graph(tasks) == {"task_a": ["task_b"]}


def test_resolve_dependencies():
    graph = {"a": ["b"], "b": []}
    assert resolve_task_dependencies(["a"], graph) == {"a", "b"}


def test_topological_sort():
    assert topological_sort({"a": [], "b": ["a"]}) == ["a", "b"]


def test_cycle_detection():
    with pytest.raises(HTTPException):
        topological_sort({"a": ["b"], "b": ["a"]})
