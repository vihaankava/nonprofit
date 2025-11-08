# Requirements Document

## Introduction

This feature enhances the Nonprofit Idea Coach application by integrating web search capabilities to provide users with accurate, real-time local information, current resources, and properly formatted content. Currently, the AI generates content based solely on its training data, which limits its ability to provide specific local organizations, up-to-date contact information, and verifiable web links. This enhancement will enable the system to search the web for relevant information and present it in well-structured formats including tables, lists, and citations.

## Glossary

- **Search Service**: The web search API integration layer that queries external search providers and returns structured results
- **AI Service**: The existing Claude API wrapper that generates content for the nonprofit coach
- **Content Generator**: The component that combines search results with AI-generated content
- **Search Provider**: External web search API (Brave Search API, Google Custom Search, etc.)
- **Citation**: A reference to a web source including title, URL, and snippet
- **Structured Content**: Content formatted with HTML tables, lists, and other semantic elements
- **Local Information**: Geographic-specific data about organizations, resources, and contacts in the user's specified location

## Requirements

### Requirement 1

**User Story:** As a nonprofit founder, I want the coach to provide real local organizations and resources in my area, so that I can find actual partners and support networks to help launch my nonprofit.

#### Acceptance Criteria

1. WHEN THE Content Generator creates research content, THE Search Service SHALL query for local organizations based on the user's specified location
2. WHEN THE Search Service returns results, THE Content Generator SHALL include organization names, websites, and contact information in the generated content
3. THE Content Generator SHALL format local organization information in HTML tables with columns for name, description, website, and relevance
4. WHEN no location is specified, THE Search Service SHALL provide general nonprofit resources without geographic filtering
5. THE Content Generator SHALL include at least 5-10 relevant local organizations when available in search results

### Requirement 2

**User Story:** As a nonprofit founder, I want all generated content to include clickable links to real websites and resources, so that I can easily access the information and verify its accuracy.

#### Acceptance Criteria

1. WHEN THE Content Generator creates any section content, THE Search Service SHALL retrieve relevant web resources with valid URLs
2. THE Content Generator SHALL format all URLs as clickable HTML links with descriptive anchor text
3. THE Content Generator SHALL include citations with source titles, URLs, and brief descriptions
4. WHEN THE AI Service generates funding information, THE Search Service SHALL find current grant opportunities with application links
5. THE Content Generator SHALL validate that all included URLs are properly formatted and accessible

### Requirement 3

**User Story:** As a nonprofit founder, I want content formatted with tables and structured layouts, so that information is easy to read and compare.

#### Acceptance Criteria

1. THE Content Generator SHALL format comparative information using HTML tables with proper headers and rows
2. WHEN presenting multiple options or resources, THE Content Generator SHALL use tables to display name, description, cost, and website columns
3. THE Content Generator SHALL use HTML lists (ordered and unordered) for sequential steps and bullet points
4. THE Content Generator SHALL apply CSS classes for responsive table layouts on mobile devices
5. THE Content Generator SHALL include table captions that describe the data being presented

### Requirement 4

**User Story:** As a nonprofit founder, I want the coach to find current grant opportunities and funding sources, so that I can apply for financial support with up-to-date information.

#### Acceptance Criteria

1. WHEN THE user requests funding content, THE Search Service SHALL query for current grant opportunities relevant to the nonprofit's cause
2. THE Search Service SHALL filter results by grant deadline, eligibility, and funding amount when available
3. THE Content Generator SHALL present grant opportunities in a table format with columns for grant name, funder, amount, deadline, and application link
4. THE Content Generator SHALL prioritize grants with upcoming deadlines within the next 6 months
5. THE Search Service SHALL include both government and private foundation funding sources

### Requirement 5

**User Story:** As a nonprofit founder, I want the coach to provide accurate implementation steps with real tools and platforms, so that I can follow actionable guidance with current resources.

