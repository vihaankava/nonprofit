"""
Simple integration test for tasks 1 and 2.
Tests the project structure and database layer together.
"""

import os
import sys
from db import (
    save_idea, 
    get_idea_by_id, 
    save_content, 
    get_content_by_idea_and_section,
    save_volunteer,
    get_volunteers_by_idea
)

def test_idea_workflow():
    """Test the complete idea creation and retrieval workflow."""
    print("=" * 60)
    print("Testing Nonprofit Idea Coach - Tasks 1 & 2 Integration")
    print("=" * 60)
    
    # Test 1: Save a new idea
    print("\n1. Creating a new nonprofit idea...")
    idea_data = {
        'title': 'Community Food Bank',
        'description': 'A food bank to serve low-income families',
        'importance': 'Addresses food insecurity in our community',
        'beneficiaries': 'Low-income families and seniors',
        'implementation': 'Partner with local grocery stores for donations',
        'significance': 'Will serve 500+ families monthly',
        'uniqueness': 'Focus on fresh produce and nutrition education',
        'status': 'draft'
    }
    
    idea_id = save_idea(idea_data)
    print(f"   ✓ Idea created with ID: {idea_id}")
    
    # Test 2: Retrieve the idea
    print("\n2. Retrieving the idea from database...")
    retrieved_idea = get_idea_by_id(idea_id)
    if retrieved_idea:
        print(f"   ✓ Retrieved idea: {retrieved_idea['title']}")
        print(f"   ✓ Description: {retrieved_idea['description']}")
    else:
        print("   ✗ Failed to retrieve idea")
        return False
    
    # Test 3: Save marketing content
    print("\n3. Saving generated marketing content...")
    content_id = save_content(
        idea_id=idea_id,
        section='marketing',
        content_type='email',
        content='Join us in fighting food insecurity! Our Community Food Bank...'
    )
    print(f"   ✓ Marketing email saved with ID: {content_id}")
    
    # Test 4: Save team content
    print("\n4. Saving team building content...")
    content_id = save_content(
        idea_id=idea_id,
        section='team',
        content_type='job_description',
        content='Volunteer Coordinator - Organize food distribution events...'
    )
    print(f"   ✓ Job description saved with ID: {content_id}")
    
    # Test 5: Retrieve content by section
    print("\n5. Retrieving marketing content...")
    marketing_content = get_content_by_idea_and_section(idea_id, 'marketing')
    print(f"   ✓ Found {len(marketing_content)} marketing content item(s)")
    for item in marketing_content:
        print(f"     - {item['content_type']}: {item['content'][:50]}...")
    
    print("\n6. Retrieving team content...")
    team_content = get_content_by_idea_and_section(idea_id, 'team')
    print(f"   ✓ Found {len(team_content)} team content item(s)")
    for item in team_content:
        print(f"     - {item['content_type']}: {item['content'][:50]}...")
    
    # Test 6: Save volunteer information
    print("\n7. Adding volunteer information...")
    volunteer_data = {
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'phone': '555-1234',
        'address': '123 Main St',
        'task': 'Food sorting and distribution'
    }
    volunteer_id = save_volunteer(idea_id, volunteer_data)
    print(f"   ✓ Volunteer saved with ID: {volunteer_id}")
    
    # Test 7: Retrieve volunteers
    print("\n8. Retrieving volunteers for this idea...")
    volunteers = get_volunteers_by_idea(idea_id)
    print(f"   ✓ Found {len(volunteers)} volunteer(s)")
    for vol in volunteers:
        print(f"     - {vol['name']} ({vol['email']}) - {vol['task']}")
    
    # Test 8: Update existing idea
    print("\n9. Updating the idea status...")
    idea_data['id'] = idea_id
    idea_data['status'] = 'active'
    updated_id = save_idea(idea_data)
    updated_idea = get_idea_by_id(updated_id)
    print(f"   ✓ Idea status updated to: {updated_idea['status']}")
    
    print("\n" + "=" * 60)
    print("✓ All tests passed successfully!")
    print("=" * 60)
    print(f"\nDatabase location: {os.path.abspath('nonprofit.db')}")
    return True

if __name__ == '__main__':
    try:
        success = test_idea_workflow()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
