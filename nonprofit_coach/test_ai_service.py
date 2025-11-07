"""
Simple test script for AI service.
Run with: python3 test_ai_service.py
"""

import os
from dotenv import load_dotenv
from ai_service import create_ai_service, AIServiceError

# Load environment variables
load_dotenv()

def test_ai_service():
    """Test the AI service with real API calls."""
    
    # Get API key from environment or prompt user
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    
    if not api_key:
        print("⚠️  No ANTHROPIC_API_KEY found in environment")
        api_key = input("Enter your Anthropic API key (or press Enter to skip): ").strip()
        if not api_key:
            print("❌ Skipping API tests - no API key provided")
            return
    
    print("🔧 Creating AI service...")
    try:
        ai_service = create_ai_service(api_key)
        print("✅ AI service created successfully\n")
    except AIServiceError as e:
        print(f"❌ Failed to create AI service: {e}")
        return
    
    # Test 1: Generate follow-up question
    print("=" * 60)
    print("TEST 1: Generate Follow-up Question")
    print("=" * 60)
    
    try:
        question = ai_service.generate_follow_up_questions(
            question_type="description",
            user_response="I want to help homeless people in my community",
            idea_context={"title": "Community Homeless Support"}
        )
        print(f"✅ Follow-up question generated:\n{question}\n")
    except AIServiceError as e:
        print(f"❌ Failed to generate follow-up: {e}\n")
    
    # Test 2: Generate section content
    print("=" * 60)
    print("TEST 2: Generate Marketing Email")
    print("=" * 60)
    
    idea_summary = {
        'title': 'Community Homeless Support',
        'description': 'A nonprofit to provide meals and shelter to homeless individuals',
        'importance': 'Many people in our community lack basic necessities',
        'beneficiaries': 'Homeless individuals and families',
        'implementation': 'Partner with local shelters and organize meal drives',
        'significance': 'Reduce homelessness and provide dignity to those in need',
        'uniqueness': 'Focus on both immediate needs and long-term support'
    }
    
    try:
        email = ai_service.generate_section_content(
            idea_summary=idea_summary,
            section='marketing',
            content_type='email'
        )
        print(f"✅ Email content generated:\n{email}\n")
    except AIServiceError as e:
        print(f"❌ Failed to generate email: {e}\n")
    
    # Test 3: Chat with context
    print("=" * 60)
    print("TEST 3: Chat with Context")
    print("=" * 60)
    
    try:
        response = ai_service.chat_with_context(
            idea_summary=idea_summary,
            section='funding',
            user_message="What are some good grant sources for this nonprofit?"
        )
        print(f"✅ Chat response:\n{response}\n")
    except AIServiceError as e:
        print(f"❌ Failed to chat: {e}\n")
    
    print("=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)


if __name__ == '__main__':
    print("\n🧪 Testing AI Service\n")
    test_ai_service()
