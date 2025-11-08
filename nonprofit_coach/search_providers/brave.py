"""
Brave Search API provider implementation.

This module implements the SearchProvider interface for Brave Search API,
providing web search capabilities with result parsing and error handling.
"""

import requests
import logging
import time
from typing import Dict, Optional
from datetime import datetime
from .base import SearchProvider
from search_service import SearchResults, SearchResult

# Configure logging
logger = logging.getLogger(__name__)


class SearchError(Exception):
    """Custom exception for search-related errors."""
    
    def __init__(self, message: str, error_type: str, original_error: Optional[Exception] = None):
        """
        Initialize SearchError.
        
        Args:
            message: Error message
            error_type: Type of error ('timeout', 'rate_limit', 'api_error', 'network_error')
            original_error: Original exception that caused this error
        """
        super().__init__(message)
        self.error_type = error_type
        self.original_error = original_error
        self.timestamp = datetime.now()


class BraveSearchProvider(SearchProvider):
    """
    Brave Search API implementation.
    
    Provides web search functionality using the Brave Search API
    with support for location-based queries and result filtering.
    """
    
    def __init__(self, api_key: str, timeout: int = 5, max_results: int = 10):
        """
        Initialize Brave Search provider.
        
        Args:
            api_key: Brave Search API key
            timeout: Request timeout in seconds (default: 5)
            max_results: Maximum number of results to return (default: 10)
        """
        self.api_key = api_key
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self.timeout = timeout
        self.max_results = max_results
    
    def search(self, query: str, params: Dict) -> Dict:
        """
        Execute search query via Brave Search API with retry logic.
        
        Implements exponential backoff retry for transient failures
        and comprehensive error handling.
        
        Args:
            query: The search query string
            params: Dictionary of search parameters (location, count, etc.)
            
        Returns:
            Dictionary containing raw API response
            
        Raises:
            SearchError: If the search fails after retries
        """
        max_retries = 1  # One retry as per requirements
        retry_delay = 1  # Initial delay in seconds
        
        for attempt in range(max_retries + 1):
            try:
                return self._execute_search(query, params)
                
            except requests.exceptions.Timeout as e:
                error_msg = f"Search request timed out after {self.timeout} seconds"
                logger.warning(f"{error_msg} (attempt {attempt + 1}/{max_retries + 1})")
                
                if attempt < max_retries:
                    # Exponential backoff
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    logger.error(f"Search failed after {max_retries + 1} attempts: {error_msg}")
                    raise SearchError(error_msg, 'timeout', e)
            
            except requests.exceptions.HTTPError as e:
                # Check for rate limiting (429) or other HTTP errors
                if e.response.status_code == 429:
                    error_msg = "API rate limit exceeded"
                    logger.error(f"{error_msg}: {e}")
                    raise SearchError(error_msg, 'rate_limit', e)
                elif e.response.status_code == 401:
                    error_msg = "Invalid API key"
                    logger.error(f"{error_msg}: {e}")
                    raise SearchError(error_msg, 'api_error', e)
                else:
                    error_msg = f"HTTP error {e.response.status_code}"
                    logger.error(f"{error_msg}: {e}")
                    
                    if attempt < max_retries:
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        raise SearchError(error_msg, 'api_error', e)
            
            except requests.exceptions.RequestException as e:
                error_msg = f"Network error during search request"
                logger.warning(f"{error_msg} (attempt {attempt + 1}/{max_retries + 1}): {e}")
                
                if attempt < max_retries:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    logger.error(f"Search failed after {max_retries + 1} attempts: {error_msg}")
                    raise SearchError(error_msg, 'network_error', e)
            
            except Exception as e:
                error_msg = f"Unexpected error during search"
                logger.error(f"{error_msg}: {e}")
                raise SearchError(error_msg, 'api_error', e)
        
        # Should never reach here, but just in case
        raise SearchError("Search failed for unknown reason", 'api_error', None)
    
    def _execute_search(self, query: str, params: Dict) -> Dict:
        """
        Execute a single search request without retry logic.
        
        Args:
            query: The search query string
            params: Dictionary of search parameters
            
        Returns:
            Dictionary containing raw API response
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        # Build request headers
        headers = {
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip',
            'X-Subscription-Token': self.api_key
        }
        
        # Build query parameters
        query_params = {
            'q': query,
            'count': params.get('count', self.max_results)
        }
        
        # Add location if provided
        if 'location' in params and params['location']:
            query_params['search_lang'] = 'en'
            # Brave uses the query itself for location context
            # The location is already in the query string
        
        # Add any additional filters
        if 'freshness' in params:
            query_params['freshness'] = params['freshness']
        
        logger.info(f"Executing Brave Search: query='{query}', params={query_params}")
        
        # Make API request
        response = requests.get(
            self.base_url,
            headers=headers,
            params=query_params,
            timeout=self.timeout
        )
        
        # Raise exception for bad status codes
        response.raise_for_status()
        
        # Return JSON response
        return response.json()
    
    def parse_results(self, raw_results: Dict) -> SearchResults:
        """
        Parse Brave API response into SearchResults format.
        
        Args:
            raw_results: Raw JSON response from Brave Search API
            
        Returns:
            SearchResults object with standardized format
        """
        # Extract web results
        web_results = raw_results.get('web', {}).get('results', [])
        
        # Parse individual results
        parsed_results = []
        for item in web_results:
            result = SearchResult(
                title=item.get('title', ''),
                url=item.get('url', ''),
                snippet=item.get('description', ''),
                domain=self._extract_domain(item.get('url', '')),
                relevance_score=None  # Brave doesn't provide explicit scores
            )
            parsed_results.append(result)
        
        # Create SearchResults object
        search_results = SearchResults(
            query=raw_results.get('query', {}).get('original', ''),
            results=parsed_results,
            total_results=len(parsed_results),
            search_time=0.0,  # Brave doesn't provide search time
            timestamp=datetime.now()
        )
        
        logger.info(f"Parsed {len(parsed_results)} results from Brave Search")
        
        return search_results
    
    def is_available(self) -> bool:
        """
        Check if Brave Search provider is configured and available.
        
        Returns:
            True if API key is configured, False otherwise
        """
        is_configured = (
            self.api_key is not None and 
            self.api_key != '' and 
            self.api_key != 'your_brave_api_key_here'
        )
        
        if not is_configured:
            logger.warning("Brave Search API key not configured")
        
        return is_configured
    
    def search_local_organizations(self, cause: str, location: str, 
                                   count: int = 10) -> Dict:
        """
        Search for local organizations with location filtering.
        
        Constructs a query optimized for finding local nonprofits,
        community organizations, and support networks.
        
        Args:
            cause: The nonprofit's cause or focus area
            location: Geographic location to search
            count: Number of results to return
            
        Returns:
            Raw API response dictionary
        """
        # Construct location-specific query
        query = f"{cause} nonprofit organizations community resources near {location}"
        
        params = {
            'count': count,
            'location': location
        }
        
        logger.info(f"Searching local organizations: cause='{cause}', location='{location}'")
        
        return self.search(query, params)
    
    def search_grants(self, cause: str, location: Optional[str] = None,
                     count: int = 10) -> Dict:
        """
        Search for grant opportunities with funding-specific queries.
        
        Constructs queries optimized for finding current grant opportunities,
        funding sources, and application information.
        
        Args:
            cause: The nonprofit's cause or focus area
            location: Optional geographic location for local grants
            count: Number of results to return
            
        Returns:
            Raw API response dictionary
        """
        # Construct grant-specific query
        location_str = f"in {location}" if location else ""
        query = f"{cause} grants funding opportunities nonprofit {location_str} 2024 2025"
        
        params = {
            'count': count,
            'freshness': 'py'  # Past year for current opportunities
        }
        
        if location:
            params['location'] = location
        
        logger.info(f"Searching grants: cause='{cause}', location='{location}'")
        
        return self.search(query, params)
    
    def search_resources(self, topic: str, count: int = 5) -> Dict:
        """
        Search for tools, platforms, and resources.
        
        Constructs queries optimized for finding software tools,
        platforms, guides, and educational resources for nonprofits.
        
        Args:
            topic: Topic or type of resource to search for
            count: Number of results to return
            
        Returns:
            Raw API response dictionary
        """
        # Construct resource-specific query
        query = f"{topic} tools platforms software resources for nonprofits best"
        
        params = {
            'count': count
        }
        
        logger.info(f"Searching resources: topic='{topic}'")
        
        return self.search(query, params)
    
    def _extract_domain(self, url: str) -> str:
        """
        Extract domain from URL.
        
        Args:
            url: Full URL string
            
        Returns:
            Domain name (e.g., 'example.com')
        """
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc
        except Exception:
            return ''
