"""
Search Service for integrating web search capabilities into content generation.

This module provides a unified interface for searching the web using various
search providers (Brave, Google, Bing) with caching support.
"""

from typing import Optional, Dict, List
from dataclasses import dataclass
from datetime import datetime
from abc import ABC, abstractmethod


@dataclass
class SearchResult:
    """Individual search result from a search provider."""
    title: str
    url: str
    snippet: str
    domain: str
    relevance_score: Optional[float] = None


@dataclass
class SearchResults:
    """Collection of search results with metadata."""
    query: str
    results: List[SearchResult]
    total_results: int
    search_time: float
    timestamp: datetime


@dataclass
class Organization:
    """Local organization or nonprofit resource."""
    name: str
    description: str
    website: Optional[str]
    location: str
    contact: Optional[str]
    relevance: str  # Why it's relevant to the nonprofit


@dataclass
class Grant:
    """Grant opportunity information."""
    name: str
    funder: str
    amount: Optional[str]
    deadline: Optional[str]
    eligibility: str
    application_url: str
    description: str


@dataclass
class Resource:
    """Tool, platform, or educational resource."""
    title: str
    url: str
    description: str
    resource_type: str  # 'tool', 'guide', 'platform', 'article'
    cost: Optional[str]  # 'free', 'paid', 'freemium'


class SearchService:
    """
    Orchestrates web searches with caching and provider management.
    
    This service provides a unified interface for searching the web,
    managing cache, and formatting results for content generation.
    """
    
    def __init__(self, provider, cache):
        """
        Initialize SearchService with a provider and cache.
        
        Args:
            provider: SearchProvider instance (e.g., BraveSearchProvider)
            cache: SearchCache instance for result caching
        """
        self.provider = provider
        self.cache = cache
    
    def search(self, query: str, location: Optional[str] = None, 
               filters: Optional[Dict] = None) -> Optional[SearchResults]:
        """
        Execute a search query with optional location and filters.
        
        Args:
            query: Search query string
            location: Optional geographic location for local results
            filters: Optional dictionary of search filters
            
        Returns:
            SearchResults object or None if search fails
        """
        # Generate cache key
        cache_key = self.cache.generate_key(query, {
            'location': location,
            'filters': filters
        })
        
        # Check cache first
        cached_results = self.cache.get(cache_key)
        if cached_results:
            return cached_results
        
        # Check if provider is available
        if not self.provider.is_available():
            return None
        
        # Build search parameters
        params = filters or {}
        if location:
            params['location'] = location
        
        try:
            # Execute search
            raw_results = self.provider.search(query, params)
            
            # Parse results
            search_results = self.provider.parse_results(raw_results)
            
            # Cache results
            self.cache.set(cache_key, search_results)
            
            return search_results
            
        except Exception as e:
            # Log the error with details
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Search failed for query '{query}': {type(e).__name__}: {e}")
            
            # Return None to trigger fallback to AI-only generation
            return None
    
    def search_local_organizations(self, cause: str, location: str, 
                                   limit: int = 10) -> List[Organization]:
        """
        Search for local nonprofit organizations and community resources.
        
        Args:
            cause: The nonprofit's cause or focus area
            location: Geographic location to search
            limit: Maximum number of results
            
        Returns:
            List of Organization objects
        """
        query = f"{cause} nonprofit organizations near {location}"
        results = self.search(query, location=location, filters={'count': limit})
        
        if not results:
            return []
        
        # Convert search results to Organization objects
        organizations = []
        for result in results.results[:limit]:
            org = Organization(
                name=result.title,
                description=result.snippet,
                website=result.url,
                location=location,
                contact=None,  # Would need additional parsing
                relevance=f"Related to {cause}"
            )
            organizations.append(org)
        
        return organizations
    
    def search_grants(self, cause: str, location: Optional[str] = None,
                     limit: int = 10) -> List[Grant]:
        """
        Search for current grant opportunities relevant to the cause.
        
        Args:
            cause: The nonprofit's cause or focus area
            location: Optional geographic location for local grants
            limit: Maximum number of results
            
        Returns:
            List of Grant objects
        """
        location_str = f"in {location}" if location else ""
        query = f"{cause} grants funding opportunities {location_str}"
        results = self.search(query, location=location, filters={'count': limit})
        
        if not results:
            return []
        
        # Convert search results to Grant objects
        grants = []
        for result in results.results[:limit]:
            grant = Grant(
                name=result.title,
                funder="See website for details",
                amount=None,  # Would need additional parsing
                deadline=None,  # Would need additional parsing
                eligibility=result.snippet,
                application_url=result.url,
                description=result.snippet
            )
            grants.append(grant)
        
        return grants
    
    def search_resources(self, topic: str, limit: int = 5) -> List[Resource]:
        """
        Search for tools, platforms, and educational resources.
        
        Args:
            topic: Topic or type of resource to search for
            limit: Maximum number of results
            
        Returns:
            List of Resource objects
        """
        query = f"{topic} tools platforms resources for nonprofits"
        results = self.search(query, filters={'count': limit})
        
        if not results:
            return []
        
        # Convert search results to Resource objects
        resources = []
        for result in results.results[:limit]:
            resource = Resource(
                title=result.title,
                url=result.url,
                description=result.snippet,
                resource_type='platform',  # Would need classification logic
                cost=None  # Would need additional parsing
            )
            resources.append(resource)
        
        return resources
