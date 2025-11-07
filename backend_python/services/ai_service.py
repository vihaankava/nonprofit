import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from uuid import uuid4
import openai
from models.ai_content import (
    ContentType, IdeaSummary, ContentRequest, 
    GeneratedContent, ContentGenerationResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI Configuration
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_MAX_TOKENS = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))


class ContentTemplates:
    """Templates for different types of content generation."""
    
    @staticmethod
    def get_system_prompt(content_type: ContentType) -> str:
        """Get the system prompt for a specific content type."""
        base_prompt = """You are an expert nonprofit consultant and content creator. 
        You help people start and run successful nonprofit organizations. 
        Create professional, engaging, and actionable content based on the user's nonprofit idea."""
        
        type_specific = {
            ContentType.FLYER: "Focus on creating compelling flyer content that attracts attention and clearly communicates the cause.",
            ContentType.EMAIL_TEMPLATE: "Create professional email templates that can be customized for different audiences.",
            ContentType.POSTER: "Design poster concepts with strong visual messaging and clear calls to action.",
            ContentType.ADVERTISEMENT: "Write advertisement copy that's suitable for various platforms (social media, print, etc.).",
            ContentType.VOLUNTEER_PITCH: "Create compelling volunteer recruitment content that motivates people to get involved.",
            ContentType.TASK_ASSIGNMENT: "Suggest practical task assignments and organizational structure for volunteers.",
            ContentType.JOB_DESCRIPTION: "Write professional job descriptions for key nonprofit roles.",
            ContentType.FUNDING_STRATEGY: "Provide strategic funding advice and identify potential funding sources.",
            ContentType.GRANT_PROPOSAL: "Create grant proposal templates and donor communication materials.",
            ContentType.COST_ESTIMATE: "Provide realistic cost estimates and budget planning guidance.",
            ContentType.LOCAL_RESEARCH: "Research and identify relevant local organizations and resources.",
            ContentType.IMPLEMENTATION_GUIDE: "Provide step-by-step implementation guidance and best practices."
        }
        
        return f"{base_prompt}\n\n{type_specific.get(content_type, '')}"
    
    @staticmethod
    def get_user_prompt(content_type: ContentType, idea_summary: IdeaSummary, 
                       additional_context: Optional[Dict[str, Any]] = None,
                       custom_instructions: Optional[str] = None) -> str:
        """Generate the user prompt based on content type and idea summary."""
        
        base_context = f"""
        Nonprofit Idea Details:
        - Cause Area: {idea_summary.cause_area}
        - Mission: {idea_summary.mission_statement}
        - Target Audience: {idea_summary.target_audience}
        - Geographic Scope: {idea_summary.geographic_scope}
        - Planned Activities: {', '.join(idea_summary.activities)}
        - Goals: {', '.join(idea_summary.goals)}
        - Resources Needed: {', '.join(idea_summary.resources_needed)}
        - Timeline: {idea_summary.timeline}
        - Budget Range: {idea_summary.budget_range or 'Not specified'}
        - Experience Level: {idea_summary.experience_level}
        """
        
        if additional_context:
            base_context += f"\n\nAdditional Context: {additional_context}"
        
        if custom_instructions:
            base_context += f"\n\nSpecial Instructions: {custom_instructions}"
        
        content_requests = {
            ContentType.FLYER: f"{base_context}\n\nCreate compelling flyer content for this nonprofit. Include a catchy headline, key messaging, and a clear call to action.",
            
            ContentType.EMAIL_TEMPLATE: f"{base_context}\n\nCreate a professional email template that can be used for outreach. Include subject line suggestions and customizable sections.",
            
            ContentType.POSTER: f"{base_context}\n\nCreate poster concept with strong messaging. Include headline, key points, visual suggestions, and call to action.",
            
            ContentType.ADVERTISEMENT: f"{base_context}\n\nWrite advertisement copy suitable for social media and other platforms. Include multiple versions for different platforms.",
            
            ContentType.VOLUNTEER_PITCH: f"{base_context}\n\nCreate a compelling volunteer recruitment pitch. Explain why people should get involved and what they can contribute.",
            
            ContentType.TASK_ASSIGNMENT: f"{base_context}\n\nSuggest specific task assignments and organizational structure for volunteers based on the planned activities.",
            
            ContentType.JOB_DESCRIPTION: f"{base_context}\n\nWrite job descriptions for key roles this nonprofit will need. Include responsibilities, qualifications, and expectations.",
            
            ContentType.FUNDING_STRATEGY: f"{base_context}\n\nProvide a funding strategy with specific funding sources, grant opportunities, and fundraising ideas suitable for this cause.",
            
            ContentType.GRANT_PROPOSAL: f"{base_context}\n\nCreate a grant proposal template and donor communication materials tailored to this nonprofit's mission and needs.",
            
            ContentType.COST_ESTIMATE: f"{base_context}\n\nProvide realistic cost estimates for implementing this nonprofit, including startup costs, ongoing expenses, and budget planning advice.",
            
            ContentType.LOCAL_RESEARCH: f"{base_context}\n\nResearch and identify local organizations, resources, and partnerships relevant to this cause in the specified geographic area.",
            
            ContentType.IMPLEMENTATION_GUIDE: f"{base_context}\n\nProvide a step-by-step implementation guide including legal requirements, best practices, and practical next steps."
        }
        
        return content_requests.get(content_type, f"{base_context}\n\nGenerate relevant content for this nonprofit idea.")


