from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
from enum import Enum


class ContentType(str, Enum):
    """Types of content that can be generated."""
    FLYER = "flyer"
    EMAIL_TEMPLATE = "email_template"
    POSTER = "poster"
    ADVERTISEMENT = "advertisement"
    VOLUNTEER_PITCH = "volunteer_pitch"
    TASK_ASSIGNMENT = "task_assignment"
    JOB_DESCRIPTION = "job_description"
    FUNDING_STRATEGY = "funding_strategy"
    GRANT_PROPOSAL = "grant_proposal"
    COST_ESTIMATE = "cost_estimate"
    LOCAL_RESEARCH = "local_research"
    IMPLEMENTATION_GUIDE = "implementation_guide"


class IdeaSummary(BaseModel):
    """Summary of a user's nonprofit idea from the questionnaire."""
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    user_id: str
    cause_area: str
    mission_statement: str
    target_audience: str
    geographic_scope: str
    activities: List[str]
    goals: List[str]
    resources_needed: List[str]
    timeline: str
    budget_range: Optional[str] = None
    experience_level: str
    created_at: datetime


class ContentRequest(BaseModel):
    """Request for AI-generated content."""
    user_id: str
    content_type: ContentType
    idea_summary: IdeaSummary
    additional_context: Optional[Dict[str, Any]] = None
    custom_instructions: Optional[str] = None


class GeneratedContent(BaseModel):
    """AI-generated content response."""
    model_config = ConfigDict(json_encoders={datetime: lambda v: v.isoformat()})
    
    content_id: str
    user_id: str
    content_type: ContentType
    title: str
    content: str
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime


class ContentGenerationResponse(BaseModel):
    """Response from content generation API."""
    success: bool
    content: Optional[GeneratedContent] = None
    error_message: Optional[str] = None
    usage_stats: Optional[Dict[str, Any]] = None