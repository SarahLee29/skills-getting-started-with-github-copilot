import copy
import importlib

import pytest
from fastapi.testclient import TestClient


# Arrange: import app module and snapshot original activities
app_module = importlib.import_module("src.app")
_ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)
client = TestClient(app_module.app)


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: reset global activities before each test
    app_module.activities = copy.deepcopy(_ORIGINAL_ACTIVITIES)
    yield
    app_module.activities = copy.deepcopy(_ORIGINAL_ACTIVITIES)


def test_get_activities_returns_activities():
    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant_and_allows_duplicates():
    # Arrange
    activity = "Chess%20Club"
    email = "teststudent@mergington.edu"

    # Act: first signup
    resp1 = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert first signup succeeded and participant added
    assert resp1.status_code == 200
    participants = app_module.activities["Chess Club"]["participants"]
    assert any(p.strip().lower() == email.strip().lower() for p in participants)

    # Act: duplicate signup (current behavior appends again)
    resp2 = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert duplicate is appended (two occurrences now)
    assert resp2.status_code == 200
    participants_after = app_module.activities["Chess Club"]["participants"]
    matches = [p for p in participants_after if p.strip().lower() == email.strip().lower()]
    assert len(matches) >= 2


def test_delete_participant_removes_student():
    # Arrange
    activity = "Chess%20Club"
    target = "michael@mergington.edu"

    # Precondition: participant exists
    assert any(p.strip().lower() == target for p in app_module.activities["Chess Club"]["participants"])

    # Act
    resp = client.delete(f"/activities/{activity}/participants", params={"email": target})

    # Assert
    assert resp.status_code == 200
    participants_after = app_module.activities["Chess Club"]["participants"]
    assert not any(p.strip().lower() == target for p in participants_after)
