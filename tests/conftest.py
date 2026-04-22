import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities_state():
    # Keep every test independent because the app stores data in a mutable global.
    initial_state = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(initial_state)


@pytest.fixture
def client():
    return TestClient(app)
