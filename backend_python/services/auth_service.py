import os
import re
from datetime import datetime, timedelta
from typing import Optional, List
from uuid import uuid4
from passlib.context import CryptContext
from jose import JWTError, jwt
from models.user import User, CreateUserRequest, LoginRequest, AuthResponse, UserResponse, UserProfile

# Password hashing - using simple hash for demo (use bcrypt in production)
import hashlib
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_HOURS", "24"))

# In-memory storage for demo (replace with database in production)
users_db: List[User] = []


class AuthService:
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA-256 (demo only - use bcrypt in production)."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password
    
    @staticmethod
    def create_access_token(user_id: str) -> str:
        """Create a JWT access token."""
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        to_encode = {"sub": user_id, "exp": expire}
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    def verify_token(token: str) -> Optional[str]:
        """Verify a JWT token and return the user ID."""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                return None
            return user_id
        except JWTError:
            return None
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """Validate password strength."""
        return len(password) >= 8
    
    @staticmethod
    def register_user(user_data: CreateUserRequest) -> AuthResponse:
        """Register a new user."""
        # Check if user already exists
        existing_user = next((u for u in users_db if u.email == user_data.email), None)
        if existing_user:
            raise ValueError("User already exists with this email")
        
        # Validate email format
        if not AuthService.validate_email(user_data.email):
            raise ValueError("Invalid email format")
        
        # Validate password strength
        if not AuthService.validate_password(user_data.password):
            raise ValueError("Password must be at least 8 characters long")
        
        # Hash password
        password_hash = AuthService.hash_password(user_data.password)
        
        # Create new user
        now = datetime.utcnow()
        new_user = User(
            user_id=str(uuid4()),
            email=user_data.email,
            password_hash=password_hash,
            profile=user_data.profile,
            created_at=now,
            last_login_at=now
        )
        
        # Store user
        users_db.append(new_user)
        
        # Generate token
        token = AuthService.create_access_token(new_user.user_id)
        
        # Return response without password hash
        user_response = UserResponse(
            user_id=new_user.user_id,
            email=new_user.email,
            profile=new_user.profile,
            created_at=new_user.created_at,
            last_login_at=new_user.last_login_at
        )
        
        return AuthResponse(user=user_response, token=token)
    
    @staticmethod
    def login_user(login_data: LoginRequest) -> AuthResponse:
        """Login a user."""
        # Find user by email
        user = next((u for u in users_db if u.email == login_data.email), None)
        if not user:
            raise ValueError("Invalid email or password")
        
        # Verify password
        if not AuthService.verify_password(login_data.password, user.password_hash):
            raise ValueError("Invalid email or password")
        
        # Update last login
        user.last_login_at = datetime.utcnow()
        
        # Generate token
        token = AuthService.create_access_token(user.user_id)
        
        # Return response without password hash
        user_response = UserResponse(
            user_id=user.user_id,
            email=user.email,
            profile=user.profile,
            created_at=user.created_at,
            last_login_at=user.last_login_at
        )
        
        return AuthResponse(user=user_response, token=token)
    
    @staticmethod
    def get_user_by_id(user_id: str) -> Optional[UserResponse]:
        """Get user by ID."""
        user = next((u for u in users_db if u.user_id == user_id), None)
        if not user:
            return None
        
        return UserResponse(
            user_id=user.user_id,
            email=user.email,
            profile=user.profile,
            created_at=user.created_at,
            last_login_at=user.last_login_at
        )
    
    @staticmethod
    def update_user_profile(user_id: str, profile_data: dict) -> Optional[UserResponse]:
        """Update user profile."""
        user = next((u for u in users_db if u.user_id == user_id), None)
        if not user:
            return None
        
        # Update profile fields
        for key, value in profile_data.items():
            if hasattr(user.profile, key):
                setattr(user.profile, key, value)
        
        return UserResponse(
            user_id=user.user_id,
            email=user.email,
            profile=user.profile,
            created_at=user.created_at,
            last_login_at=user.last_login_at
        )