import pytest
from datetime import datetime
from services.auth_service import AuthService
from models.user import CreateUserRequest, LoginRequest, UserProfile


class TestAuthService:
    """Test cases for AuthService."""
    
    def setup_method(self):
        """Clear users database before each test."""
        from services.auth_service import users_db
        users_db.clear()
    
    def test_hash_password(self):
        """Test password hashing."""
        password = "testpassword123"
        hashed = AuthService.hash_password(password)
        
        assert hashed is not None
        assert hashed != password
        assert len(hashed) > 50
    
    def test_verify_password(self):
        """Test password verification."""
        password = "testpassword123"
        hashed = AuthService.hash_password(password)
        
        assert AuthService.verify_password(password, hashed) is True
        assert AuthService.verify_password("wrongpassword", hashed) is False
    
    def test_create_access_token(self):
        """Test JWT token creation."""
        user_id = "test-user-id"
        token = AuthService.create_access_token(user_id)
        
        assert token is not None
        assert isinstance(token, str)
        assert len(token.split('.')) == 3  # JWT has 3 parts
    
    def test_verify_token(self):
        """Test JWT token verification."""
        user_id = "test-user-id"
        token = AuthService.create_access_token(user_id)
        decoded_user_id = AuthService.verify_token(token)
        
        assert decoded_user_id == user_id
    
    def test_verify_invalid_token(self):
        """Test invalid JWT token verification."""
        invalid_token = "invalid.token.here"
        result = AuthService.verify_token(invalid_token)
        
        assert result is None
    
    def test_validate_email(self):
        """Test email validation."""
        assert AuthService.validate_email("test@example.com") is True
        assert AuthService.validate_email("invalid-email") is False
        assert AuthService.validate_email("test@") is False
        assert AuthService.validate_email("@example.com") is False
    
    def test_validate_password(self):
        """Test password validation."""
        assert AuthService.validate_password("password123") is True
        assert AuthService.validate_password("short") is False
        assert AuthService.validate_password("") is False
    
    def test_register_user_success(self):
        """Test successful user registration."""
        user_data = CreateUserRequest(
            email="test@example.com",
            password="testpassword123",
            profile=UserProfile(
                first_name="John",
                last_name="Doe",
                location="New York"
            )
        )
        
        result = AuthService.register_user(user_data)
        
        assert result is not None
        assert result.user.email == user_data.email
        assert result.user.profile.first_name == user_data.profile.first_name
        assert result.user.profile.last_name == user_data.profile.last_name
        assert result.user.user_id is not None
        assert result.token is not None
        from services.auth_service import users_db
        assert len(users_db) == 1
    
    def test_register_duplicate_email(self):
        """Test registration with duplicate email."""
        user_data = CreateUserRequest(
            email="test@example.com",
            password="testpassword123",
            profile=UserProfile(first_name="John", last_name="Doe")
        )
        
        # Register first user
        AuthService.register_user(user_data)
        
        # Try to register with same email
        with pytest.raises(ValueError, match="User already exists with this email"):
            AuthService.register_user(user_data)
    
    def test_register_invalid_email(self):
        """Test registration with invalid email."""
        user_data = CreateUserRequest(
            email="invalid-email",
            password="testpassword123",
            profile=UserProfile(first_name="John", last_name="Doe")
        )
        
        with pytest.raises(ValueError, match="Invalid email format"):
            AuthService.register_user(user_data)
    
    def test_register_weak_password(self):
        """Test registration with weak password."""
        user_data = CreateUserRequest(
            email="test@example.com",
            password="123",
            profile=UserProfile(first_name="John", last_name="Doe")
        )
        
        with pytest.raises(ValueError, match="Password must be at least 8 characters long"):
            AuthService.register_user(user_data)
    
    def test_login_success(self):
        """Test successful login."""
        # Register user first
        user_data = CreateUserRequest(
            email="test@example.com",
            password="testpassword123",
            profile=UserProfile(first_name="John", last_name="Doe")
        )
        AuthService.register_user(user_data)
        
        # Login
        login_data = LoginRequest(
            email="test@example.com",
            password="testpassword123"
        )
        result = AuthService.login_user(login_data)
        
        assert result is not None
        assert result.user.email == login_data.email
        assert result.token is not None
    
    def test_login_invalid_email(self):
        """Test login with invalid email."""
        login_data = LoginRequest(
            email="nonexistent@example.com",
            password="testpassword123"
        )
        
        with pytest.raises(ValueError, match="Invalid email or password"):
            AuthService.login_user(login_data)
    
    def test_login_invalid_password(self):
        """Test login with invalid password."""
        # Register user first
        user_data = CreateUserRequest(
            email="test@example.com",
            password="testpassword123",
            profile=UserProfile(first_name="John", last_name="Doe")
        )
        AuthService.register_user(user_data)
        
        # Try login with wrong password
        login_data = LoginRequest(
            email="test@example.com",
            password="wrongpassword"
        )
        
        with pytest.raises(ValueError, match="Invalid email or password"):
            AuthService.login_user(login_data)
    
    def test_get_user_by_id(self):
        """Test getting user by ID."""
        # Register user first
        user_data = CreateUserRequest(
            email="test@example.com",
            password="testpassword123",
            profile=UserProfile(first_name="John", last_name="Doe")
        )
        result = AuthService.register_user(user_data)
        user_id = result.user.user_id
        
        # Get user by ID
        user = AuthService.get_user_by_id(user_id)
        
        assert user is not None
        assert user.user_id == user_id
        assert user.email == user_data.email
    
    def test_get_nonexistent_user(self):
        """Test getting non-existent user."""
        user = AuthService.get_user_by_id("nonexistent-id")
        assert user is None
    
    def test_update_user_profile(self):
        """Test updating user profile."""
        # Register user first
        user_data = CreateUserRequest(
            email="test@example.com",
            password="testpassword123",
            profile=UserProfile(first_name="John", last_name="Doe")
        )
        result = AuthService.register_user(user_data)
        user_id = result.user.user_id
        
        # Update profile
        update_data = {
            "first_name": "Jane",
            "location": "California"
        }
        updated_user = AuthService.update_user_profile(user_id, update_data)
        
        assert updated_user is not None
        assert updated_user.profile.first_name == "Jane"
        assert updated_user.profile.last_name == "Doe"  # Should remain unchanged
        assert updated_user.profile.location == "California"
    
    def test_update_nonexistent_user_profile(self):
        """Test updating profile of non-existent user."""
        update_data = {"first_name": "Jane"}
        result = AuthService.update_user_profile("nonexistent-id", update_data)
        assert result is None