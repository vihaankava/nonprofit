# Implementation Plan

- [x] 1. Set up search service infrastructure
  - Create search service module structure
  - Implement base search provider interface
  - Set up configuration management for search providers
  - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 1.1 Create search service base classes
  - Write `search_service.py` with SearchService class
  - Write `search_providers/base.py` with SearchProvider abstract class
  - Define SearchResults, SearchResult, Organization, Grant, and Resource data models
  - _Requirements: 8.1_

- [x] 1.2 Implement search cache layer
  - Write `search_cache.py` with SearchCache class
  - Implement cache key generation from query parameters
  - Implement TTL-based expiration logic
  - Add cleanup method for expired entries
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [x] 1.3 Add search configuration to environment
  - Update `.env` file with search provider settings
  - Add SEARCH_PROVIDER, BRAVE_API_KEY, SEARCH_ENABLED variables
  - Add cache configuration variables (TTL, max size)
  - Create configuration validation on app startup
  - _Requirements: 8.2, 8.3, 8.4, 8.5_

- [ ] 2. Implement Brave Search provider
  - Create Brave Search API integration
  - Implement result parsing and formatting
  - Add error handling and fallback logic
  - _Requirements: 1.1, 1.2, 2.1, 2.2, 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 2.1 Create Brave Search provider class
  - Write `search_providers/brave.py` with BraveSearchProvider class
  - Implement search() method with API request logic
  - Implement parse_results() method to convert API response to SearchResults
  - Add is_available() method to check API key configuration
  - _Requirements: 8.1_

- [ ] 2.2 Implement specialized search methods
  - Add search_local_organizations() method with location filtering
  - Add search_grants() method with funding-specific queries
  - Add search_resources() method for tools and platforms
  - Implement query construction for each search type
  - _Requirements: 1.1, 1.2, 4.1, 4.2, 5.1, 5.2_

- [ ] 2.3 Add error handling and fallback
  - Implement retry logic with exponential backoff
  - Add timeout handling (5 second limit)
  - Implement graceful degradation when search fails
  - Log all search errors with details
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 3. Enhance AI service for search integration
  - Modify AI service to accept search results
  - Update prompts to include search context
  - Add formatting instructions for tables and links
  - _Requirements: 1.3, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 3.1 Add search-aware content generation method
  - Create generate_section_content_with_search() method in AIService
  - Accept optional search_results parameter
  - Fall back to standard generation if search_results is None
  - _Requirements: 7.1, 7.4_

- [ ] 3.2 Enhance system prompts with search context
  - Create _get_enhanced_system_prompt() method
  - Format search results for inclusion in prompts
  - Add formatting requirements (tables, links, citations)
  - Instruct AI to use search results as primary source
  - _Requirements: 1.3, 2.3, 3.1, 3.2, 3.3_

- [ ] 3.3 Update content prompts for structured output
  - Modify _get_content_prompt() to request HTML tables
  - Add instructions for clickable links with anchor tags
  - Request citation formatting with source references
  - _Requirements: 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 4. Create content formatter module
  - Build content formatting utilities
  - Implement table generation from data
  - Add citation and link formatting
  - _Requirements: 1.3, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 4.1 Create ContentFormatter class
  - Write `content_formatter.py` with ContentFormatter class
  - Implement format_with_tables() static method
  - Implement add_citations() static method
  - Implement ensure_links_clickable() static method
  - _Requirements: 2.2, 2.3, 3.1, 3.2_

- [ ] 4.2 Add specialized table formatters
  - Implement format_organization_table() for local organizations
  - Implement format_grant_table() for funding opportunities
  - Implement format_resource_table() for tools and platforms
  - Add responsive CSS classes for mobile display
  - _Requirements: 1.3, 3.1, 3.2, 3.3, 3.4, 3.5, 4.3_

- [ ] 5. Integrate search into Flask routes
  - Modify /api/generate endpoint to use search
  - Add search decision logic
  - Implement search result processing
  - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 4.1, 4.2, 4.3, 5.1, 5.2, 5.3_

- [ ] 5.1 Update /api/generate endpoint
  - Add search service initialization
  - Implement should_use_search() helper function
  - Add perform_search() helper function
  - Integrate search results into content generation
  - Apply content formatting to final output
  - _Requirements: 1.1, 1.2, 2.1, 4.1, 5.1_

- [ ] 5.2 Implement search decision logic
  - Define which content types require search (local_orgs, grants, resources, etc.)
  - Create mapping of content types to search methods
  - Add location-based search for research section
  - _Requirements: 1.1, 1.2, 4.1, 4.2, 5.1, 5.2_

- [ ] 5.3 Add search result caching
  - Check cache before making API calls
  - Store successful search results in cache
  - Track API usage to prevent rate limit issues
  - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 6. Implement interactive content regeneration
  - Create chat intent analyzer
  - Add regeneration endpoint
  - Update frontend for content updates
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 6.1 Create ChatIntentAnalyzer class
  - Write `chat_intent_analyzer.py` with ChatIntentAnalyzer class
  - Implement detect_regeneration_request() method
  - Define RegenerationIntent data model
  - Add pattern matching for modification keywords
  - _Requirements: 9.1_

- [ ] 6.2 Create /api/regenerate endpoint
  - Add new Flask route for content regeneration
  - Accept current_content and modification_request parameters
  - Call AI service with modification context
  - Return regenerated content and confirmation message
  - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [ ] 6.3 Update AI service for regeneration
  - Add regenerate_content() method to AIService
  - Include current content and modification request in prompt
  - Maintain chat history context during regeneration
  - _Requirements: 9.1, 9.2, 9.4_

