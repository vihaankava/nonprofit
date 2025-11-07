import os
import re
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from uuid import uuid4
import openai
from models.chat import (
    ChatRequest, ChatResponse, ChatMessage, MessageRole, 
    GeneratedMaterial, ConversationHistory
)
from models.image_generation import ImageRequest, ImageType, ImageStyle
from services.image_service import ImageService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChatService:
    """Conversational AI service for nonprofit assistance."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = None
        self.conversations: Dict[str, ConversationHistory] = {}
        self.image_service = ImageService()
        
        # Only initialize OpenAI client if API key is properly set
        if self.api_key and self.api_key != "your-openai-api-key-here":
            try:
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
                self.client = None
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the nonprofit assistant."""
        return """You are an expert nonprofit consultant and creative assistant. You help people:

1. Answer questions about starting and running nonprofits
2. Create custom marketing materials (flyers, posters, emails, etc.)
3. Provide strategic advice for nonprofit operations
4. Generate content tailored to specific causes and audiences

When users ask for materials like flyers, posters, or emails, you should:
- Create professional, compelling content
- Include specific formatting instructions
- Make it actionable and engaging
- Tailor it to their specific cause and audience

When users ask questions, provide helpful, practical advice based on nonprofit best practices.

If a user asks for multiple materials or has complex requests, break them down and provide each material separately.

Format your responses clearly and include material generation when requested."""
    
    async def chat(self, request: ChatRequest) -> ChatResponse:
        """Process a chat message and generate response."""
        try:
            # Get or create conversation
            conversation_id = request.conversation_id or str(uuid4())
            conversation = self.conversations.get(conversation_id)
            
            if not conversation:
                conversation = ConversationHistory(
                    conversation_id=conversation_id,
                    user_id=request.user_id,
                    messages=[],
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                self.conversations[conversation_id] = conversation
            
            # Add user message to conversation
            user_message = ChatMessage(
                role=MessageRole.USER,
                content=request.message,
                timestamp=datetime.utcnow(),
                metadata=request.context
            )
            conversation.messages.append(user_message)
            
            # Generate AI response
            if self.client:
                response = await self._generate_ai_response(conversation, request)
            else:
                response = await self._generate_demo_response(conversation, request)
            
            # Add assistant message to conversation
            assistant_message = ChatMessage(
                role=MessageRole.ASSISTANT,
                content=response["content"],
                timestamp=datetime.utcnow(),
                metadata=response.get("metadata")
            )
            conversation.messages.append(assistant_message)
            conversation.updated_at = datetime.utcnow()
            
            # Create chat response
            chat_response = ChatResponse(
                conversation_id=conversation_id,
                message=assistant_message,
                generated_materials=response.get("materials", []),
                suggestions=response.get("suggestions", []),
                timestamp=datetime.utcnow()
            )
            
            # Add generated images to metadata if any
            if response.get("images"):
                chat_response.message.metadata = chat_response.message.metadata or {}
                chat_response.message.metadata["generated_images"] = response["images"]
            
            return chat_response
            
        except Exception as e:
            logger.error(f"Error in chat service: {str(e)}")
            # Return error response
            error_message = ChatMessage(
                role=MessageRole.ASSISTANT,
                content=f"I apologize, but I encountered an error: {str(e)}. Please try again.",
                timestamp=datetime.utcnow()
            )
            
            return ChatResponse(
                conversation_id=request.conversation_id or str(uuid4()),
                message=error_message,
                timestamp=datetime.utcnow()
            )
    
    async def _generate_ai_response(self, conversation: ConversationHistory, request: ChatRequest) -> Dict[str, Any]:
        """Generate AI response using OpenAI."""
        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": self.get_system_prompt()}
        ]
        
        # Add conversation history (last 10 messages to stay within token limits)
        recent_messages = conversation.messages[-10:]
        for msg in recent_messages:
            messages.append({
                "role": msg.role.value,
                "content": msg.content
            })
        
        # Call OpenAI API
        response = self.client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            messages=messages,
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "2000")),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        )
        
        content = response.choices[0].message.content
        
        # Extract materials if any were generated
        materials = self._extract_materials(content, request.message)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(request.message, content)
        
        return {
            "content": content,
            "materials": materials,
            "suggestions": suggestions,
            "metadata": {
                "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
                "tokens_used": response.usage.total_tokens
            }
        }
    
    async def _generate_demo_response(self, conversation: ConversationHistory, request: ChatRequest) -> Dict[str, Any]:
        """Generate demo response when OpenAI is not available."""
        user_message = request.message.lower()
        
        # Check if user is asking for materials
        materials = []
        images = []
        
        # Check for image generation requests
        if any(word in user_message for word in ["poster", "flyer", "banner", "logo", "graphic", "image", "design"]):
            image_request = await self._create_image_request(request)
            if image_request:
                image_response = await self.image_service.generate_image(image_request)
                if image_response.success and image_response.image:
                    images.append(image_response.image)
        
        # Check for text materials
        if any(word in user_message for word in ["email", "brochure", "template", "letter"]):
            materials = self._generate_demo_materials(request.message)
        
        # Generate contextual response based on what was requested
        if images and len(images) > 0:
            # If we generated an image, create a specific response
            image = images[0]
            content = f"""Perfect! I've created a custom {image.image_type} for you! 🎨

**Your Generated {image.image_type.title()}:**
• **Title:** {image.title}
• **Style:** {image.style.value.title()}
• **Description:** {image.description}

**Usage Tips:**
- High resolution design ready for professional use
- Perfect for printing or digital sharing
- Customize with your specific text and branding
- Great for social media, websites, or print materials

What other designs would you like me to create?"""
        
        elif "flyer" in user_message:
            content = """I'd be happy to help you create a flyer! Here's a custom flyer based on your request:

**Design Tips for Your Flyer:**
- Use bold, eye-catching headlines
- Include your mission statement prominently
- Add clear contact information
- Use high-contrast colors for readability
- Include a strong call-to-action

Would you like me to create any other materials like posters or email templates?"""
        
        elif "poster" in user_message:
            content = """Great! I'll create a poster design for you. Here's your custom poster:

**Poster Design Guidelines:**
- Make the headline large and bold
- Use compelling imagery or graphics
- Keep text minimal but impactful
- Include event details if applicable
- Add QR codes for easy contact

What other materials would you like me to create?"""
        
        elif "email" in user_message:
            content = """Perfect! I'll create a professional email template for you:

**Email Best Practices:**
- Write compelling subject lines
- Personalize the greeting
- Keep paragraphs short and scannable
- Include clear calls-to-action
- Add your contact signature

Would you like me to create additional outreach materials?"""
        
        elif any(word in user_message for word in ["banner", "logo", "graphic", "social"]):
            content = f"""I'll create that design for you! 🎨

Based on your request for "{request.message}", I'm generating a custom design that will be perfect for your nonprofit.

**What I'm Creating:**
- Professional quality design
- Optimized for your specific use case
- Ready for both digital and print use
- Tailored to nonprofit best practices

The design will appear above once it's generated. What other materials can I help you create?"""

        elif any(word in user_message for word in ["volunteer", "recruitment", "recruit"]):
            content = """Great! Volunteer recruitment is crucial for nonprofits. I'll help you create compelling materials to attract volunteers.

**Volunteer Recruitment Tips:**
- Highlight the impact volunteers will make
- Be specific about time commitments
- Show the community and connection aspect
- Include clear next steps for getting involved

What type of volunteer recruitment material would you like me to create? A poster, flyer, or social media graphic?"""

        elif any(word in user_message for word in ["fundraising", "donation", "donor", "funding"]):
            content = """Fundraising materials are essential for nonprofit success! I can help you create compelling content that motivates people to donate.

**Effective Fundraising Design Elements:**
- Clear impact statements
- Compelling visuals that tell your story
- Specific donation amounts and what they accomplish
- Easy ways for people to contribute

What fundraising material would you like me to create? A flyer, poster, or social media campaign graphic?"""

        elif any(word in user_message for word in ["event", "cleanup", "workshop", "meeting"]):
            content = """Event promotion is key to getting people involved! I'll help you create eye-catching materials that drive attendance.

**Event Promotion Best Practices:**
- Clear date, time, and location
- Compelling reason to attend
- What to expect or bring
- Contact information for questions

What type of event promotional material do you need? A poster, flyer, or social media graphic?"""

        elif any(word in user_message for word in ["help", "start", "nonprofit", "organization"]):
            content = """I'm here to help you with your nonprofit! I can assist you with:

🎨 **Creating Materials:**
- Custom flyers and posters
- Professional email templates
- Social media content
- Volunteer recruitment materials

💡 **Strategic Advice:**
- Nonprofit startup guidance
- Fundraising strategies
- Volunteer management
- Legal requirements

📋 **Planning Tools:**
- Budget templates
- Task organization
- Implementation guides

What specific help do you need today? Just ask me to create any materials or answer questions about nonprofit management!"""
        
        else:
            content = """I'm your nonprofit assistant! I can help you with:

- **Creating custom materials** (flyers, posters, emails, brochures)
- **Answering questions** about nonprofit management
- **Providing strategic advice** for your cause
- **Generating content** tailored to your mission

What would you like help with today? You can ask me things like:
- "Create a flyer for my environmental nonprofit"
- "How do I start a nonprofit?"
- "Make me an email template for volunteer recruitment"
- "What are the legal requirements for nonprofits?"

Just tell me what you need!"""
        
        suggestions = [
            "Create a flyer for my cause",
            "Make me an email template",
            "Design a volunteer recruitment poster",
            "How do I start a nonprofit?",
            "What funding options are available?"
        ]
        
        return {
            "content": content,
            "materials": materials,
            "images": images,
            "suggestions": suggestions,
            "metadata": {"is_demo": True}
        }
    
    async def _create_image_request(self, request: ChatRequest) -> Optional[ImageRequest]:
        """Create an image request based on user message."""
        user_message = request.message.lower()
        
        # Determine image type
        image_type = ImageType.POSTER  # default
        if "flyer" in user_message:
            image_type = ImageType.FLYER
        elif "poster" in user_message:
            image_type = ImageType.POSTER
        elif "banner" in user_message:
            image_type = ImageType.BANNER
        elif "logo" in user_message:
            image_type = ImageType.LOGO
        elif "social" in user_message or "instagram" in user_message or "facebook" in user_message:
            image_type = ImageType.SOCIAL_MEDIA
        elif "infographic" in user_message:
            image_type = ImageType.INFOGRAPHIC
        
        # Determine style
        style = ImageStyle.PROFESSIONAL  # default
        if "modern" in user_message:
            style = ImageStyle.MODERN
        elif "colorful" in user_message or "bright" in user_message:
            style = ImageStyle.COLORFUL
        elif "minimal" in user_message or "simple" in user_message:
            style = ImageStyle.MINIMALIST
        elif "vintage" in user_message or "retro" in user_message:
            style = ImageStyle.VINTAGE
        elif "bold" in user_message or "striking" in user_message:
            style = ImageStyle.BOLD
        
        # Extract description and colors
        description = self._extract_description(request.message)
        colors = self._extract_colors(request.message)
        
        return ImageRequest(
            user_id=request.user_id,
            image_type=image_type,
            description=description,
            style=style,
            colors=colors,
            additional_details="High-quality nonprofit design suitable for professional use"
        )
    
    def _extract_description(self, message: str) -> str:
        """Extract the main description from user message."""
        # Remove common command words but keep descriptive content
        words_to_remove = ["create", "make", "design", "generate", "build", "a", "an", "the", "for", "my", "please", "can", "you", "me", "i", "want", "need"]
        
        words = message.lower().split()
        filtered_words = []
        
        for word in words:
            # Keep words that are longer than 2 characters and not in removal list
            if len(word) > 2 and word not in words_to_remove:
                # Remove punctuation
                clean_word = word.strip('.,!?;:')
                if clean_word:
                    filtered_words.append(clean_word)
        
        if not filtered_words:
            return "nonprofit organization"
        
        # Join the meaningful words to create a description
        description = " ".join(filtered_words[:8])  # Limit to 8 words for better prompts
        
        # If it's too short, add context
        if len(description.split()) < 2:
            description = f"{description} nonprofit organization"
        
        return description
    
    def _extract_colors(self, message: str) -> Optional[str]:
        """Extract color preferences from user message."""
        color_words = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "black", "white", "gray", "brown"]
        
        found_colors = []
        for color in color_words:
            if color in message.lower():
                found_colors.append(color)
        
        if found_colors:
            return " and ".join(found_colors[:3])  # Limit to 3 colors
        
        return None
    
    def _extract_materials(self, content: str, user_request: str) -> List[GeneratedMaterial]:
        """Extract generated materials from AI response."""
        materials = []
        
        # Simple pattern matching for material types
        material_patterns = {
            "flyer": r"(?i)flyer|promotional material",
            "poster": r"(?i)poster|banner",
            "email": r"(?i)email|message|template",
            "brochure": r"(?i)brochure|pamphlet",
            "social_media": r"(?i)social media|facebook|twitter|instagram"
        }
        
        for material_type, pattern in material_patterns.items():
            if re.search(pattern, user_request):
                # Extract relevant content section
                material_content = self._extract_material_content(content, material_type)
                if material_content:
                    materials.append(GeneratedMaterial(
                        material_type=material_type,
                        title=f"Custom {material_type.title()} for Your Nonprofit",
                        content=material_content,
                        format_instructions=f"This {material_type} is ready to use. Customize colors, fonts, and images as needed."
                    ))
        
        return materials
    
    def _extract_material_content(self, content: str, material_type: str) -> Optional[str]:
        """Extract specific material content from AI response."""
        # This is a simplified extraction - in a real implementation,
        # you'd use more sophisticated parsing
        lines = content.split('\n')
        material_lines = []
        in_material = False
        
        for line in lines:
            if material_type.lower() in line.lower() or in_material:
                in_material = True
                material_lines.append(line)
                # Stop at next section or end
                if line.strip() == "" and len(material_lines) > 3:
                    break
        
        return '\n'.join(material_lines) if material_lines else None
    
    def _generate_demo_materials(self, user_request: str) -> List[GeneratedMaterial]:
        """Generate demo materials based on user request."""
        materials = []
        request_lower = user_request.lower()
        
        if "flyer" in request_lower:
            materials.append(GeneratedMaterial(
                material_type="flyer",
                title="Custom Nonprofit Flyer",
                content="""# JOIN OUR MISSION
## Making a Difference in Our Community

**WHO WE ARE:**
A passionate group dedicated to positive change

**WHAT WE DO:**
• Community outreach programs
• Educational workshops
• Volunteer coordination
• Resource distribution

**HOW YOU CAN HELP:**
✓ Volunteer your time
✓ Donate resources
✓ Spread the word
✓ Join our events

**CONTACT US TODAY!**
📧 info@yournonprofit.org
📞 (555) 123-4567
🌐 www.yournonprofit.org

*Together, we can make a difference!*""",
                format_instructions="Print on 8.5x11 paper. Use bright colors and bold fonts. Add your logo and contact details."
            ))
        
        if "poster" in request_lower:
            materials.append(GeneratedMaterial(
                material_type="poster",
                title="Event Poster Design",
                content="""# COMMUNITY ACTION DAY
## Join Us for a Day of Impact!

**WHEN:** Saturday, [DATE]
**TIME:** 9:00 AM - 4:00 PM
**WHERE:** [LOCATION]

### ACTIVITIES:
🌱 Tree Planting
🧹 Community Cleanup
🎨 Kids Activities
🍕 Free Lunch

### WHY ATTEND?
• Make a real difference
• Meet like-minded people
• Learn new skills
• Have fun while helping

**REGISTER NOW!**
Visit: www.yournonprofit.org/events
Call: (555) 123-4567

*Bring friends, bring family, bring hope!*""",
                format_instructions="Design as 18x24 poster. Use high-contrast colors. Include compelling images of community activities."
            ))
        
        if "email" in request_lower:
            materials.append(GeneratedMaterial(
                material_type="email",
                title="Professional Email Template",
                content="""Subject: Join Us in Making a Difference - [Your Cause]

Dear [Name],

I hope this message finds you well. I'm reaching out because I believe you share our passion for making a positive impact in our community.

**About Our Mission:**
[Brief description of your nonprofit's mission and goals]

**Current Projects:**
• [Project 1 - brief description]
• [Project 2 - brief description]
• [Project 3 - brief description]

**How You Can Get Involved:**
Whether you have 2 hours or 20 hours to spare, there's a meaningful way for you to contribute:

✓ **Volunteer** - Join our team for hands-on impact
✓ **Donate** - Support our programs financially
✓ **Advocate** - Help spread awareness
✓ **Partner** - Collaborate on initiatives

**Next Steps:**
I'd love to chat more about how you can get involved. Reply to this email or call me at [phone number] to set up a brief conversation.

Thank you for considering joining our mission. Together, we can create lasting change!

Warm regards,

[Your Name]
[Your Title]
[Organization Name]
[Contact Information]

P.S. Follow us on social media [@yournonprofit] for updates on our latest projects!""",
                format_instructions="Customize the bracketed sections with your specific information. Use a professional email signature."
            ))
        
        return materials
    
    def _generate_suggestions(self, user_message: str, ai_response: str) -> List[str]:
        """Generate follow-up suggestions based on the conversation."""
        base_suggestions = [
            "Create a volunteer recruitment flyer",
            "Design a fundraising poster",
            "Write a donor thank-you email",
            "How do I register my nonprofit?",
            "What are effective fundraising strategies?"
        ]
        
        # Customize suggestions based on user message
        if "flyer" in user_message.lower():
            return [
                "Create a matching poster design",
                "Write an email to promote this flyer",
                "Design social media graphics",
                "Create a volunteer sign-up form"
            ]
        elif "email" in user_message.lower():
            return [
                "Create a follow-up email sequence",
                "Design a flyer to attach",
                "Write a social media post",
                "Create a donation landing page"
            ]
        elif "poster" in user_message.lower():
            return [
                "Create promotional flyers",
                "Write event invitation emails",
                "Design social media graphics",
                "Create volunteer task lists"
            ]
        
        return base_suggestions[:5]
    
    def get_conversation(self, conversation_id: str) -> Optional[ConversationHistory]:
        """Get conversation history by ID."""
        return self.conversations.get(conversation_id)
    
    def get_user_conversations(self, user_id: str) -> List[ConversationHistory]:
        """Get all conversations for a user."""
        return [conv for conv in self.conversations.values() if conv.user_id == user_id]