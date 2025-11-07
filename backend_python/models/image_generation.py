from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from enum import Enum


class ImageType(str, Enum):
    """Types of images that can be generated."""
    POSTER = "poster"
    FLYER = "flyer"
    SOCIAL_MEDIA = "social_media"
    BANNER = "banner"
    LOGO = "logo"
    INFOGRAPHIC = "infographic"


class ImageStyle(str, Enum):
    """Image generation styles."""
    PROFESSIONAL = "professional"
    MODERN = "modern"
    COLORFUL = "colorful"
    MINIMALIST = "minimalist"
    VINTAGE = "vintage"
    BOLD = "bold"


class ImageRequest(BaseModel):
    """Request for image generation."""
    user_id: str
    image_type: ImageType
    description: str
    style: Optional[ImageStyle] = ImageStyle.PROFESSIONAL
    colors: Optional[str] = None  # e.g., "blue and green"
    text_content: Optional[str] = None  # Text to include in image
    additional_details: Optional[str] = None


class GeneratedImage(BaseModel):
    """Generated image response."""
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    image_id: str
    user_id: str
    image_type: ImageType
    title: str
    description: str
    image_url: str
    revised_prompt: Optional[str] = None  # DALL-E's revised prompt
    style: ImageStyle
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime


class ImageGenerationResponse(BaseModel):
    """Response from image generation API."""
    success: bool
    image: Optional[GeneratedImage] = None
    error_message: Optional[str] = None
    usage_stats: Optional[Dict[str, Any]] = None