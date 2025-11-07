# Implementation Plan

- [x] 1. Set up project structure and dependencies
  - Create Flask project directory structure
  - Create requirements.txt with Flask, anthropic, sqlite3
  - Set up basic Flask app with routes
  - Create templates and static folders
  - _Requirements: 1.1, 2.1_

- [x] 2. Implement database layer
  - [x] 2.1 Create SQLite database schema
    - Write db.py with connection helper functions
    - Create ideas table schema
    - Create content table schema
    - Create volunteers table schema (optional)
    - _Requirements: 1.5, 2.2_

  - [x] 2.2 Implement database helper functions
    - Write function to save idea responses
    - Write function to retrieve idea by ID
    - Write function to save generated content
    - Write function to retrieve content by idea and section
    - _Requirements: 1.5, 2.4_

- [x] 3. Build AI service integration
  - [x] 3.1 Create Claude API wrapper
    - Write ai_service.py with Claude API client
    - Implement function to generate follow-up questions
    - Implement function to generate section content
    - Add error handling for API failures
    - _Requirements: 1.3, 3.2, 4.2, 5.2, 6.2_

  - [x] 3.2 Create prompt templates
    - Write system prompt that includes idea context
    - Create prompts for each content type (email, flyer, pitch, etc.)
    - Add prompt for generating follow-up questions during questionnaire
    - _Requirements: 1.3, 3.2, 3.3, 3.4, 3.5, 4.2, 5.2, 6.2_

- [x] 4. Implement idea development questionnaire
  - [x] 4.1 Create home page with two tabs
    - Build index.html with tab interface (All Ideas / New Idea)
    - Create "All Ideas" tab showing list of previously created ideas with links
    - Create "New Idea" tab with API key input and questionnaire form
    - Add JavaScript for tab switching and dynamic content loading
    - Display AI-generated follow-up questions dynamically in questionnaire
    - _Requirements: 1.1, 1.2, 1.3_

  - [x] 4.2 Create questionnaire backend routes
    - Implement GET / route to serve home page with list of all ideas
    - Implement POST /start route to initialize session with API key
    - Create POST /question route to save responses and get follow-ups
    - Implement POST /complete route to finalize idea and trigger generation
    - Add session management for API key storage
    - _Requirements: 1.1, 1.2, 1.4, 1.5_

- [x] 5. Build website generator
  - [x] 5.1 Create HTML templates for generated sites
    - Write base template with navigation and clean styling
    - Create home page template with idea summary
    - Create section page template (reusable for all 4 sections)
    - Add embedded chat interface to section template
    - _Requirements: 2.1, 2.2, 2.3, 3.1, 4.1, 5.1, 6.1_

  - [x] 5.2 Implement site generation logic
    - Write site_generator.py with template rendering functions
    - Create function to generate all pages for an idea
    - Implement function to save generated HTML to file system
    - Add function to determine theme/colors based on cause type
    - _Requirements: 2.1, 2.2, 2.6_

  - [x] 5.3 Create routes to serve generated sites
    - Implement GET /site/<idea_id> route to serve generated home page
    - Create GET /site/<idea_id>/<section> route for section pages
    - Add static file serving for generated site assets
    - _Requirements: 2.1, 2.3_

- [x] 6. Implement section functionality (in startup journey order)
  - [x] 6.1 Create research section features
    - Add buttons for Implementation Steps, Local Orgs, Resources
    - Implement POST /generate route that accepts section and content type
    - Display generated content in the page
    - Add chat interface for research questions
    - _Requirements: 6.1, 6.2, 6.3, 6.5_

  - [x] 6.2 Create team building section features
    - Add buttons for Recruiting Pitch, Job Description, Volunteer Form
    - Implement volunteer management form (optional)
    - Connect to content generation API
    - Add chat interface for team-related questions
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 6.3 Create funding section features
    - Add buttons for Grant Proposal, Donor Letter, Budget Plan
    - Connect to content generation API
    - Add chat interface for funding questions
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [x] 6.4 Create marketing section features
    - Add buttons for Email, Flyer, Social Post
    - Connect to content generation API
    - Add chat interface for iterative refinement
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 7. Add styling and polish
  - [ ] 7.1 Create clean, minimal CSS
    - Write style.css with Apple-inspired design
    - Add responsive layout for mobile devices
    - Style forms, buttons, and chat interface
    - Add simple color themes for different cause types
    - _Requirements: 2.5, 2.6_

  - [ ] 7.2 Add JavaScript for interactivity
    - Write app.js for chat functionality
    - Add AJAX calls for content generation
    - Implement loading indicators
    - Add smooth transitions and basic animations
    - _Requirements: 3.1.6, 4.1.7, 5.1.7, 6.1.7_

- [ ] 8. Testing and documentation
  - [ ]* 8.1 Test core functionality
    - Test questionnaire flow end-to-end
    - Test website generation
    - Test content generation for each section
    - Test chat interface functionality
    - _Requirements: All_

  - [ ]* 8.2 Create setup documentation
    - Write README with installation instructions
    - Document API key setup process
    - Add troubleshooting guide
    - Create demo video or screenshots
    - _Requirements: All_
