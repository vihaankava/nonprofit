import pytest
from fastapi.testclient import TestClient
from main import app
from services.auth_service import AuthService

client = TestClient(app)


class TestAuthRoutes:
    """Test cases for authentication routes."""
    
    def setup_method(self):
        """Clear users database before each test."""
        from services.auth_service import users_db
        users_db.clear()
    
    def test_register_success(self):
        """Test successful user registration."""
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "profile": {
                "first_name": "John",
                "last_name": "Doe",
                "location": "New York"
            }
        }
        
        response = client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 201
        data = response.json()
        assert "user" in data
        assert "token" in data
        assert data["user"]["email"] == user_data["email"]
        assert data["user"]["profile"]["first_name"] == user_data["profile"]["first_name"]
    
    def test_register_missing_name(self):
        """Test registration with missing first or last name."""
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "profile": {
                "first_name": "John"
                # Missing last_name
            }
        }
        
        response = client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 400
        data = response.json()
        assert data["code"] == "VALIDATION_ERROR"
        assert "First name and last name are required" in data["message"]
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email."""
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "profile": {
                "first_name": "John",
                "last_name": "Doe"
            }
        }
        
        # Register first user
        client.post("/api/auth/register", json=user_data)
        
        # Try to register with same email
        response = client.post("/api/auth/register", json=user_data)
        
        assert response.status_code == 400
        data = response.json()
        assert data["code"] == "REGISTRATION_ERROR"
        assert "User already exists with this email" in data["message"]
    
    def test_login_success(self):
        """Test successful login."""
        # Register user first
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "profile": {
                "first_name": "John",
                "last_name": "Doe"
            }
        }
        client.post("/api/auth/register", json=user_data)
        
        # Login
        login_data = {
            "email": "test@example.com",
            "password": "testpassword123"
        }
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert "token" in data
        assert data["user"]["email"] == login_data["email"]
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "wrongpassword"
        }
        
        response = client.post("/api/auth/login", json=login_data)
        
        assert response.status_code == 401
        data = response.json()
        assert data["code"] == "AUTHENTICATION_ERROR"
        assert "Invalid email or password" in data["message"]
    
    def test_get_profile_success(self):
        """Test getting user profile with valid token."""
        # Register and login user
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "profile": {
                "first_name": "John",
                "last_name": "Doe"
            }
        }
        register_response = client.post("/api/auth/register", json=user_data)
        token = register_response.json()["token"]
        
        # Get profile
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/auth/profile", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert data["user"]["email"] == user_data["email"]
    
    def test_get_profile_no_token(self):
        """Test getting profile without token."""
        response = client.get("/api/auth/profile")
        
        assert response.status_code == 403  # FastAPI returns 403 for missing auth
    
    def test_get_profile_invalid_token(self):
        """Test getting profile with invalid token."""
        headers = {"Authorization": "Bearer invalid-token"}
        response = client.get("/api/auth/profile", headers=headers)
        
        assert response.status_code == 401
        data = response.json()
        assert data["code"] == "AUTHENTICATION_ERROR"
    
    def test_update_profile_success(self):
        """Test updating user profile."""
        # Register user
        user_data = {
            "email": "test@example.com",
            "password": "testpassword123",
            "profile": {
                "first_name": "John",
                "last_name": "Doe"
            }
        }
        register_response = client.post("/api/auth/register", json=user_data)
        token = register_response.json()["token"]
        
        # Update profile
        update_data = {
            "first_name": "Jane",
            "location": "California"
        }
        headers = {"Authorization": f"Bearer {token}"}
        response = client.put("/api/auth/profile", json=update_data, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["user"]["profile"]["first_name"] == "Jane"
        assert data["user"]["profile"]["last_name"] == "Doe"  # Should remain unchanged
        assert data["user"]["profile"]["location"] == "California"
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "OK"
        assert "timestamp" in data
    
    def test_api_info(self):
        """Test API info endpoint."""
        response = client.get("/api")
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "timestamp" in data