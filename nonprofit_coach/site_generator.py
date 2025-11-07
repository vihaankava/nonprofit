"""
Site Generator for Nonprofit Idea Coach
Generates personalized websites for each nonprofit idea.
"""

import os
from typing import Dict, Any
from flask import render_template


# Theme colors based on cause type keywords
THEME_COLORS = {
    'education': '#0071e3',      # Blue
    'health': '#34c759',         # Green
    'environment': '#30d158',    # Green
    'animals': '#ff9500',        # Orange
    'children': '#ff2d55',       # Pink
    'elderly': '#5856d6',        # Purple
    'homeless': '#ff3b30',       # Red
    'hunger': '#ff9500',         # Orange
    'poverty': '#af52de',        # Purple
    'community': '#0071e3',      # Blue
    'arts': '#ff2d55',           # Pink
    'sports': '#32ade6',         # Light Blue
    'technology': '#5856d6',     # Purple
    'default': '#0071e3'         # Default Blue
}


def determine_theme_color(idea: Dict[str, Any]) -> str:
    """
    Determine theme color based on cause type from idea content.
    
    Args:
        idea: Dictionary containing idea data
        
    Returns:
        Hex color code for the theme
    """
    # Combine relevant text fields
    text_to_analyze = ' '.join([
        idea.get('title', ''),
        idea.get('description', ''),
        idea.get('beneficiaries', '')
    ]).lower()
    
    # Check for keywords
    for keyword, color in THEME_COLORS.items():
        if keyword in text_to_analyze:
            return color
    
    return THEME_COLORS['default']


def generate_home_page(idea: Dict[str, Any]) -> str:
    """
    Generate HTML for the home page of a nonprofit site.
    
    Args:
        idea: Dictionary containing idea data
        
    Returns:
        Rendered HTML string
    """
    theme_color = determine_theme_color(idea)
    
    return render_template(
        'generated_home.html',
        idea=idea,
        theme_color=theme_color,
        current_page='home'
    )


def generate_section_page(idea: Dict[str, Any], section: str) -> str:
    """
    Generate HTML for a section page (research, team, funding, marketing).
    
    Args:
        idea: Dictionary containing idea data
        section: Section name ('research', 'team', 'funding', 'marketing')
        
    Returns:
        Rendered HTML string
    """
    theme_color = determine_theme_color(idea)
    
    # Section configurations
    section_config = {
        'research': {
            'title': '📚 Research & Planning',
            'description': 'Plan your approach and understand the landscape',
            'buttons': [
                {'label': 'Implementation Steps', 'type': 'implementation_steps'},
                {'label': 'Local Organizations', 'type': 'local_orgs'},
                {'label': 'Resources', 'type': 'resources'}
            ]
        },
        'team': {
            'title': '👥 Team Building',
            'description': 'Build and manage your volunteer team',
            'buttons': [
                {'label': 'Recruiting Pitch', 'type': 'recruiting_pitch'},
                {'label': 'Job Description', 'type': 'job_description'},
                {'label': 'Volunteer Form', 'type': 'volunteer_form'}
            ]
        },
        'funding': {
            'title': '💰 Funding Strategy',
            'description': 'Secure resources and funding for your nonprofit',
            'buttons': [
                {'label': 'Grant Proposal', 'type': 'grant_proposal'},
                {'label': 'Donor Letter', 'type': 'donor_letter'},
                {'label': 'Budget Plan', 'type': 'budget_plan'}
            ]
        },
        'marketing': {
            'title': '📢 Marketing Materials',
            'description': 'Promote your cause and engage supporters',
            'buttons': [
                {'label': 'Email Template', 'type': 'email'},
                {'label': 'Flyer', 'type': 'flyer'},
                {'label': 'Social Post', 'type': 'social_post'}
            ]
        }
    }
    
    config = section_config.get(section, {
        'title': section.capitalize(),
        'description': '',
        'buttons': []
    })
    
    return render_template(
        'generated_section.html',
        idea=idea,
        theme_color=theme_color,
        current_page=section,
        section_name=section,
        section_title=config['title'],
        section_description=config['description'],
        section_buttons=config['buttons']
    )


def generate_all_pages(idea: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate all pages for a nonprofit site.
    
    Args:
        idea: Dictionary containing idea data
        
    Returns:
        Dictionary mapping page names to HTML content
    """
    pages = {
        'home': generate_home_page(idea),
        'research': generate_section_page(idea, 'research'),
        'team': generate_section_page(idea, 'team'),
        'funding': generate_section_page(idea, 'funding'),
        'marketing': generate_section_page(idea, 'marketing')
    }
    
    return pages


def save_generated_site(idea_id: int, pages: Dict[str, str]) -> bool:
    """
    Save generated HTML pages to file system.
    
    Args:
        idea_id: ID of the idea
        pages: Dictionary mapping page names to HTML content
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create directory for this idea's site
        site_dir = os.path.join(
            os.path.dirname(__file__),
            'generated_sites',
            str(idea_id)
        )
        os.makedirs(site_dir, exist_ok=True)
        
        # Save each page
        for page_name, html_content in pages.items():
            filename = 'index.html' if page_name == 'home' else f'{page_name}.html'
            filepath = os.path.join(site_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
        
        return True
        
    except Exception as e:
        print(f"Error saving generated site: {e}")
        return False


def generate_and_save_site(idea: Dict[str, Any]) -> bool:
    """
    Generate all pages for an idea and save them to file system.
    
    Args:
        idea: Dictionary containing idea data
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Generate all pages
        pages = generate_all_pages(idea)
        
        # Save to file system
        return save_generated_site(idea['id'], pages)
        
    except Exception as e:
        print(f"Error generating site: {e}")
        return False
