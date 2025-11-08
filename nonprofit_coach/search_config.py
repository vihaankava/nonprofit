"""
Search service configuration and validation.

This module handles configuration loading, validation, and
search service initialization for the application.
"""

import os
import logging
from typing import Optional
from search_service import SearchService
from search_cache import SearchCache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SearchConfig:
    """Configuration manager for search service."""
    
    def __init__(self):
        """Load configuration from environment variables."""
        self.provider_name = os.getenv('SEARCH_PROVIDER', 'none').lower()
        self.enabled = os.getenv('SEARCH_ENABLED', 'true').lower() == 'true'
        
        # API Keys
        self.brave_api_key = os.getenv('BRAVE_API_KEY')
        self.google_api_key = os.getenv('GOOGLE_SEARCH_API_KEY')
        self.google_engine_id = os.getenv('GOOGLE_SEARCH_ENGINE_ID')
        self.bing_api_key = os.getenv('BING_SEARCH_API_KEY')
        
        # Cache configuration
        self.cache_ttl = int(os.getenv('SEARCH_CACHE_TTL', '86400'))
        self.cache_max_size = int(os.getenv('SEARCH_CACHE_MAX_SIZE', '1000'))
        
        # Search behavior
        self.timeout = int(os.getenv('SEARCH_TIMEOUT', '5'))
        self.max_results = int(os.getenv('SEARCH_MAX_RESULTS', '10'))
        self.retry_attempts = int(os.getenv('SEARCH_RETRY_ATTEMPTS', '1'))
    
    def validate(self) -> bool:
        """
        Validate search configuration.
        
        Returns:
            True if configuration is valid, False otherwise
        """
        if not self.enabled:
            logger.info("Search service is disabled")
            return True
        
        if self.provider_name == 'none':
            logger.info("No search provider configured, search will be disabled")
            return True
        
        # Validate provider-specific configuration
        if self.provider_name == 'brave':
            if not self.brave_api_key or self.brave_api_key == 'your_brave_api_key_here':
                logger.warning("Brave Search API key not configured. Search will be disabled.")
                return False
            logger.info("Brave Search provider configured successfully")
            return True
        
        elif self.provider_name == 'google':
            if not self.google_api_key or not self.google_engine_id:
                logger.warning("Google Search API key or Engine ID not configured. Search will be disabled.")
                return False
            logger.info("Google Search provider configured successfully")
            return True
        
        elif self.provider_name == 'bing':
            if not self.bing_api_key:
                logger.warning("Bing Search API key not configured. Search will be disabled.")
                return False
            logger.info("Bing Search provider configured successfully")
            return True
        
        else:
            logger.warning(f"Unknown search provider: {self.provider_name}. Search will be disabled.")
            return False
    
    def get_provider_info(self) -> dict:
        """
        Get information about the configured provider.
        
        Returns:
            Dictionary with provider configuration details
        """
        return {
            'provider': self.provider_name,
            'enabled': self.enabled,
            'cache_ttl': self.cache_ttl,
            'cache_max_size': self.cache_max_size,
            'timeout': self.timeout,
            'max_results': self.max_results
        }


def create_search_service() -> Optional[SearchService]:
    """
    Create and configure a search service instance.
    
    Returns:
        SearchService instance if configured, None otherwise
    """
    config = SearchConfig()
    
    # Validate configuration
    if not config.validate():
        logger.info("Search service not available due to configuration issues")
        return None
    
    # If disabled or no provider, return None
    if not config.enabled or config.provider_name == 'none':
        return None
    
    # Import provider based on configuration
    provider = None
    
    if config.provider_name == 'brave':
        try:
            from search_providers.brave import BraveSearchProvider
            provider = BraveSearchProvider(
                api_key=config.brave_api_key,
                timeout=config.timeout,
                max_results=config.max_results
            )
        except ImportError:
            logger.error("BraveSearchProvider not found. Install required dependencies.")
            return None
    
    elif config.provider_name == 'google':
        try:
            from search_providers.google import GoogleSearchProvider
            provider = GoogleSearchProvider(
                api_key=config.google_api_key,
                engine_id=config.google_engine_id,
                timeout=config.timeout,
                max_results=config.max_results
            )
        except ImportError:
            logger.error("GoogleSearchProvider not found. Install required dependencies.")
            return None
    
    elif config.provider_name == 'bing':
        try:
            from search_providers.bing import BingSearchProvider
            provider = BingSearchProvider(
                api_key=config.bing_api_key,
                timeout=config.timeout,
                max_results=config.max_results
            )
        except ImportError:
            logger.error("BingSearchProvider not found. Install required dependencies.")
            return None
    
    if not provider:
        return None
    
    # Create cache
    cache = SearchCache(
        ttl_seconds=config.cache_ttl,
        max_size=config.cache_max_size
    )
    
    # Create and return search service
    search_service = SearchService(provider, cache)
    logger.info(f"Search service initialized with {config.provider_name} provider")
    
    return search_service


def validate_search_config_on_startup():
    """
    Validate search configuration on application startup.
    
    This function should be called when the Flask app starts
    to ensure search configuration is valid and log any issues.
    """
    config = SearchConfig()
    
    logger.info("=" * 60)
    logger.info("Search Service Configuration")
    logger.info("=" * 60)
    
    info = config.get_provider_info()
    for key, value in info.items():
        logger.info(f"  {key}: {value}")
    
    is_valid = config.validate()
    
    if is_valid and config.enabled and config.provider_name != 'none':
        logger.info("✓ Search service is configured and ready")
    elif not config.enabled or config.provider_name == 'none':
        logger.info("ℹ Search service is disabled")
    else:
        logger.warning("✗ Search service configuration has issues")
    
    logger.info("=" * 60)
    
    return is_valid
