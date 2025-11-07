from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from dotenv import load_dotenv
from db import (
    save_idea, 
    get_idea_by_id,
    get_all_ideas,
    save_content, 
    get_content_by_idea_and_section,
    save_volunteer,
    get_volunteers_by_idea,
    delete_idea
)
from ai_service import create_ai_service, AIServiceError
from site_generator import (
    generate_home_page,
    generate_section_page,
    generate_and_save_site
)

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Helper function to get API key
def get_api_key():
    """Get API key from session or environment variable."""
    return session.get('api_key') or os.environ.get('ANTHROPIC_API_KEY')

# Landing page route - shows all ideas and new idea form
@app.route('/')
def index():
    # Get all ideas from database
    ideas = get_all_ideas()
    return render_template('index.html', ideas=ideas)

# API key setup route
@app.route('/api/setup', methods=['POST'])
def setup_api_key():
    data = request.get_json()
    api_key = data.get('api_key')
    save_api_key = data.get('save_api_key', False)
    
    # If no API key provided, check if one exists in environment
    if not api_key:
        api_key = os.environ.get('ANTHROPIC_API_KEY')
        if not api_key:
            return jsonify({'error': 'API key is required'}), 400
    
    session['api_key'] = api_key
    session['save_api_key'] = save_api_key
    session.permanent = True  # Make session persist
    return jsonify({'success': True})

# Start idea development session
@app.route('/api/start', methods=['POST'])
def start_session():
    if 'api_key' not in session:
        return jsonify({'error': 'API key not configured'}), 401
    
    # TODO: Initialize idea development session
    return jsonify({'success': True, 'session_id': 'placeholder'})

# Save question response and get follow-up
@app.route('/api/question', methods=['POST'])
def save_question():
    api_key = get_api_key()
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 401
    
    try:
        data = request.get_json()
        question_type = data.get('question_type')
        user_response = data.get('user_response')
        idea_context = data.get('idea_context', {})
        
        # Create AI service
        ai_service = create_ai_service(api_key)
        
        # Generate follow-up question
        followup = ai_service.generate_follow_up_questions(
            question_type=question_type,
            user_response=user_response,
            idea_context=idea_context
        )
        
        return jsonify({'success': True, 'followup': followup})
        
    except AIServiceError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Failed to generate follow-up'}), 500

# Complete questionnaire and generate site
@app.route('/api/complete', methods=['POST'])
def complete_questionnaire():
    api_key = get_api_key()
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 401
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'importance', 'beneficiaries', 
                          'implementation', 'significance', 'uniqueness']
        
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Save idea to database
        idea_data = {
            'title': data.get('title'),
            'description': data.get('description'),
            'importance': data.get('importance'),
            'beneficiaries': data.get('beneficiaries'),
            'implementation': data.get('implementation'),
            'significance': data.get('significance'),
            'uniqueness': data.get('uniqueness'),
            'status': 'complete'
        }
        
        # Save API key if user opted in
        if session.get('save_api_key'):
            idea_data['api_key'] = api_key
        
        idea_id = save_idea(idea_data)
        
        # Generate website
        idea = get_idea_by_id(idea_id)
        if idea:
            generate_and_save_site(idea)
        
        return jsonify({'success': True, 'idea_id': idea_id})
        
    except Exception as e:
        print(f"Error saving idea: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to save idea: {str(e)}'}), 500

# Serve generated site home page
@app.route('/site/<int:idea_id>')
def serve_site(idea_id):
    # Get idea from database
    idea = get_idea_by_id(idea_id)
    
    if not idea:
        return "Idea not found", 404
    
    # If idea has stored API key, use it; otherwise use environment or session
    if idea.get('api_key'):
        session['api_key'] = idea['api_key']
    elif not get_api_key():
        # Redirect to home page to enter API key
        return redirect(url_for('index'))
    
    # Generate and serve home page
    return generate_home_page(idea)

# Serve generated site section pages
@app.route('/site/<int:idea_id>/<section>')
def serve_section(idea_id, section):
    # Validate section
    valid_sections = ['research', 'team', 'funding', 'marketing']
    if section not in valid_sections:
        return "Invalid section", 404
    
    # Get idea from database
    idea = get_idea_by_id(idea_id)
    
    if not idea:
        return "Idea not found", 404
    
    # If idea has stored API key, use it; otherwise use environment or session
    if idea.get('api_key'):
        session['api_key'] = idea['api_key']
    elif not get_api_key():
        # Redirect to home page to enter API key
        return redirect(url_for('index'))
    
    # Generate and serve section page
    return generate_section_page(idea, section)

# Generate content for sections
@app.route('/api/generate', methods=['POST'])
def generate_content():
    api_key = get_api_key()
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 401
    
    try:
        data = request.get_json()
        idea_id = data.get('idea_id')
        section = data.get('section')
        content_type = data.get('content_type')
        chat_context = data.get('chat_context', [])
        
        # Get idea from database
        idea = get_idea_by_id(idea_id)
        if not idea:
            return jsonify({'error': 'Idea not found'}), 404
        
        # Create AI service
        ai_service = create_ai_service(api_key)
        
        # Generate content
        content = ai_service.generate_section_content(
            idea_summary=idea,
            section=section,
            content_type=content_type,
            chat_context=chat_context
        )
        
        # Save content to database
        save_content(idea_id, section, content_type, content)
        
        return jsonify({'success': True, 'content': content})
        
    except AIServiceError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Failed to generate content'}), 500


# Chat with AI assistant
@app.route('/api/chat', methods=['POST'])
def chat():
    api_key = get_api_key()
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 401
    
    try:
        data = request.get_json()
        idea_id = data.get('idea_id')
        section = data.get('section')
        message = data.get('message')
        chat_history = data.get('chat_history', [])
        
        # Get idea from database
        idea = get_idea_by_id(idea_id)
        if not idea:
            return jsonify({'error': 'Idea not found'}), 404
        
        # Create AI service
        ai_service = create_ai_service(api_key)
        
        # Get AI response
        response = ai_service.chat_with_context(
            idea_summary=idea,
            section=section,
            user_message=message,
            chat_history=chat_history
        )
        
        return jsonify({'success': True, 'response': response})
        
    except AIServiceError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'Failed to get response'}), 500

