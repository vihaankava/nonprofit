from datetime import datetime
from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.auth_service import AuthService


class AuthMiddleware:
    """Authentication middleware for FastAPI."""
    
    @staticmethod
    def get_current_user(credentials: HTTPAuthorizationCredentials) -> str:
        """Get current authenticated user from JWT token."""
        user_id = AuthService.verify_token(credentials.credentials)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "AUTHENTICATION_ERROR",
                    "message": "Invalid or expired token",
                    "timestamp": datetime.utcnow()
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
                    "timestamp": datetime.utcnow()
                }
            )
        
        return user_id
    
    @staticmethod
    def authorize_website_access(user_id_param: str, current_user_id: str) -> None:
        """Authorize access to user websites (users can only access their own)."""
        if user_id_param != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "AUTHORIZATION_ERROR",
                    "message": "Access denied: You can only access your own website",
                    "timestamp": datetime.utcnow()
                }
            )
    
    @staticmethod
    def optional_auth(credentials: HTTPAuthorizationCredentials = None) -> str | None:
        """Optional authentication - returns user ID if valid token, None otherwise."""
        if not credentials:
            return None
        
        try:
            user_id = AuthService.verify_token(credentials.credentials)
            if user_id:
                user = AuthService.get_user_by_id(user_id)
                if user:
                    return user_id
        except Exception:
            pass
        
        return None