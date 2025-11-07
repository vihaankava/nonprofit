from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth_service import AuthService
from models.user import CreateUserRequest, LoginRequest, AuthResponse, UserResponse, ErrorResponse
from middleware.rate_limit_middleware import auth_rate_limiter, registration_rate_limiter

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Dependency to get current authenticated user."""
    user_id = AuthService.verify_token(credentials.credentials)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "AUTHENTICATION_ERROR",
                "message": "Invalid or expired token",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    # Verify user still exists
    user = AuthService.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "AUTHENTICATION_ERROR",
                "message": "User not found",
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    return user_id


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register_user(request: Request, user_data: CreateUserRequest):
    """Register a new user."""
    # Apply rate limiting
    registration_rate_limiter(request)
    
    try:
        # Validate required fields
        if not user_data.profile.first_name or not user_data.profile.last_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": "VALIDATION_ERROR",
                    "message": "First name and last name are required",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        auth_response = AuthService.register_user(user_data)
        return auth_response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": "REGISTRATION_ERROR",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SERVER_ERROR",
                "message": "Registration failed",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.post("/login", response_model=AuthResponse)
async def login_user(request: Request, login_data: LoginRequest):
    """Login a user."""
    # Apply rate limiting
    auth_rate_limiter(request)
    
    try:
        auth_response = AuthService.login_user(login_data)
        return auth_response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "AUTHENTICATION_ERROR",
                "message": str(e),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SERVER_ERROR",
                "message": "Login failed",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/profile", response_model=dict)
async def get_user_profile(current_user_id: str = Depends(get_current_user)):
    """Get current user profile."""
    try:
        user = AuthService.get_user_by_id(current_user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "USER_NOT_FOUND",
                    "message": "User not found",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        return {"user": user}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SERVER_ERROR",
                "message": "Failed to retrieve user profile",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.put("/profile", response_model=dict)
async def update_user_profile(
    profile_data: dict,
    current_user_id: str = Depends(get_current_user)
):
    """Update current user profile."""
    try:
        updated_user = AuthService.update_user_profile(current_user_id, profile_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "USER_NOT_FOUND",
                    "message": "User not found",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        return {"user": updated_user}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SERVER_ERROR",
                "message": "Failed to update user profile",
                "timestamp": datetime.utcnow().isoformat()
            }
        )