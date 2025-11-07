import time
from datetime import datetime, timedelta
from typing import Dict, Optional
from fastapi import HTTPException, Request, status
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded


# In-memory rate limit store (replace with Redis in production)
rate_limit_store: Dict[str, Dict[str, any]] = {}


def cleanup_expired_entries():
    """Clean up expired rate limit entries."""
    current_time = time.time()
    expired_keys = []
    
    for key, data in rate_limit_store.items():
        if data.get('reset_time', 0) < current_time:
            expired_keys.append(key)
    
    for key in expired_keys:
        del rate_limit_store[key]


class CustomRateLimiter:
    """Custom rate limiter for authentication endpoints."""
    
    def __init__(self, max_requests: int, window_seconds: int, message: str = "Rate limit exceeded"):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.message = message
    
    def __call__(self, request: Request):
        """Check rate limit for the request."""
        # Clean up expired entries periodically
        if len(rate_limit_store) > 1000:  # Cleanup when store gets large
            cleanup_expired_entries()
        
        # Generate key based on IP and endpoint
        client_ip = get_remote_address(request)
        endpoint = request.url.path
        key = f"{client_ip}:{endpoint}"
        
        # For auth endpoints, include email in key for more granular control
        if endpoint in ["/auth/login", "/auth/register"]:
            try:
                # This is a simplified approach - in production, you'd want to
                # parse the request body more carefully
                email = getattr(request.state, 'email', '')
                if email:
                    key = f"{client_ip}:{endpoint}:{email}"
            except:
                pass
        
        current_time = time.time()
        reset_time = current_time + self.window_seconds
        
        # Initialize or get existing rate limit data
        if key not in rate_limit_store or rate_limit_store[key]['reset_time'] < current_time:
            rate_limit_store[key] = {
                'count': 1,
                'reset_time': reset_time
            }
        else:
            rate_limit_store[key]['count'] += 1
        
        count = rate_limit_store[key]['count']
        
        # Check if rate limit exceeded
        if count > self.max_requests:
            retry_after = int(rate_limit_store[key]['reset_time'] - current_time)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail={
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": self.message,
                    "retry_after": retry_after,
                    "timestamp": datetime.utcnow().isoformat()
                },
                headers={"Retry-After": str(retry_after)}
            )
        
        return True


# Predefined rate limiters
auth_rate_limiter = CustomRateLimiter(
    max_requests=5,
    window_seconds=15 * 60,  # 15 minutes
    message="Too many authentication attempts, please try again in 15 minutes"
)

registration_rate_limiter = CustomRateLimiter(
    max_requests=3,
    window_seconds=60 * 60,  # 1 hour
    message="Too many registration attempts, please try again in 1 hour"
)

general_api_rate_limiter = CustomRateLimiter(
    max_requests=100,
    window_seconds=15 * 60,  # 15 minutes
    message="Too many API requests, please try again later"
)


# SlowAPI limiter for general use
limiter = Limiter(key_func=get_remote_address)


def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Custom rate limit exceeded handler."""
    return HTTPException(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        detail={
            "code": "RATE_LIMIT_EXCEEDED",
            "message": "Rate limit exceeded",
            "retry_after": exc.retry_after,
            "timestamp": datetime.utcnow()
        }
    )