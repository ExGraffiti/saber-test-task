from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

def validate_config(builds: dict, tasks: dict) -> None:
    """Проверяет, что все задачи из билдов существуют."""
    missing_tasks = {
        task for build_tasks in builds.values()
        for task in build_tasks
        if task not in tasks
    }
    if missing_tasks:
        error_msg = f"Tasks not found: {', '.join(missing_tasks)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg
        )