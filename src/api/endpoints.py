# src/api/endpoints.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from src.config.loader import config_manager
from src.services.dependency import resolve_task_dependencies
from src.services.sorter import topological_sort
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class BuildRequest(BaseModel):
    build: str

@router.post("/get_tasks")
async def get_sorted_build_tasks(request: BuildRequest) -> dict:
    try:
        config = config_manager.config
        if request.build not in config["builds"]:
            logger.warning(f"Build '{request.build}' not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Build '{request.build}' not found"
            )

        build_tasks = config["builds"][request.build]
        all_tasks = resolve_task_dependencies(build_tasks, config["tasks"])
        filtered_graph = {
            task: deps
            for task, deps in config["tasks"].items()
            if task in all_tasks
        }
        sorted_tasks = topological_sort(filtered_graph)
        return {"tasks": sorted_tasks}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing build: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )