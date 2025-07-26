from collections import defaultdict, deque
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

def topological_sort(dependency_graph: dict) -> list:
    """Сортирует задачи с учётом зависимостей (алгоритм Кана)."""
    in_degree = defaultdict(int)
    reverse_graph = defaultdict(list)
    queue = deque()
    result = []

    # Построение обратного графа и подсчёт входящих степеней
    for task, deps in dependency_graph.items():
        for dep in deps:
            reverse_graph[dep].append(task)
            in_degree[task] += 1
        if not deps:
            queue.append(task)

    # Обработка задач без зависимостей
    while queue:
        task = queue.popleft()
        result.append(task)
        for dependent in reverse_graph[task]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    # Проверка на циклы
    if len(result) != len(dependency_graph):
        logger.error("Cyclic dependencies detected")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cyclic dependencies in task graph"
        )

    return result