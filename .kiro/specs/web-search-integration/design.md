# Design Document: Web Search Integration

## Overview

This design document outlines the architecture for integrating web search capabilities into the Nonprofit Idea Coach application. The enhancement will enable the system to retrieve real-time, location-specific information about local organizations, current grant opportunities, and verified resources. The design follows a modular approach with a pluggable search provider interface, caching layer, and enhanced content generation that combines AI with search results.

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│   Flask App     │
│   (app.py)      │
└────────┬────────┘
         │
         ├──────────────────┬──────────────────┐
         │                  │                  │
         ▼                  ▼                  ▼
┌─────────────────┐  ┌──────────────┐  ┌──────────────┐
│  AI Service     │  │Search Service│  │Content Gen   │
│ (ai_service.py) │  │(search_svc.py│  │(enhanced)    │
└─────────────────┘  └──────┬───────┘  └──────────────┘
                            │
                            ├────────────┬────────────┐
                            ▼            ▼            ▼
                     ┌──────────┐ ┌──────────┐ ┌──────────┐
                     │  Brave   │ │  Google  │ │   Bing   │
                     │ Provider │ │ Provider │ │ Provider │
                     └──────────┘ └──────────┘ └──────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ Cache Layer  │
                     │ (in-memory)  │
                     └──────────────┘
```

### Component Interaction Flow

1. **User Request** → Flask route receives content generation request
2. **Search Service** → Determines if search is needed based on content type
3. **Cache Check** → Checks if results exist in cache
4. **Search Provider** → Queries external API if cache miss
5. **Result Processing** → Formats and structures search results
6. **AI Service** → Generates content with search results as context
7. **Content Formatter** → Applies HTML formatting (tables, links, citations)
8. **Response** → Returns enhanced content to user

## Components and Interfaces

### 1. Search Service (`search_service.py`)

**Purpose:** Orchestrates web searches, manages caching, and provides a unified interface for multiple search providers.

**Class: SearchService**

```python
class SearchService:
    def __init__(self, provider: SearchProvider, cache: SearchCache):
        """Initialize with a search provider and cache."""
        
    def search(self, query: str, location: Optional[str] = None, 
               filters: Optional[Dict] = None) -> SearchResults:
        """
        Execute a search query with optional location and filters.
        Returns structured search results.
        """
        
    def search_local_organizations(self, cause: str, location: str, 
                                   limit: int = 10) -> List[Organization]:
        """
        Search for local nonprofit organizations and community resources.
        """
        
    def search_grants(self, cause: str, location: Optional[str] = None,
                     limit: int = 10) -> List[Grant]:
        """
        Search for current grant opportunities relevant to the cause.
        """
        
    def search_resources(self, topic: str, limit: int = 5) -> List[Resource]:
        """
        Search for tools, platforms, and educational resources.
        """
```

### 2. Search Provider Interface (`search_providers/base.py`)

**Purpose:** Abstract interface that all search providers must implement.

```python
class SearchProvider(ABC):
    @abstractmethod
    def search(self, query: str, params: Dict) -> Dict:
        """Execute search and return raw results."""
        
    @abstractmethod
    def parse_results(self, raw_results: Dict) -> SearchResults:
        """Parse provider-specific results into standard format."""
        
    @abstractmethod
    def is_available(self) -> bool:
        """Check if provider is configured and available."""
```

### 3. Brave Search Provider (`search_providers/brave.py`)

**Purpose:** Implementation for Brave Search API.

```python
class BraveSearchProvider(SearchProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        
    def search(self, query: str, params: Dict) -> Dict:
        """Make API request to Brave Search."""
        
    def parse_results(self, raw_results: Dict) -> SearchResults:
        """Convert Brave API response to SearchResults."""
```

### 4. Search Cache (`search_cache.py`)

**Purpose:** In-memory caching with TTL to reduce API calls and improve performance.

```python
class SearchCache:
    def __init__(self, ttl_seconds: int = 86400):  # 24 hours default
        self.cache: Dict[str, CacheEntry] = {}
        self.ttl_seconds = ttl_seconds
        
    def get(self, cache_key: str) -> Optional[SearchResults]:
        """Retrieve cached results if not expired."""
        
    def set(self, cache_key: str, results: SearchResults):
        """Store results with timestamp."""
        
    def generate_key(self, query: str, params: Dict) -> str:
        """Generate cache key from query and parameters."""
        
    def cleanup_expired(self):
        """Remove expired cache entries."""
```

### 5. Enhanced AI Service (`ai_service.py` - modifications)

**Purpose:** Extend existing AI service to accept and utilize search results in prompts.

**New Method:**
```python
def generate_section_content_with_search(
    self,
    idea_summary: Dict,
    section: str,
    content_type: str,
    search_results: Optional[SearchResults] = None,
    chat_context: Optional[List[Dict]] = None
) -> str:
    """
    Generate content with search results integrated into the prompt.
    Falls back to standard generation if search_results is None.
    """
```

### 6. Content Formatter (`content_formatter.py`)

**Purpose:** Format AI-generated content with proper HTML structure, tables, and citations.

```python
class ContentFormatter:
    @staticmethod
    def format_with_tables(content: str, data: List[Dict], 
                          table_type: str) -> str:
        """Insert HTML tables into content based on data type."""
        
    @staticmethod
    def add_citations(content: str, sources: List[Source]) -> str:
        """Append citation section with source links."""
        
    @staticmethod
    def ensure_links_clickable(content: str) -> str:
        """Convert plain URLs to HTML anchor tags."""
        
    @staticmethod
    def format_organization_table(orgs: List[Organization]) -> str:
        """Create HTML table for local organizations."""
        
    @staticmethod
    def format_grant_table(grants: List[Grant]) -> str:
        """Create HTML table for grant opportunities."""
```

## Data Models

### SearchResults
```python
@dataclass
class SearchResults:
    query: str
    results: List[SearchResult]
    total_results: int
    search_time: float
    timestamp: datetime
```

### SearchResult
```python
@dataclass
class SearchResult:
    title: str
    url: str
    snippet: str
    domain: str
    relevance_score: Optional[float] = None
```

### Organization
```python
@dataclass
class Organization:
    name: str
    description: str
    website: Optional[str]
    location: str
    contact: Optional[str]
    relevance: str  # Why it's relevant to the nonprofit
```

### Grant
```python
@dataclass
class Grant:
    name: str
    funder: str
    amount: Optional[str]
    deadline: Optional[str]
    eligibility: str
    application_url: str
    description: str
```

### Resource
```python
@dataclass
class Resource:
    title: str
    url: str
    description: str
    resource_type: str  # 'tool', 'guide', 'platform', 'article'
    cost: Optional[str]  # 'free', 'paid', 'freemium'
```

## Integration Points

### 1. Flask Routes (`app.py`)

**Modify `/api/generate` endpoint:**

```python
@app.route('/api/generate', methods=['POST'])
def generate_content():
    # ... existing code ...
    
    # Initialize search service
    search_service = create_search_service()
    
    # Determine if search is needed
    search_results = None
    if should_use_search(section, content_type):
        search_results = perform_search(
            search_service, 
            idea, 
            section, 
            content_type
        )
    
    # Generate content with search results
    content = ai_service.generate_section_content_with_search(
        idea_summary=idea,
        section=section,
        content_type=content_type,
        search_results=search_results,
        chat_context=chat_context
    )
    
    # Format content with tables and citations
    formatted_content = ContentFormatter.format_content(
        content, 
        search_results
    )
    
    # ... return response ...
```

### 2. Search Decision Logic

**When to use search:**

- **Research Section:**
  - `local_orgs` → Always search for local organizations
  - `implementation_steps` → Search for tools and platforms
  - `resources` → Search for guides and articles

- **Funding Section:**
  - `grant_proposal` → Search for relevant grants
  - `budget_plan` → Search for cost benchmarks
  - `donor_letter` → Search for similar successful campaigns

- **Team Section:**
  - `recruiting_pitch` → Search for volunteer platforms
  - `job_description` → Search for salary benchmarks

- **Marketing Section:**
  - Generally AI-only, but can search for successful campaign examples

### 3. Prompt Enhancement

**Enhanced System Prompt with Search Results:**

```python
def _get_enhanced_system_prompt(self, idea_summary: Dict, section: str, 
                                search_results: SearchResults) -> str:
    base_prompt = self._get_section_system_prompt(idea_summary, section)
    
    search_context = f"""

SEARCH RESULTS:
You have access to current web search results to provide accurate, up-to-date information.

{self._format_search_results_for_prompt(search_results)}

FORMATTING REQUIREMENTS:
- Use HTML tables for comparative data (organizations, grants, tools)
- Make all URLs clickable with <a href="...">descriptive text</a>
- Include citations at the end with [1], [2], etc. markers
- Use <ul> and <ol> for lists
- Use <strong> for emphasis

IMPORTANT: Base your response on the search results provided. Include specific names, 
URLs, and details from the search results. Do not make up information.
"""
    
    return base_prompt + search_context
```

## Error Handling

### Search Failure Scenarios

1. **API Key Missing/Invalid**
   - Log warning
   - Fall back to AI-only generation
   - Display notice: "Content generated without web search"

2. **Rate Limit Exceeded**
   - Check cache for similar queries
   - Use cached results if available
   - Otherwise fall back to AI-only
   - Log rate limit event

3. **Network Timeout**
   - Retry once with 2-second timeout
   - Fall back to AI-only if retry fails
   - Log timeout event

4. **No Results Found**
   - Log query that returned no results
   - Proceed with AI-only generation
   - AI can mention that specific local information wasn't found

### Error Response Structure

```python
@dataclass
class SearchError:
    error_type: str  # 'rate_limit', 'timeout', 'no_results', 'api_error'
    message: str
    fallback_used: bool
    timestamp: datetime
```

## Testing Strategy

### Unit Tests

1. **Search Service Tests**
   - Test cache hit/miss scenarios
   - Test query formatting
   - Test result parsing
   - Test error handling

2. **Search Provider Tests**
   - Mock API responses
   - Test result parsing for each provider
   - Test error scenarios

3. **Content Formatter Tests**
   - Test table generation
   - Test link formatting
   - Test citation formatting

### Integration Tests

1. **End-to-End Search Flow**
   - Test complete flow from request to formatted response
   - Test with real API (limited, using test account)
   - Test fallback scenarios

2. **Cache Behavior**
   - Test cache expiration
   - Test cache key generation
   - Test concurrent access

### Manual Testing

1. **Content Quality**
   - Verify local organizations are relevant
   - Verify grant information is current
   - Verify links are valid and accessible

2. **Formatting**
   - Verify tables render correctly
   - Verify responsive design on mobile
   - Verify citations are properly linked

## Configuration

### Environment Variables

```bash
# Search Provider Configuration
SEARCH_PROVIDER=brave  # Options: brave, google, bing, none
BRAVE_API_KEY=your_brave_api_key
GOOGLE_SEARCH_API_KEY=your_google_key
GOOGLE_SEARCH_ENGINE_ID=your_engine_id
BING_SEARCH_API_KEY=your_bing_key

# Cache Configuration
SEARCH_CACHE_TTL=86400  # 24 hours in seconds
SEARCH_CACHE_MAX_SIZE=1000  # Maximum cache entries

# Search Behavior
SEARCH_ENABLED=true
SEARCH_TIMEOUT=5  # Seconds
SEARCH_MAX_RESULTS=10
SEARCH_RETRY_ATTEMPTS=1
```

### Provider Selection Logic

```python
def create_search_service() -> Optional[SearchService]:
    provider_name = os.getenv('SEARCH_PROVIDER', 'none')
    
    if provider_name == 'none' or not os.getenv('SEARCH_ENABLED', 'true'):
        return None
        
    if provider_name == 'brave':
        api_key = os.getenv('BRAVE_API_KEY')
        if api_key:
            provider = BraveSearchProvider(api_key)
        else:
            logger.warning("Brave API key not found")
            return None
            
    # ... similar for other providers ...
    
    cache = SearchCache(ttl_seconds=int(os.getenv('SEARCH_CACHE_TTL', 86400)))
    return SearchService(provider, cache)
```

## Performance Considerations

### Caching Strategy

- **Cache Key:** Hash of (query + location + filters)
- **TTL:** 24 hours for most queries
- **Size Limit:** 1000 entries (LRU eviction)
- **Cleanup:** Background task every hour

### API Rate Limits

**Brave Search Free Tier:**
- 2,000 queries/month
- ~66 queries/day
- Implement daily quota tracking

**Mitigation:**
- Aggressive caching
- Batch similar queries
- Fall back to AI-only when approaching limit

### Response Time

- **Target:** < 3 seconds for search + generation
- **Search timeout:** 5 seconds
- **Cache hit:** < 100ms
- **AI generation:** 1-2 seconds

## Security Considerations

1. **API Key Storage**
   - Store in environment variables
   - Never commit to version control
   - Use separate keys for dev/prod

2. **Input Validation**
   - Sanitize search queries
   - Validate location inputs
   - Prevent injection attacks

3. **URL Validation**
   - Verify URLs before including in content
   - Check for malicious domains
   - Use HTTPS when available

4. **Rate Limiting**
   - Track API usage per user session
   - Implement per-user rate limits
   - Prevent abuse

## Migration Plan

### Phase 1: Core Infrastructure
- Implement search service interface
- Implement Brave Search provider
- Implement caching layer
- Add configuration management

### Phase 2: AI Integration
- Modify AI service to accept search results
- Enhance prompts with search context
- Implement fallback logic

### Phase 3: Content Formatting
- Implement content formatter
- Add table generation
- Add citation formatting
- Update CSS for tables

### Phase 4: Testing & Refinement
- Unit tests
- Integration tests
- Manual testing
- Performance optimization

### Phase 5: Additional Providers (Optional)
- Google Custom Search
- Bing Search API
- Provider comparison and selection

## Interactive Content Regeneration

### Overview

Users can request modifications to generated content through the chat interface, and the system will regenerate the upper content area with the requested changes.

### Chat Message Analysis

**New Component: `ChatIntentAnalyzer`**

```python
class ChatIntentAnalyzer:
    @staticmethod
    def detect_regeneration_request(message: str) -> Optional[RegenerationIntent]:
        """
        Analyze chat message to detect if user wants to regenerate content.
        
        Returns RegenerationIntent with:
        - is_regeneration: bool
        - modification_type: 'revise', 'expand', 'shorten', 'reformat'
        - specific_changes: List[str]
        """
```

**Detection Patterns:**
- "change the...", "update the...", "modify the..."
- "make it more...", "make it less..."
- "add...", "remove...", "include..."
- "regenerate", "redo", "rewrite"

### Regeneration Flow

```
User Chat Message
       ↓
ChatIntentAnalyzer
       ↓
   [Is Regeneration Request?]
       ↓ Yes
AI Service (with modification context)
       ↓
New Content Generated
       ↓
Frontend Update (upper content area)
       ↓
Chat Confirmation Message
```

### API Enhancement

**New Endpoint: `/api/regenerate`**

```python
@app.route('/api/regenerate', methods=['POST'])
def regenerate_content():
    """
    Regenerate content based on chat-driven modifications.
    
    Request:
    {
        "idea_id": int,
        "section": str,
        "content_type": str,
        "current_content": str,
        "modification_request": str,
        "chat_history": List[Dict]
    }
    
    Response:
    {
        "success": bool,
        "content": str,
        "message": str  # Confirmation for chat
    }
    """
```

### Frontend Updates

**JavaScript Enhancement:**

```javascript
// Detect regeneration intent in chat response
async function sendMessage() {
    // ... existing code ...
    
    const data = await response.json();
    
    // Check if AI suggests regeneration
    if (data.should_regenerate) {
        await regenerateContent(data.modification_request);
    }
    
    // ... rest of code ...
}

async function regenerateContent(modificationRequest) {
    const display = document.getElementById('content-display');
    const currentContent = display.querySelector('.generated-content').innerHTML;
    
    // Show regenerating indicator
    showRegeneratingIndicator();
    
    const response = await fetch('/api/regenerate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            idea_id: ideaId,
            section: section,
            content_type: currentContentType,
            current_content: currentContent,
            modification_request: modificationRequest,
            chat_history: chatHistory
        })
    });
    
    const data = await response.json();
    
    if (data.success) {
        // Update upper content area
        updateContentDisplay(data.content);
        
        // Add confirmation to chat
        addMessage('assistant', data.message);
    }
}
```

## Content-Type Specific Artifacts

### Overview

Different content types will be rendered with specialized templates and interactive elements to match their real-world format.

### Artifact Templates

**New Component: `ArtifactRenderer`**

```python
class ArtifactRenderer:
    """Render content with type-specific templates."""
    
    @staticmethod
    def render(content: str, content_type: str, data: Dict) -> str:
        """
        Render content using appropriate artifact template.
        
        Returns HTML with embedded interactive elements.
        """
        
    @staticmethod
    def render_email(content: Dict) -> str:
        """Render email with header fields and body."""
        
    @staticmethod
    def render_form(content: Dict) -> str:
        """Render interactive HTML form."""
        
    @staticmethod
    def render_budget(content: Dict) -> str:
        """Render interactive budget spreadsheet."""
        
    @staticmethod
    def render_flyer(content: Dict) -> str:
        """Render visual flyer with design template."""
