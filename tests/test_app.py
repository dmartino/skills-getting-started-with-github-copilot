import pytest

# Arrange-Act-Assert pattern is used in all tests

def test_get_activities(client):
    # Arrange: (nothing to set up, activities are reset by fixture)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    for activity in data.values():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity
        assert isinstance(activity["participants"], list)

def test_signup_success(client):
    # Arrange
    email = "student1@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    # Confirm participant is added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]

def test_signup_duplicate(client):
    # Arrange
    email = "student2@mergington.edu"
    activity = next(iter(client.get("/activities").json().keys()))
    client.post(f"/activities/{activity}/signup?email={email}")
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Student is already signed up"

def test_signup_activity_not_found(client):
    # Arrange
    email = "student3@mergington.edu"
    activity = "NonExistentActivity"
    
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Activity not found"

def test_root_redirect(client):
    # Arrange: nothing
    # Act
    response = client.get("/", follow_redirects=False)
    # Assert
    assert response.status_code in (302, 307)
    assert "/static/index.html" in response.headers["location"]
