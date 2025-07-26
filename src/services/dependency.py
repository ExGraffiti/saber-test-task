from typing import Set, List, Dict
from collections import deque

def resolve_task_dependencies(
    initial_tasks: List[str],
    dependency_graph: Dict[str, List[str]]
) -> Set[str]:
    """Находит все зависимости для задач билда."""
    resolved = set(initial_tasks)
    queue = deque(initial_tasks)

    while queue:
        task = queue.popleft()
        for dependency in dependency_graph.get(task, []):
            if dependency not in resolved:
                resolved.add(dependency)
                queue.append(dependency)

    return resolved