class AIService:
    """Service for AI-powered content generation."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        self.templates = ContentTemplates()
        
        # Only initialize OpenAI client if API key is properly set
        if self.api_key and self.api_key != "your-openai-api-key-here":
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                self.client = None
    
    async def generate_content(self, request: ContentRequest) -> ContentGenerationResponse:
        """Generate content using OpenAI API or demo content."""
        try:
            # Check if OpenAI client is available
            if not self.client:
                return self._generate_demo_content(request)
            
            # Get prompts
            system_prompt = self.templates.get_system_prompt(request.content_type)
            user_prompt = self.templates.get_user_prompt(
                request.content_type, 
                request.idea_summary,
                request.additional_context,
                request.custom_instructions
            )
            
            logger.info(f"Generating {request.content_type} content for user {request.user_id}")
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=OPENAI_MAX_TOKENS,
                temperature=OPENAI_TEMPERATURE
            )
            
            # Extract generated content
            generated_text = response.choices[0].message.content
            
            # Create content object
            now = datetime.utcnow()
            content = GeneratedContent(
                content_id=str(uuid4()),
                user_id=request.user_id,
                content_type=request.content_type,
                title=self._generate_title(request.content_type, request.idea_summary),
                content=generated_text,
                metadata={
                    "model": OPENAI_MODEL,
                    "tokens_used": response.usage.total_tokens,
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens
                },
                created_at=now,
                updated_at=now
            )
            
            return ContentGenerationResponse(
                success=True,
                content=content,
                usage_stats={
                    "tokens_used": response.usage.total_tokens,
                    "cost_estimate": self._estimate_cost(response.usage.total_tokens)
                }
            )
            
        except Exception as e:
            logger.error(f"Error generating content: {str(e)}")
            return ContentGenerationResponse(
                success=False,
                error_message=f"Content generation failed: {str(e)}"
            )
    
    def _generate_demo_content(self, request: ContentRequest) -> ContentGenerationResponse:
        """Generate demo content when OpenAI API is not available."""
        demo_content = {
            ContentType.FLYER: f"""
# Join Our Mission: {request.idea_summary.cause_area}

## {request.idea_summary.mission_statement}

**Who We Serve:** {request.idea_summary.target_audience}
**Where We Work:** {request.idea_summary.geographic_scope}

### What We Do:
{chr(10).join(f"• {activity}" for activity in request.idea_summary.activities)}

### Our Goals:
{chr(10).join(f"• {goal}" for goal in request.idea_summary.goals)}

**Get Involved Today!**
Together, we can make a difference in our community.

*Contact us to learn more about volunteer opportunities.*

---
*This is demo content. Configure OpenAI API key for AI-generated content.*
            """,
            
            ContentType.EMAIL_TEMPLATE: f"""
Subject: Join Us in Making a Difference - {request.idea_summary.cause_area}

Dear [Name],

I hope this email finds you well. I'm reaching out to share an exciting opportunity to make a positive impact in our community.

**About Our Mission:**
{request.idea_summary.mission_statement}

**What We're Doing:**
{chr(10).join(f"• {activity}" for activity in request.idea_summary.activities)}

**How You Can Help:**
We're looking for passionate individuals like you to join our cause. Whether you have 2 hours or 20 hours to spare, there's a way for you to contribute.

**Next Steps:**
Reply to this email or visit our website to learn more about volunteer opportunities.

Thank you for considering joining our mission!

Best regards,
[Your Name]
[Organization Name]

---
*This is demo content. Configure OpenAI API key for AI-generated content.*
            """,
            
            ContentType.VOLUNTEER_PITCH: f"""
# Make a Real Difference: Volunteer with {request.idea_summary.cause_area}

**Why Your Help Matters:**
{request.idea_summary.mission_statement}

**What You'll Be Doing:**
{chr(10).join(f"• {activity}" for activity in request.idea_summary.activities)}