#### Acceptance Criteria

1. WHEN THE Content Generator creates implementation plans, THE Search Service SHALL find current tools, platforms, and services mentioned in the plan
2. THE Content Generator SHALL include direct links to sign-up pages, documentation, and pricing information for recommended tools
3. THE Search Service SHALL verify that recommended platforms are currently active and accepting new users
4. THE Content Generator SHALL format tool comparisons in tables showing features, pricing, and best use cases
5. THE Content Generator SHALL include at least one alternative option for each recommended tool or platform

### Requirement 6

**User Story:** As a nonprofit founder, I want search results to be cached temporarily, so that the application responds quickly and doesn't exceed API rate limits.

#### Acceptance Criteria

1. THE Search Service SHALL cache search results for identical queries for 24 hours
2. WHEN THE Search Service receives a query, THE Search Service SHALL check the cache before making an external API call
3. THE Search Service SHALL track API usage and prevent exceeding rate limits by returning cached results when limits are approached
4. THE Search Service SHALL store cache entries with timestamps and query parameters as keys
5. THE Search Service SHALL automatically clear cache entries older than 24 hours

### Requirement 7

**User Story:** As a nonprofit founder, I want the system to gracefully handle search failures, so that I still receive helpful content even when web search is unavailable.

#### Acceptance Criteria

1. WHEN THE Search Service fails to return results, THE Content Generator SHALL generate content using the AI Service without search augmentation
2. THE Content Generator SHALL log search failures with error details for debugging
3. WHEN search API rate limits are exceeded, THE Content Generator SHALL use cached results or AI-only generation
4. THE Content Generator SHALL display a notice to users when content is generated without web search
5. THE Search Service SHALL retry failed requests once with exponential backoff before falling back to AI-only mode

### Requirement 8

**User Story:** As a system administrator, I want to configure which search provider to use, so that I can choose based on cost, features, and reliability.

#### Acceptance Criteria

1. THE Search Service SHALL support multiple search providers through a pluggable interface (Brave Search, Google Custom Search, Bing)
2. THE Search Service SHALL read the active search provider from environment configuration
3. WHEN no search provider is configured, THE Search Service SHALL default to AI-only content generation
4. THE Search Service SHALL require API keys for search providers to be stored in environment variables
5. THE Search Service SHALL validate search provider configuration on application startup and log any configuration errors

### Requirement 9

**User Story:** As a nonprofit founder, I want to ask the chatbot to modify the generated content in the upper section, so that I can iteratively refine the content without regenerating from scratch.

#### Acceptance Criteria

1. WHEN THE user sends a chat message requesting content changes, THE AI Service SHALL detect modification requests and regenerate the content
2. THE Content Generator SHALL update the upper content display area with the regenerated content automatically
3. THE Content Generator SHALL maintain the current content type context when regenerating based on chat requests
4. WHEN content is regenerated via chat, THE Content Generator SHALL preserve the chat history for context
5. THE user interface SHALL provide visual feedback when content is being regenerated from a chat request

### Requirement 10

**User Story:** As a nonprofit founder, I want different content types to be displayed with appropriate formatting and interactive elements, so that emails look like emails, forms are fillable, and budgets are presented as spreadsheets.

#### Acceptance Criteria

1. WHEN THE Content Generator creates email content, THE system SHALL display it with email-specific formatting including subject line, to/from fields, and body sections
2. WHEN THE Content Generator creates form content (volunteer forms, contact forms), THE system SHALL render interactive HTML form elements with input fields, dropdowns, and submit buttons
3. WHEN THE Content Generator creates budget or financial content, THE system SHALL present it as an interactive table with editable cells and calculation features
4. WHEN THE Content Generator creates flyer or marketing content, THE system SHALL apply visual design templates with appropriate typography and layout
5. THE Content Generator SHALL use content-type specific CSS classes and templates to ensure each artifact type has distinct visual presentation
