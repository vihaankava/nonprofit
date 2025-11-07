import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4
import openai
from models.image_generation import (
    ImageRequest, ImageGenerationResponse, GeneratedImage, 
    ImageType, ImageStyle
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# DALL-E Configuration
DALLE_MODEL = os.getenv("DALLE_MODEL", "dall-e-3")
DALLE_SIZE = os.getenv("DALLE_SIZE", "1024x1024")
DALLE_QUALITY = os.getenv("DALLE_QUALITY", "standard")


class ImageService:
    """Service for AI-powered image generation using DALL-E."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        
        # Only initialize OpenAI client if API key is properly set
        if self.api_key and self.api_key != "your-openai-api-key-here":
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                self.client = None
    
    async def generate_image(self, request: ImageRequest) -> ImageGenerationResponse:
        """Generate an image using DALL-E."""
        try:
            if not self.client:
                return self._generate_demo_response(request)
            
            # Create the prompt for DALL-E
            prompt = self._create_dalle_prompt(request)
            
            logger.info(f"Generating {request.image_type} image for user {request.user_id}")
            
            # Call DALL-E API
            response = self.client.images.generate(
                model=DALLE_MODEL,
                prompt=prompt,
                size=DALLE_SIZE,
                quality=DALLE_QUALITY,
                n=1
            )
            
            # Extract image data
            image_data = response.data[0]
            
            # Create image object
            now = datetime.utcnow()
            image = GeneratedImage(
                image_id=str(uuid4()),
                user_id=request.user_id,
                image_type=request.image_type,
                title=self._generate_title(request),
                description=request.description,
                image_url=image_data.url,
                revised_prompt=image_data.revised_prompt,
                style=request.style,
                metadata={
                    "model": DALLE_MODEL,
                    "size": DALLE_SIZE,
                    "quality": DALLE_QUALITY,
                    "original_prompt": prompt
                },
                created_at=now
            )
            
            return ImageGenerationResponse(
                success=True,
                image=image,
                usage_stats={
                    "model": DALLE_MODEL,
                    "cost_estimate": self._estimate_cost()
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating image: {str(e)}")
            return ImageGenerationResponse(
                success=False,
                error_message=f"Image generation failed: {str(e)}"
            )
    
    def _create_dalle_prompt(self, request: ImageRequest) -> str:
        """Create a detailed prompt for DALL-E based on the request."""
        
        # Base prompt templates for different image types
        base_prompts = {
            ImageType.POSTER: "Create a professional nonprofit poster design",
            ImageType.FLYER: "Design a compelling nonprofit flyer",
            ImageType.SOCIAL_MEDIA: "Create a social media graphic for a nonprofit",
            ImageType.BANNER: "Design a nonprofit banner",
            ImageType.LOGO: "Create a nonprofit organization logo",
            ImageType.INFOGRAPHIC: "Design an infographic for a nonprofit"
        }
        
        # Style descriptions
        style_descriptions = {
            ImageStyle.PROFESSIONAL: "clean, professional, corporate style",
            ImageStyle.MODERN: "modern, sleek, contemporary design",
            ImageStyle.COLORFUL: "vibrant, colorful, energetic design",
            ImageStyle.MINIMALIST: "minimalist, simple, clean design",
            ImageStyle.VINTAGE: "vintage, retro, classic style",
            ImageStyle.BOLD: "bold, striking, eye-catching design"
        }
        
        # Build the prompt
        prompt_parts = [
            base_prompts.get(request.image_type, "Create a nonprofit design"),
            f"with {style_descriptions.get(request.style, 'professional style')}."
        ]
        
        # Add description
        if request.description:
            prompt_parts.append(f"The design should represent: {request.description}")
        
        # Add color preferences
        if request.colors:
            prompt_parts.append(f"Use colors: {request.colors}")
        
        # Add text content if specified
        if request.text_content:
            prompt_parts.append(f"Include text: '{request.text_content}'")
        
        # Add additional details
        if request.additional_details:
            prompt_parts.append(request.additional_details)
        
        # Add quality and format specifications
        prompt_parts.extend([
            "High quality, professional design suitable for printing.",
            "Clear, readable text if any text is included.",
            "Appropriate for nonprofit/charity organization use."
        ])
        
        return " ".join(prompt_parts)
    
    def _generate_title(self, request: ImageRequest) -> str:
        """Generate a title for the image."""
        type_names = {
            ImageType.POSTER: "Poster",
            ImageType.FLYER: "Flyer", 
            ImageType.SOCIAL_MEDIA: "Social Media Graphic",
            ImageType.BANNER: "Banner",
            ImageType.LOGO: "Logo",
            ImageType.INFOGRAPHIC: "Infographic"
        }
        
        base_title = type_names.get(request.image_type, "Design")
        
        # Add description if short enough
        if request.description and len(request.description) < 50:
            return f"{base_title} - {request.description}"
        
        return f"Custom {base_title}"
    
    def _estimate_cost(self) -> float:
        """Estimate the cost of DALL-E image generation."""
        # DALL-E 3 pricing (approximate)
        if DALLE_MODEL == "dall-e-3":
            if DALLE_SIZE == "1024x1024":
                return 0.040  # $0.040 per image
            elif DALLE_SIZE == "1792x1024" or DALLE_SIZE == "1024x1792":
                return 0.080  # $0.080 per image
        elif DALLE_MODEL == "dall-e-2":
            return 0.020  # $0.020 per image for 1024x1024
        
        return 0.040  # Default estimate
    
    def _generate_demo_response(self, request: ImageRequest) -> ImageGenerationResponse:
        """Generate demo response when DALL-E is not available."""
        
        # Create placeholder image URLs (these would be actual generated images in production)
        demo_images = {
            ImageType.POSTER: "https://via.placeholder.com/1024x1024/4CAF50/FFFFFF?text=NONPROFIT+POSTER",
            ImageType.FLYER: "https://via.placeholder.com/1024x1024/2196F3/FFFFFF?text=NONPROFIT+FLYER", 
            ImageType.SOCIAL_MEDIA: "https://via.placeholder.com/1024x1024/FF9800/FFFFFF?text=SOCIAL+MEDIA",
            ImageType.BANNER: "https://via.placeholder.com/1024x1024/9C27B0/FFFFFF?text=NONPROFIT+BANNER",
            ImageType.LOGO: "https://via.placeholder.com/1024x1024/F44336/FFFFFF?text=NONPROFIT+LOGO",
            ImageType.INFOGRAPHIC: "https://via.placeholder.com/1024x1024/607D8B/FFFFFF?text=INFOGRAPHIC"
        }
        
        now = datetime.utcnow()
        demo_image = GeneratedImage(
            image_id=str(uuid4()),
            user_id=request.user_id,
            image_type=request.image_type,
            title=f"[DEMO] {self._generate_title(request)}",
            description=request.description,
            image_url=demo_images.get(request.image_type, demo_images[ImageType.POSTER]),
            revised_prompt=f"Demo image for {request.image_type.value}",
            style=request.style,
            metadata={
                "is_demo": True,
                "note": "This is a placeholder image. Configure OpenAI API key for DALL-E image generation."
            },
            created_at=now
        )
        
        return ImageGenerationResponse(
            success=True,
            image=demo_image,
            usage_stats={
                "is_demo": True,
                "cost_estimate": 0.0,
                "message": "This is a demo placeholder. Configure OpenAI API key for real image generation."
            }
        )