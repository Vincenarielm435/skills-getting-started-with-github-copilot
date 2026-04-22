def test_get_activities_returns_expected_status_and_payload(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert expected_activity in data


def test_get_activities_returns_expected_schema_for_each_activity(client):
    # Arrange
    required_keys = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities_payload = response.json()
    for activity_details in activities_payload.values():
        assert required_keys.issubset(activity_details.keys())
        assert isinstance(activity_details["participants"], list)


def test_get_activities_contains_seed_participants(client):
    # Arrange
    expected_participant = "michael@mergington.edu"

    # Act
    response = client.get("/activities")

    # Assert
    participants = response.json()["Chess Club"]["participants"]
    assert expected_participant in participants
