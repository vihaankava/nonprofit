from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.image_service import ImageService
from services.auth_service import AuthService
from models.image_generation import ImageRequest, ImageGenerationResponse, ImageType, ImageStyle

router = APIRouter(prefix="/images", tags=["image-generation"])
security = HTTPBearer()
image_service = ImageService()


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


@router.post("/generate", response_model=ImageGenerationResponse)
async def generate_image(
    request: ImageRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Generate an image using DALL-E."""
    try:
        # Ensure the request is for the authenticated user
        if request.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "AUTHORIZATION_ERROR",
                    "message": "You can only generate images for your own account",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        # Generate image
        response = await image_service.generate_image(request)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SERVER_ERROR",
                "message": f"Image generation failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.post("/demo", response_model=ImageGenerationResponse)
async def generate_demo_image(
    image_type: ImageType,
    description: str,
    style: ImageStyle = ImageStyle.PROFESSIONAL,
    colors: str = None
):
    """Generate a demo image without authentication."""
    try:
        demo_request = ImageRequest(
            user_id="demo-user",
            image_type=image_type,
            description=description,
            style=style,
            colors=colors,
            additional_details="Demo image generation for testing"
        )
        
        response = await image_service.generate_image(demo_request)
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SERVER_ERROR",
                "message": f"Demo image generation failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/types")
async def get_image_types():
    """Get available image types and styles."""
    return {
        "image_types": [
            {
                "type": ImageType.POSTER,
                "name": "Poster",
                "description": "Large format promotional posters"
            },
            {
                "type": ImageType.FLYER,
                "name": "Flyer",
                "description": "Compact promotional flyers"
            },
            {
                "type": ImageType.SOCIAL_MEDIA,
                "name": "Social Media",
                "description": "Graphics optimized for social platforms"
            },
            {
                "type": ImageType.BANNER,
                "name": "Banner",
                "description": "Web banners and headers"
            },
            {
                "type": ImageType.LOGO,
                "name": "Logo",
                "description": "Organization logos and branding"
            },
            {
                "type": ImageType.INFOGRAPHIC,
                "name": "Infographic",
                "description": "Information graphics and charts"
            }
        ],
        "styles": [
            {
                "style": ImageStyle.PROFESSIONAL,
                "name": "Professional",
                "description": "Clean, corporate, business-appropriate"
            },
            {
                "style": ImageStyle.MODERN,
                "name": "Modern",
                "description": "Contemporary, sleek, trendy"
            },
            {
                "style": ImageStyle.COLORFUL,
                "name": "Colorful",
                "description": "Vibrant, energetic, eye-catching"
            },
            {
                "style": ImageStyle.MINIMALIST,
                "name": "Minimalist",
                "description": "Simple, clean, uncluttered"
            },
            {
                "style": ImageStyle.VINTAGE,
                "name": "Vintage",
                "description": "Retro, classic, timeless"
            },
            {
                "style": ImageStyle.BOLD,
                "name": "Bold",
                "description": "Strong, striking, impactful"
            }
        ]
    }