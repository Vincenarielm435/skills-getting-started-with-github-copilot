from src.app import activities


def test_unregister_removes_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "someone@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_if_participant_not_registered(client):
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_keeps_other_activity_participants_unchanged(client):
    # Arrange
    target_activity = "Chess Club"
    email_to_remove = "michael@mergington.edu"
    untouched_activity = "Programming Class"
    previous_untouched_participants = list(activities[untouched_activity]["participants"])

    # Act
    response = client.delete(f"/activities/{target_activity}/participants/{email_to_remove}")

    # Assert
    assert response.status_code == 200
    assert activities[untouched_activity]["participants"] == previous_untouched_participants