- [ ] 6.4 Update frontend JavaScript for regeneration
  - Modify sendMessage() to detect regeneration responses
  - Implement regenerateContent() function
  - Add visual feedback during regeneration (loading indicator)
  - Update content display area with new content
  - Add confirmation message to chat
  - _Requirements: 9.2, 9.3, 9.5_

- [ ] 7. Implement content-type specific artifacts
  - Create artifact renderer module
  - Build artifact templates for each content type
  - Add interactive features to artifacts
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 7.1 Create ArtifactRenderer class
  - Write `artifact_renderer.py` with ArtifactRenderer class
  - Implement render() method with type detection
  - Add render_email(), render_form(), render_budget(), render_flyer() methods
  - Parse AI-generated JSON into artifact templates
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 7.2 Create email artifact template
  - Build HTML template for email display
  - Add from/to/subject header fields
  - Create editable body content area
  - Add copy and download action buttons
  - _Requirements: 10.1_

- [ ] 7.3 Create form artifact template
  - Build HTML template for interactive forms
  - Support text inputs, textareas, selects, and checkboxes
  - Add form submission handling
  - Add copy HTML and preview buttons
  - _Requirements: 10.2_

- [ ] 7.4 Create budget artifact template
  - Build HTML table template for budget spreadsheet
  - Make cells editable with contenteditable
  - Add JavaScript for automatic total calculations
  - Add row addition and CSV export features
  - _Requirements: 10.3_

- [ ] 7.5 Create flyer artifact template
  - Build HTML template with visual design layout
  - Add header, body, and footer sections
  - Support custom colors and images
  - Add design editing and PDF download buttons
  - _Requirements: 10.4_

- [ ] 7.6 Update AI prompts for structured artifact output
  - Modify _get_content_prompt() to request JSON format for artifacts
  - Add JSON schema examples for each artifact type
  - Ensure AI outputs parseable structured data
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 7.7 Create artifact CSS stylesheet
  - Write `static/artifacts.css` with artifact-specific styles
  - Style email, form, budget, and flyer artifacts
  - Add responsive design for mobile devices
  - Style action buttons and interactive elements
  - _Requirements: 10.5_

- [ ] 8. Update database schema for artifacts
  - Add artifact_data column to content table
  - Update save_content() to store artifact JSON
  - Update get_content() to retrieve artifact data
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 8.1 Modify database schema
  - Add artifact_data TEXT column to content table
  - Create migration script if needed
  - Update db.py with new column handling
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 8.2 Update content storage functions
  - Modify save_content() to accept and store artifact_data
  - Modify get_content_by_idea_and_section() to return artifact_data
  - Ensure backward compatibility with existing content
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 9. Update frontend templates and JavaScript
  - Modify generated_section.html to support artifacts
  - Add artifact rendering on page load
  - Update content display logic
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 9.1 Update generated_section.html template
  - Include artifacts.css stylesheet
  - Add artifact container div
  - Update content display area to support artifacts
  - _Requirements: 10.5_

- [ ] 9.2 Update JavaScript for artifact rendering
  - Modify generateContent() to handle artifact responses
  - Add renderArtifact() function to display artifacts
  - Update regenerateContent() to support artifacts
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 9.3 Add artifact interaction handlers
  - Implement copy button functionality
  - Implement download button functionality
  - Add budget calculation logic
  - Add form preview functionality
  - _Requirements: 10.2, 10.3_

- [ ] 10. Add CSS for search-enhanced content
  - Create styles for tables and citations
  - Add responsive table layouts
  - Style clickable links
  - _Requirements: 1.3, 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 10.1 Create search content stylesheet
  - Write CSS for organization tables
  - Write CSS for grant tables
  - Write CSS for resource tables
  - Add citation section styling
  - Add responsive breakpoints for mobile
  - _Requirements: 1.3, 3.1, 3.2, 3.4, 3.5_

- [ ] 10.2 Update generated_section.html with search styles
  - Include search content CSS
  - Add table wrapper classes
  - Add citation container
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5_

- [ ] 11. Add requirements and documentation
  - Update requirements.txt with new dependencies
  - Add search provider setup instructions
  - Document artifact system
  - _Requirements: All_

- [ ] 11.1 Update requirements.txt
  - Add requests library for HTTP calls
  - Add any additional dependencies
  - Update anthropic version if needed
  - _Requirements: 8.1_

- [ ] 11.2 Update README with search setup
  - Document how to get Brave Search API key
  - Add environment variable configuration instructions
  - Document search provider options
  - Add troubleshooting section
  - _Requirements: 8.2, 8.3, 8.4, 8.5_

- [ ] 11.3 Create artifact documentation
  - Document available artifact types
  - Explain how to add new artifact types
  - Document artifact JSON schemas
  - Add examples for each artifact type
  - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 12. Testing and validation
  - Test search functionality with real API
  - Test cache behavior
  - Test artifact rendering
  - Test content regeneration
  - _Requirements: All_

- [ ] 12.1 Test search integration
  - Test Brave Search API connection
  - Verify local organization search results
  - Verify grant search results
  - Test cache hit/miss scenarios
  - Test fallback when search fails
  - _Requirements: 1.1, 1.2, 2.1, 4.1, 6.1, 6.2, 7.1, 7.2, 7.3_

- [ ] 12.2 Test artifact rendering
  - Generate and verify email artifact
  - Generate and verify form artifact
  - Generate and verify budget artifact
  - Generate and verify flyer artifact
  - Test artifact interactions (copy, download, edit)
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 12.3 Test content regeneration
  - Test chat-based modification requests
  - Verify content updates in upper display area
  - Test regeneration with different modification types
  - Verify chat history is maintained
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [ ] 12.4 Test formatting and responsiveness
  - Verify tables render correctly on desktop
  - Verify tables are responsive on mobile
  - Test link formatting and clickability
  - Verify citations display properly
  - _Requirements: 1.3, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 3.5_
