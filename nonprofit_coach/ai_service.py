"""
AI Service for Nonprofit Idea Coach
Handles all interactions with Claude API for content generation and follow-up questions.
"""

import anthropic
from typing import Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from search_service import SearchResults, Organization, Grant, Resource


class AIService:
    """Wrapper for Claude API with prompt templates for nonprofit coaching."""
    
    def __init__(self, api_key: str):
        """
        Initialize AI service with Claude API key.
        
        Args:
            api_key: Anthropic API key for Claude
        """
        # Initialize client with minimal configuration to avoid compatibility issues
        self.client = anthropic.Anthropic(
            api_key=api_key,
            max_retries=2
        )
        self.model = "claude-3-haiku-20240307"
        self.max_tokens = 2048
    
    def generate_follow_up_questions(
        self, 
        question_type: str, 
        user_response: str,
        idea_context: Optional[Dict] = None
    ) -> str:
        """
        Generate follow-up questions during the idea development questionnaire.
        
        Args:
            question_type: Type of question (e.g., 'description', 'importance', 'beneficiaries')
            user_response: The user's response to the current question
            idea_context: Optional context from previous responses
            
        Returns:
            AI-generated follow-up question or guidance
        """
        try:
            # Build context from previous responses
            context_str = ""
            if idea_context:
                context_str = f"\n\nPrevious responses:\n"
                for key, value in idea_context.items():
                    if value:
                        context_str += f"- {key}: {value}\n"
            
            system_prompt = self._get_questionnaire_system_prompt()
            user_prompt = f"""The user is answering questions about their nonprofit idea.

Current question type: {question_type}
User's response: {user_response}{context_str}

Based on their response, generate ONE thoughtful follow-up question that:
1. Encourages them to think deeper about this aspect
2. Helps them provide more specific details
3. Is supportive and encouraging
4. Is concise (1-2 sentences max)

If their response is already detailed and complete, respond with "Great! Let's move on." instead of asking another question."""
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            return response.content[0].text.strip()
            
        except anthropic.APIError as e:
            raise AIServiceError(f"Claude API error: {str(e)}")
        except Exception as e:
            raise AIServiceError(f"Unexpected error generating follow-up: {str(e)}")
    
    def generate_section_content(
        self,
        idea_summary: Dict,
        section: str,
        content_type: str,
        chat_context: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate content for a specific section (marketing, team, funding, research).
        
        Args:
            idea_summary: Complete idea information from questionnaire
            section: Section name ('marketing', 'team', 'funding', 'research')
            content_type: Type of content to generate (e.g., 'email', 'flyer', 'grant_proposal')
            chat_context: Optional chat history for iterative refinement
            
        Returns:
            AI-generated content
        """
        try:
            system_prompt = self._get_section_system_prompt(idea_summary, section)
            user_prompt = self._get_content_prompt(section, content_type, chat_context)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            return response.content[0].text.strip()
            
        except anthropic.APIError as e:
            raise AIServiceError(f"Claude API error: {str(e)}")
        except Exception as e:
            raise AIServiceError(f"Unexpected error generating content: {str(e)}")
    
    def generate_section_content_with_search(
        self,
        idea_summary: Dict,
        section: str,
        content_type: str,
        search_results: Optional['SearchResults'] = None,
        chat_context: Optional[List[Dict]] = None
    ) -> str:
        """
        Generate content with search results integrated into the prompt.
        Falls back to standard generation if search_results is None.
        
        Args:
            idea_summary: Complete idea information from questionnaire
            section: Section name ('marketing', 'team', 'funding', 'research')
            content_type: Type of content to generate (e.g., 'email', 'flyer', 'grant_proposal')
            search_results: Optional SearchResults object with web search data
            chat_context: Optional chat history for iterative refinement
            
        Returns:
            AI-generated content enhanced with search results
        """
        # Fall back to standard generation if no search results
        if search_results is None:
            return self.generate_section_content(
                idea_summary, section, content_type, chat_context
            )
        
        try:
            # Use enhanced system prompt with search context
            system_prompt = self._get_enhanced_system_prompt(
                idea_summary, section, search_results
            )
            user_prompt = self._get_content_prompt(section, content_type, chat_context)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            
            return response.content[0].text.strip()
            
        except anthropic.APIError as e:
            raise AIServiceError(f"Claude API error: {str(e)}")
        except Exception as e:
            raise AIServiceError(f"Unexpected error generating content with search: {str(e)}")
    
    def chat_with_context(
        self,
        idea_summary: Dict,
        section: str,
        user_message: str,
        chat_history: Optional[List[Dict]] = None
    ) -> str:
        """
        Handle chat interactions within a section with full idea context.
        
        Args:
            idea_summary: Complete idea information
            section: Current section ('marketing', 'team', 'funding', 'research')
            user_message: User's chat message
            chat_history: Previous chat messages
            
        Returns:
            AI response
        """
        try:
            system_prompt = self._get_section_system_prompt(idea_summary, section)
            
            # Build message history
            messages = []
            if chat_history:
                for msg in chat_history:
                    messages.append({
                        "role": msg.get("role", "user"),
                        "content": msg.get("content", "")
                    })
            
            messages.append({"role": "user", "content": user_message})
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=system_prompt,
                messages=messages
            )
            
            return response.content[0].text.strip()
            
        except anthropic.APIError as e:
            raise AIServiceError(f"Claude API error: {str(e)}")
        except Exception as e:
            raise AIServiceError(f"Unexpected error in chat: {str(e)}")
    
    # ============================================================
    # PROMPT TEMPLATES
    # ============================================================
    
    def _get_questionnaire_system_prompt(self) -> str:
        """System prompt for questionnaire follow-up questions."""
        return """You are a supportive nonprofit coach helping someone develop their cause-based idea into a detailed nonprofit plan.

Your role is to:
- Ask thoughtful follow-up questions that encourage deeper thinking
- Help users articulate their vision clearly
- Be encouraging and supportive
- Keep questions concise and focused
- Guide them to provide specific, actionable details

Remember: You're helping them refine their idea, not judging it."""
    
    def _get_section_system_prompt(self, idea_summary: Dict, section: str) -> str:
        """System prompt that includes idea context for section work."""
        idea_context = f"""You are an AI assistant helping with a nonprofit organization.

NONPROFIT IDEA DETAILS:
- Title: {idea_summary.get('title', 'Untitled')}
- Description: {idea_summary.get('description', 'N/A')}
- Why it matters: {idea_summary.get('importance', 'N/A')}
- Target beneficiaries: {idea_summary.get('beneficiaries', 'N/A')}
- Implementation approach: {idea_summary.get('implementation', 'N/A')}
- Significance: {idea_summary.get('significance', 'N/A')}
- What makes it unique: {idea_summary.get('uniqueness', 'N/A')}
- Operating location: {idea_summary.get('location', 'N/A')}

CURRENT SECTION: {section.upper()}
"""
        
        section_guidance = {
            'marketing': """
Your role: Help create compelling marketing materials (emails, flyers, social posts, ads) that communicate the nonprofit's mission and inspire action.

Guidelines:
- Use clear, compelling language
- Focus on the impact and beneficiaries
- Include clear calls-to-action
- Keep tone professional yet warm
- Tailor content to the specific format requested""",
            
            'team': """
Your role: Help with team building, volunteer recruitment, and organizational structure.

Guidelines:
- Create compelling recruitment materials
- Suggest appropriate roles and responsibilities
- Provide hiring guidance and job descriptions
- Focus on the skills and passion needed
- Emphasize the impact volunteers will make""",
            
            'funding': """
Your role: Help develop funding strategies, grant proposals, and donor communications.

Guidelines:
- Identify appropriate funding sources
- Create persuasive grant proposals
- Draft compelling donor communications
- Provide realistic cost estimates
- Focus on sustainability and impact""",
            
            'research': """
Your role: Help with implementation planning and research.

Guidelines:
- Provide detailed, actionable implementation steps
- Identify relevant local organizations and resources
- Suggest practical next steps
- Focus on realistic, achievable goals
- Provide links and references when helpful"""
        }
        
        return idea_context + section_guidance.get(section, "")
    
    def _get_enhanced_system_prompt(
        self, 
        idea_summary: Dict, 
        section: str,
        search_results: 'SearchResults'
    ) -> str:
        """
        Create enhanced system prompt with search results context.
        
        Args:
            idea_summary: Complete idea information
            section: Current section name
            search_results: SearchResults object with web search data
            
        Returns:
            Enhanced system prompt with search context and formatting instructions
        """
        base_prompt = self._get_section_system_prompt(idea_summary, section)
        
        # Format search results for inclusion in prompt
        search_context = self._format_search_results_for_prompt(search_results)
        
        enhanced_section = f"""

SEARCH RESULTS:
You have access to current web search results to provide accurate, up-to-date information.

{search_context}

FORMATTING REQUIREMENTS:
- Use HTML tables for comparative data (organizations, grants, tools, resources)
- Make all URLs clickable with <a href="URL" target="_blank">descriptive text</a>
- Include citations at the end with [1], [2], etc. markers linking to sources
- Use <ul> and <ol> for lists
- Use <strong> for emphasis
- Use <table>, <thead>, <tbody>, <tr>, <th>, <td> for tables
- Add CSS class "search-results-table" to tables for styling

TABLE FORMAT EXAMPLE:
<table class="search-results-table">
  <thead>
    <tr>
      <th>Name</th>
      <th>Description</th>
      <th>Website</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Organization Name</td>
      <td>Brief description</td>
      <td><a href="https://example.com" target="_blank">Visit Website</a></td>
    </tr>
  </tbody>
</table>

IMPORTANT INSTRUCTIONS:
- Base your response on the search results provided above
- Include specific names, URLs, and details from the search results
- Do not make up information - use only what's in the search results
- If search results are limited, acknowledge this and supplement with general guidance
- Always make URLs clickable and properly formatted
- Present comparative information in tables for easy scanning
"""
        
        return base_prompt + enhanced_section
    
    def _format_search_results_for_prompt(self, search_results: 'SearchResults') -> str:
        """
        Format search results into a readable string for the AI prompt.
        
        Args:
            search_results: SearchResults object
            
        Returns:
            Formatted string with search results
        """
        if not search_results or not search_results.results:
            return "No search results available."
        
        formatted = f"Query: {search_results.query}\n"
        formatted += f"Total Results: {search_results.total_results}\n\n"
        
        for idx, result in enumerate(search_results.results, 1):
            formatted += f"[{idx}] {result.title}\n"
            formatted += f"    URL: {result.url}\n"
            formatted += f"    Domain: {result.domain}\n"
            formatted += f"    Snippet: {result.snippet}\n"
            if result.relevance_score:
                formatted += f"    Relevance: {result.relevance_score}\n"
            formatted += "\n"
        
        return formatted
    
    def _get_content_prompt(
        self, 
        section: str, 
        content_type: str,
        chat_context: Optional[List[Dict]] = None
    ) -> str:
        """Generate specific prompt for content type with HTML formatting instructions."""
        
        # Content type specific prompts with HTML formatting guidance
        prompts = {
            # Marketing section
            'email': "Create a compelling email template for this nonprofit. Include a subject line, greeting, body with clear call-to-action, and closing. Keep it concise (300-400 words). Use HTML formatting with <p> tags for paragraphs and <a> tags for any links.",
            'flyer': "Create content for a flyer about this nonprofit. Include a catchy headline, key points about the cause, impact statement, and how people can get involved. Format with clear sections using HTML headings (<h3>, <h4>) and lists (<ul>, <ol>).",
            'social_post': "Create 3 social media posts (one for each: Twitter/X, Facebook, Instagram) promoting this nonprofit. Make them engaging, shareable, and include relevant hashtags. Format each post clearly with line breaks.",
            'advertisement': "Create advertisement copy for this nonprofit. Include a headline, body copy, and call-to-action. Make it compelling and concise (150-200 words). Use HTML formatting with <strong> for emphasis.",
            
            # Team section
            'recruiting_pitch': "Create a compelling volunteer recruitment pitch. Explain why people should join, what they'll do, and the impact they'll make. Keep it inspiring and specific (200-300 words). Use HTML formatting with <p> tags and <ul> for bullet points. Include clickable links with <a> tags for any resources or sign-up pages.",
            'job_description': "Create a job description for a key role in this nonprofit. Include role title, responsibilities, qualifications, and what makes this opportunity special. Use HTML formatting with <h3> for sections, <ul> for lists, and <strong> for emphasis.",
            'volunteer_form': "Create a simple volunteer sign-up form structure. List the fields needed to collect volunteer information and their availability. Format as an HTML list with field names and types.",
            
            # Funding section
            'grant_proposal': "Create a grant proposal outline for this nonprofit. Include: Executive Summary, Problem Statement, Proposed Solution, Budget Overview, and Expected Impact. Be specific and compelling. If search results include grant opportunities, present them in an HTML table with columns for Grant Name, Funder, Amount, Deadline, and Application Link. Use <a> tags for all URLs.",
            'donor_letter': "Write a letter to potential donors. Explain the cause, why it matters, how their donation will help, and include a clear ask. Keep it personal and compelling (300-400 words). Use HTML formatting with <p> tags for paragraphs.",
            'budget_plan': "Create a basic budget plan for this nonprofit. Include startup costs, ongoing operational expenses, and funding needs. Provide realistic estimates with explanations. Present the budget as an HTML table with columns for Category, Item, Cost, and Notes. Use proper <table>, <thead>, <tbody> structure.",
            
            # Research section
            'implementation_steps': "Create a detailed, step-by-step implementation plan for this nonprofit. Include 10-15 specific, actionable steps in chronological order. Be practical and realistic. Format as an ordered list (<ol>) with each step clearly numbered. If search results include relevant tools or platforms, present them in an HTML table and include clickable links with <a> tags.",
            'local_orgs': "Identify specific local organizations, community groups, and resources in the operating location that could help or partner with this nonprofit. If search results are available, present them in an HTML table with columns for Organization Name, Description, Website, and How They Can Help. Use <a href='URL' target='_blank'>Visit Website</a> format for all links. Include at least 5-10 organizations. Add a citations section at the end with numbered references [1], [2], etc.",
            'resources': "Provide a list of helpful resources for starting this nonprofit. Include websites, tools, organizations, and guides that would be valuable. If search results are available, present them in an HTML table with columns for Resource Name, Description, Type (tool/guide/platform), and Link. Use <a href='URL' target='_blank'>descriptive text</a> format for all links. Include citations at the end."
        }
        
        base_prompt = prompts.get(content_type, f"Create {content_type} content for this nonprofit. Use proper HTML formatting with tables for structured data, <a> tags for clickable links, and appropriate semantic HTML elements.")
        
        # Add chat context if provided
        if chat_context:
            context_str = "\n\nPrevious conversation:\n"
            for msg in chat_context[-3:]:  # Last 3 messages for context
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                context_str += f"{role}: {content}\n"
            base_prompt += context_str + "\n\nPlease refine or adjust the content based on the conversation above. Maintain HTML formatting in your response."
        
        return base_prompt


class AIServiceError(Exception):
    """Custom exception for AI service errors."""
    pass


# ============================================================
# HELPER FUNCTIONS FOR FLASK ROUTES
# ============================================================

def create_ai_service(api_key: str) -> AIService:
    """
    Factory function to create AI service instance.
    
    Args:
        api_key: Anthropic API key
        
    Returns:
        Configured AIService instance
    """
    if not api_key:
        raise AIServiceError("API key is required")
    
    return AIService(api_key)
