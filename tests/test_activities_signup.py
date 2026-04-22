from src.app import activities


def test_signup_adds_new_participant_successfully(client):
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": new_email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
    assert new_email in activities[activity_name]["participants"]


def test_signup_returns_404_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Activity"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_duplicate_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_mutates_only_target_activity_participants(client):
    # Arrange
    target_activity = "Chess Club"
    untouched_activity = "Programming Class"
    new_email = "targetonly@mergington.edu"
    previous_untouched_participants = list(activities[untouched_activity]["participants"])

    # Act
    response = client.post(f"/activities/{target_activity}/signup", params={"email": new_email})

    # Assert
    assert response.status_code == 200
    assert new_email in activities[target_activity]["participants"]
    assert activities[untouched_activity]["participants"] == previous_untouched_participants