# Delete an idea
@app.route('/api/ideas/<int:idea_id>', methods=['DELETE'])
def delete_idea_route(idea_id):
    try:
        # Delete from database
        success = delete_idea(idea_id)
        
        if success:
            # Delete generated site files
            import shutil
            site_dir = os.path.join(
                os.path.dirname(__file__),
                'generated_sites',
                str(idea_id)
            )
            if os.path.exists(site_dir):
                shutil.rmtree(site_dir)
            
            return jsonify({'success': True, 'message': 'Idea deleted successfully'})
        else:
            return jsonify({'error': 'Failed to delete idea'}), 500
            
    except Exception as e:
        print(f"Error deleting idea: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Failed to delete idea: {str(e)}'}), 500


# Logout/clear API key
@app.route('/api/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# ============================================================
# TEST ROUTES FOR TASKS 1 & 2 - Database Integration
# ============================================================

@app.route('/test')
def test_page():
    """Serve the test interface page."""
    return render_template('test.html')


@app.route('/api/test/ideas', methods=['POST'])
def test_create_idea():
    """Test route: Create a new nonprofit idea."""
    try:
        data = request.get_json()
        idea_id = save_idea(data)
        idea = get_idea_by_id(idea_id)
        return jsonify({
            'success': True,
            'idea_id': idea_id,
            'idea': idea
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/test/ideas/<int:idea_id>', methods=['GET'])
def test_get_idea(idea_id):
    """Test route: Get an idea by ID."""
    try:
        idea = get_idea_by_id(idea_id)
        if idea:
            return jsonify({
                'success': True,
                'idea': idea
            })
        return jsonify({'error': 'Idea not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/test/ideas/<int:idea_id>/content', methods=['POST'])
def test_save_content(idea_id):
    """Test route: Save content for an idea."""
    try:
        data = request.get_json()
        content_id = save_content(
            idea_id=idea_id,
            section=data.get('section'),
            content_type=data.get('content_type'),
            content=data.get('content')
        )
        return jsonify({
            'success': True,
            'content_id': content_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/test/ideas/<int:idea_id>/content/<section>', methods=['GET'])
def test_get_content(idea_id, section):
    """Test route: Get content for an idea and section."""
    try:
        content_type = request.args.get('content_type')
        content = get_content_by_idea_and_section(idea_id, section, content_type)
        return jsonify({
            'success': True,
            'content': content
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/test/ideas/<int:idea_id>/volunteers', methods=['POST'])
def test_save_volunteer(idea_id):
    """Test route: Save volunteer for an idea."""
    try:
        data = request.get_json()
        volunteer_id = save_volunteer(idea_id, data)
        return jsonify({
            'success': True,
            'volunteer_id': volunteer_id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/test/ideas/<int:idea_id>/volunteers', methods=['GET'])
def test_get_volunteers(idea_id):
    """Test route: Get volunteers for an idea."""
    try:
        volunteers = get_volunteers_by_idea(idea_id)
        return jsonify({
            'success': True,
            'volunteers': volunteers
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Use PORT from environment variable for deployment, or 5001 for local
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
