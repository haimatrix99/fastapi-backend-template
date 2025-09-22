def test_create_user(client):
    """Test creating a new user."""
    user_data = {"name": "John Doe", "email": "john.doe@example.com"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "created_at" in data


def test_create_user_duplicate_email(client):
    """Test creating a user with an existing email."""
    user_data = {"name": "John Doe", "email": "john.doe@example.com"}
    # Create first user
    client.post("/users/", json=user_data)

    # Try to create another user with the same email
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_get_users(client):
    """Test getting all users."""
    # Create a user first
    user_data = {"name": "John Doe", "email": "john.doe@example.com"}
    client.post("/users/", json=user_data)

    # Get all users
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["name"] == user_data["name"]
    assert data[0]["email"] == user_data["email"]


def test_get_user_by_id(client):
    """Test getting a user by ID."""
    # Create a user first
    user_data = {"name": "John Doe", "email": "john.doe@example.com"}
    create_response = client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]

    # Get user by ID
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]


def test_get_user_not_found(client):
    """Test getting a user that doesn't exist."""
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User with ID 999 not found"


def test_update_user(client):
    """Test updating a user."""
    # Create a user first
    user_data = {"name": "John Doe", "email": "john.doe@example.com"}
    create_response = client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]

    # Update the user
    update_data = {"name": "Jane Doe"}
    response = client.put(f"/users/{user_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "Jane Doe"
    assert data["email"] == user_data["email"]  # Email should remain unchanged
    assert "updated_at" in data


def test_update_user_not_found(client):
    """Test updating a user that doesn't exist."""
    update_data = {"name": "Jane Doe"}
    response = client.put("/users/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "User with ID 999 not found"


def test_update_user_duplicate_email(client):
    """Test updating a user with an email that already exists."""
    # Create two users
    user1_data = {"name": "John Doe", "email": "john.doe@example.com"}
    user2_data = {"name": "Jane Smith", "email": "jane.smith@example.com"}
    client.post("/users/", json=user1_data)
    user2_response = client.post("/users/", json=user2_data)
    user2_id = user2_response.json()["id"]

    # Try to update user2 with user1's email
    update_data = {"email": "john.doe@example.com"}
    response = client.put(f"/users/{user2_id}", json=update_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_delete_user(client):
    """Test deleting a user."""
    # Create a user first
    user_data = {"name": "John Doe", "email": "john.doe@example.com"}
    create_response = client.post("/users/", json=user_data)
    user_id = create_response.json()["id"]

    # Delete the user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verify the user is deleted
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404


def test_delete_user_not_found(client):
    """Test deleting a user that doesn't exist."""
    response = client.delete("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User with ID 999 not found"
