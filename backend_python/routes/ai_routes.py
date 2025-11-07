from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.ai_service import AIService
from services.auth_service import AuthService
from models.ai_content import (
    ContentRequest, ContentGenerationResponse, ContentType, IdeaSummary
)

router = APIRouter(prefix="/ai", tags=["ai-content"])
security = HTTPBearer()
ai_service = AIService()


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


@router.post("/generate", response_model=ContentGenerationResponse)
async def generate_content(
    request: ContentRequest,
    current_user_id: str = Depends(get_current_user)
):
    """Generate AI content based on the user's nonprofit idea."""
    try:
        # Ensure the request is for the authenticated user
        if request.user_id != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "code": "AUTHORIZATION_ERROR",
                    "message": "You can only generate content for your own account",
                    "timestamp": datetime.utcnow().isoformat()
                }
            )
        
        # Generate content
        response = await ai_service.generate_content(request)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SERVER_ERROR",
                "message": f"Content generation failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.get("/content-types")
async def get_content_types():
    """Get available content types for generation."""
    return {
        "content_types": [
            {
                "type": ContentType.FLYER,
                "name": "Flyer",
                "description": "Compelling flyer content for your cause",
                "category": "marketing"
            },
            {
                "type": ContentType.EMAIL_TEMPLATE,
                "name": "Email Template",
                "description": "Professional email templates for outreach",
                "category": "marketing"
            },
            {
                "type": ContentType.POSTER,
                "name": "Poster",
                "description": "Poster concepts with strong messaging",
                "category": "marketing"
            },
            {
                "type": ContentType.ADVERTISEMENT,
                "name": "Advertisement",
                "description": "Ad copy for various platforms",
                "category": "marketing"
            },
            {
                "type": ContentType.VOLUNTEER_PITCH,
                "name": "Volunteer Pitch",
                "description": "Compelling volunteer recruitment content",
                "category": "team_building"
            },
            {
                "type": ContentType.TASK_ASSIGNMENT,
                "name": "Task Assignment",
                "description": "Organizational structure and task suggestions",
                "category": "team_building"
            },
            {
                "type": ContentType.JOB_DESCRIPTION,
                "name": "Job Description",
                "description": "Professional job descriptions for key roles",
                "category": "team_building"
            },
            {
                "type": ContentType.FUNDING_STRATEGY,
                "name": "Funding Strategy",
                "description": "Strategic funding advice and opportunities",
                "category": "funding"
            },
            {
                "type": ContentType.GRANT_PROPOSAL,
                "name": "Grant Proposal",
                "description": "Grant proposal templates and donor communications",
                "category": "funding"
            },
            {
                "type": ContentType.COST_ESTIMATE,
                "name": "Cost Estimate",
                "description": "Budget planning and cost estimates",
                "category": "funding"
            },
            {
                "type": ContentType.LOCAL_RESEARCH,
                "name": "Local Research",
                "description": "Local organizations and resources research",
                "category": "research"
            },
            {
                "type": ContentType.IMPLEMENTATION_GUIDE,
                "name": "Implementation Guide",
                "description": "Step-by-step implementation guidance",
                "category": "research"
            }
        ],
        "categories": {
            "marketing": "Marketing Materials",
            "team_building": "Team Building",
            "funding": "Funding & Finance",
            "research": "Research & Planning"
        }
    }


@router.get("/suggestions/{cause_area}")
async def get_content_suggestions(
    cause_area: str,
    current_user_id: str = Depends(get_current_user)
):
    """Get content suggestions based on cause area."""
    try:
        suggestions = await ai_service.get_content_suggestions(cause_area)
        return suggestions
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SERVER_ERROR",
                "message": f"Failed to get suggestions: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )


@router.post("/demo/generate", response_model=ContentGenerationResponse)
async def generate_demo_content(content_type: ContentType):
    """Generate demo content without authentication (for testing)."""
    try:
        # Create a demo idea summary
        demo_idea = IdeaSummary(
            user_id="demo-user",
            cause_area="Environmental Conservation",
            mission_statement="To protect local wildlife and promote sustainable living in our community",
            target_audience="Local community members, families, and environmental enthusiasts",
            geographic_scope="Local city and surrounding areas",
            activities=["Community cleanups", "Educational workshops", "Tree planting events"],
            goals=["Reduce local pollution", "Educate 500 people annually", "Plant 1000 trees"],
            resources_needed=["Volunteers", "Cleaning supplies", "Educational materials"],
            timeline="6 months to launch, ongoing operations",
            budget_range="$5,000 - $15,000 annually",
            experience_level="Beginner",
            created_at=datetime.utcnow()
        )
        
        # Create demo request
        demo_request = ContentRequest(
            user_id="demo-user",
            content_type=content_type,
            idea_summary=demo_idea,
            custom_instructions="This is a demo generation for testing purposes."
        )
        
        # Generate content
        response = await ai_service.generate_content(demo_request)
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "code": "SERVER_ERROR",
                "message": f"Demo content generation failed: {str(e)}",
                "timestamp": datetime.utcnow().isoformat()
            }
        )