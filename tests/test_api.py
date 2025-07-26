# test_api.py
from fastapi import status


def test_valid_build(client, mock_config):
    response = client.post("/get_tasks", json={"build": "forward_interest"})
    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()["tasks"]
    assert tasks.index("build_teal_leprechauns") < tasks.index("coloring_aqua_centaurs")


def test_nonexistent_build(client, mock_config):
    response = client.post("/get_tasks", json={"build": "missing_build"})
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_cyclic_dependencies(client, mock_config):
    response = client.post("/get_tasks", json={"build": "cyclic_build"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST, \
        f"Expected 400 for cyclic deps, got {response.status_code}. Response: {response.text}"