**What We're Looking For:**
• Passionate individuals who care about {request.idea_summary.cause_area.lower()}
• People who want to make a tangible impact in {request.idea_summary.geographic_scope}
• Team players who are ready to contribute their skills and time

**What You'll Gain:**
• Experience working on meaningful projects
• Skills in nonprofit operations and community organizing
• A network of like-minded individuals
• The satisfaction of making a real difference

**Time Commitment:** Flexible - we work with your schedule
**Experience Required:** None - we'll train you!

Ready to join us? Contact us today!

---
*This is demo content. Configure OpenAI API key for AI-generated content.*
            """
        }
        
        # Get demo content or create generic content
        content_text = demo_content.get(request.content_type, f"""
# {request.content_type.value.replace('_', ' ').title()} for {request.idea_summary.cause_area}

**Mission:** {request.idea_summary.mission_statement}

**Target Audience:** {request.idea_summary.target_audience}

**Activities:**
{chr(10).join(f"• {activity}" for activity in request.idea_summary.activities)}

**Goals:**
{chr(10).join(f"• {goal}" for goal in request.idea_summary.goals)}

---
*This is demo content. Configure OpenAI API key for AI-generated content.*
        """)
        
        # Create content object
        now = datetime.utcnow()
        content = GeneratedContent(
            content_id=str(uuid4()),
            user_id=request.user_id,
            content_type=request.content_type,
            title=f"[DEMO] {self._generate_title(request.content_type, request.idea_summary)}",
            content=content_text.strip(),
            metadata={
                "model": "demo",
                "tokens_used": 0,
                "is_demo": True
            },
            created_at=now,
            updated_at=now
        )
        
        return ContentGenerationResponse(
            success=True,
            content=content,
            usage_stats={
                "tokens_used": 0,
                "cost_estimate": 0.0,
                "is_demo": True,
                "message": "This is demo content. Configure OpenAI API key for AI-generated content."
            }
        )
    
    def _generate_title(self, content_type: ContentType, idea_summary: IdeaSummary) -> str:
        """Generate a title for the content based on type and idea."""
        titles = {
            ContentType.FLYER: f"Flyer for {idea_summary.cause_area}",
            ContentType.EMAIL_TEMPLATE: f"Email Template - {idea_summary.cause_area}",
            ContentType.POSTER: f"Poster Design - {idea_summary.cause_area}",
            ContentType.ADVERTISEMENT: f"Advertisement Copy - {idea_summary.cause_area}",
            ContentType.VOLUNTEER_PITCH: f"Volunteer Recruitment - {idea_summary.cause_area}",
            ContentType.TASK_ASSIGNMENT: f"Task Organization - {idea_summary.cause_area}",
            ContentType.JOB_DESCRIPTION: f"Job Descriptions - {idea_summary.cause_area}",
            ContentType.FUNDING_STRATEGY: f"Funding Strategy - {idea_summary.cause_area}",
            ContentType.GRANT_PROPOSAL: f"Grant Proposal - {idea_summary.cause_area}",
            ContentType.COST_ESTIMATE: f"Cost Estimates - {idea_summary.cause_area}",
            ContentType.LOCAL_RESEARCH: f"Local Research - {idea_summary.cause_area}",
            ContentType.IMPLEMENTATION_GUIDE: f"Implementation Guide - {idea_summary.cause_area}"
        }
        return titles.get(content_type, f"Content for {idea_summary.cause_area}")
    
    def _estimate_cost(self, tokens_used: int) -> float:
        """Estimate the cost of the API call based on tokens used."""
        # GPT-3.5-turbo pricing (approximate)
        cost_per_1k_tokens = 0.002  # $0.002 per 1K tokens
        return (tokens_used / 1000) * cost_per_1k_tokens
    
    async def get_content_suggestions(self, cause_area: str) -> Dict[str, Any]:
        """Get content type suggestions based on cause area."""
        suggestions = {
            "marketing": [ContentType.FLYER, ContentType.EMAIL_TEMPLATE, ContentType.POSTER, ContentType.ADVERTISEMENT],
            "team_building": [ContentType.VOLUNTEER_PITCH, ContentType.TASK_ASSIGNMENT, ContentType.JOB_DESCRIPTION],
            "funding": [ContentType.FUNDING_STRATEGY, ContentType.GRANT_PROPOSAL, ContentType.COST_ESTIMATE],
            "research": [ContentType.LOCAL_RESEARCH, ContentType.IMPLEMENTATION_GUIDE]
        }
        
        return {
            "cause_area": cause_area,
            "suggested_content_types": suggestions,
            "recommended_order": [
                "research",  # Start with research
                "funding",   # Then funding strategy
                "team_building",  # Build the team
                "marketing"  # Finally, marketing materials
            ]
        }