```

### Artifact Type Definitions

#### 1. Email Artifact

**Template Structure:**
```html
<div class="artifact artifact-email">
    <div class="email-header">
        <div class="email-field">
            <label>From:</label>
            <input type="email" value="{{from_email}}" />
        </div>
        <div class="email-field">
            <label>To:</label>
            <input type="email" value="{{to_email}}" />
        </div>
        <div class="email-field">
            <label>Subject:</label>
            <input type="text" value="{{subject}}" />
        </div>
    </div>
    <div class="email-body">
        <div contenteditable="true">{{body_content}}</div>
    </div>
    <div class="email-actions">
        <button class="copy-btn">Copy Email</button>
        <button class="download-btn">Download</button>
    </div>
</div>
```

#### 2. Form Artifact

**Template Structure:**
```html
<div class="artifact artifact-form">
    <form class="interactive-form">
        <h3>{{form_title}}</h3>
        {{#each fields}}
        <div class="form-group">
            <label>{{label}}</label>
            {{#if (eq type 'text')}}
                <input type="text" name="{{name}}" placeholder="{{placeholder}}" />
            {{else if (eq type 'select')}}
                <select name="{{name}}">
                    {{#each options}}
                    <option value="{{value}}">{{label}}</option>
                    {{/each}}
                </select>
            {{else if (eq type 'textarea')}}
                <textarea name="{{name}}" placeholder="{{placeholder}}"></textarea>
            {{/if}}
        </div>
        {{/each}}
        <button type="submit" class="submit-btn">Submit</button>
    </form>
    <div class="form-actions">
        <button class="copy-html-btn">Copy HTML</button>
        <button class="preview-btn">Preview</button>
    </div>
</div>
```

#### 3. Budget Artifact

**Template Structure:**
```html
<div class="artifact artifact-budget">
    <div class="budget-toolbar">
        <button class="add-row-btn">+ Add Row</button>
        <button class="export-csv-btn">Export CSV</button>
    </div>
    <table class="budget-table">
        <thead>
            <tr>
                <th>Category</th>
                <th>Item</th>
                <th>Quantity</th>
                <th>Unit Cost</th>
                <th>Total</th>
                <th>Notes</th>
            </tr>
        </thead>
        <tbody>
            {{#each budget_items}}
            <tr>
                <td contenteditable="true">{{category}}</td>
                <td contenteditable="true">{{item}}</td>
                <td contenteditable="true" class="number">{{quantity}}</td>
                <td contenteditable="true" class="currency">{{unit_cost}}</td>
                <td class="calculated currency">{{total}}</td>
                <td contenteditable="true">{{notes}}</td>
            </tr>
            {{/each}}
        </tbody>
        <tfoot>
            <tr class="total-row">
                <td colspan="4"><strong>Total Budget</strong></td>
                <td class="calculated currency"><strong>{{grand_total}}</strong></td>
                <td></td>
            </tr>
        </tfoot>
    </table>
</div>

<script>
// Auto-calculate totals when cells are edited
document.querySelectorAll('.budget-table td[contenteditable]').forEach(cell => {
    cell.addEventListener('input', recalculateBudget);
});
</script>
```

#### 4. Flyer Artifact

**Template Structure:**
```html
<div class="artifact artifact-flyer">
    <div class="flyer-canvas" style="background: {{background_color}}">
        <div class="flyer-header">
            <h1 style="color: {{primary_color}}">{{headline}}</h1>
        </div>
        <div class="flyer-body">
            <div class="flyer-image">
                <img src="{{image_url}}" alt="{{image_alt}}" />
            </div>
            <div class="flyer-content">
                {{body_html}}
            </div>
        </div>
        <div class="flyer-footer">
            <div class="contact-info">{{contact_info}}</div>
            <div class="call-to-action">{{cta_text}}</div>
        </div>
    </div>
    <div class="flyer-actions">
        <button class="edit-design-btn">Edit Design</button>
        <button class="download-pdf-btn">Download PDF</button>
    </div>
</div>
```

### AI Prompt Enhancement for Artifacts

**Structured Output Format:**

```python
def _get_artifact_prompt(self, content_type: str) -> str:
    """Get prompt that instructs AI to output structured artifact data."""
    
    artifact_prompts = {
        'email': """
Generate an email in the following JSON format:
{
    "from_email": "organization@example.com",
    "to_email": "recipient@example.com",
    "subject": "Email subject line",
    "body": "Email body content with paragraphs"
}
""",
        'volunteer_form': """
Generate a form structure in the following JSON format:
{
    "form_title": "Volunteer Sign-Up Form",
    "fields": [
        {
            "name": "full_name",
            "label": "Full Name",
            "type": "text",
            "placeholder": "Enter your full name",
            "required": true
        },
        // ... more fields
    ]
}
""",
        'budget_plan': """
Generate a budget in the following JSON format:
{
    "budget_items": [
        {
            "category": "Startup Costs",
            "item": "Website Development",
            "quantity": 1,
            "unit_cost": 2000,
            "notes": "Professional website"
        },
        // ... more items
    ]
}
"""
    }
    
    return artifact_prompts.get(content_type, "")
```

### CSS Styling for Artifacts

**New Stylesheet: `artifacts.css`**

```css
/* Base artifact styles */
.artifact {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    margin: 20px 0;
}

/* Email artifact */
.artifact-email .email-header {
    border-bottom: 2px solid #e0e0e0;
    padding-bottom: 16px;
    margin-bottom: 20px;
}

.artifact-email .email-field {
    display: flex;
    align-items: center;
    margin-bottom: 12px;
}

.artifact-email .email-field label {
    width: 80px;
    font-weight: 600;
}

.artifact-email .email-body {
    min-height: 300px;
    padding: 20px;
    background: #fafafa;
    border-radius: 8px;
}

/* Form artifact */
.artifact-form .form-group {
    margin-bottom: 20px;
}

.artifact-form label {
    display: block;
    font-weight: 600;
    margin-bottom: 8px;
}

.artifact-form input,
.artifact-form select,
.artifact-form textarea {
    width: 100%;
    padding: 12px;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    font-size: 1rem;
}

/* Budget artifact */
.artifact-budget .budget-table {
    width: 100%;
    border-collapse: collapse;
}

.artifact-budget .budget-table th,
.artifact-budget .budget-table td {
    padding: 12px;
    border: 1px solid #e0e0e0;
    text-align: left;
}

.artifact-budget .budget-table th {
    background: #f5f5f5;
    font-weight: 600;
}

.artifact-budget .currency::before {
    content: '$';
}

.artifact-budget .calculated {
    background: #f9f9f9;
    font-weight: 600;
}

/* Flyer artifact */
.artifact-flyer .flyer-canvas {
    width: 8.5in;
    height: 11in;
    margin: 0 auto;
    padding: 40px;
    box-shadow: 0 0 20px rgba(0,0,0,0.15);
}

.artifact-flyer .flyer-header h1 {
    font-size: 3rem;
    text-align: center;
    margin-bottom: 30px;
}

/* Action buttons */
.artifact .artifact-actions,
.email-actions,
.form-actions,
.flyer-actions {
    display: flex;
    gap: 12px;
    margin-top: 20px;
    padding-top: 20px;
    border-top: 1px solid #e0e0e0;
}
```

### Database Schema Update

**Add artifact_data column:**

```sql
ALTER TABLE content ADD COLUMN artifact_data TEXT;
```

This stores the structured JSON data for artifacts, allowing them to be reconstructed on page load.

## Future Enhancements

1. **Advanced Search Features**
   - Date range filtering
   - Domain-specific searches
   - Image search for marketing materials

2. **Machine Learning**
   - Learn which sources are most helpful
   - Personalize search results
   - Improve relevance scoring

3. **Real-time Updates**
   - WebSocket notifications for new grants
   - Deadline reminders
   - Resource recommendations

4. **Collaborative Features**
   - Share search results between users
   - Community-curated resource lists
   - Verified organization database

5. **Advanced Artifact Features**
   - Real-time collaboration on artifacts
   - Version history for content
   - Export to multiple formats (PDF, DOCX, etc.)
   - Template marketplace for flyers and marketing materials
