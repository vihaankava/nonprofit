"""
Base search provider interface.

All search providers must implement this abstract interface to ensure
consistent behavior across different search APIs.
"""

from abc import ABC, abstractmethod
from typing import Dict


class SearchProvider(ABC):
    """
    Abstract base class for search providers.
    
    All search provider implementations (Brave, Google, Bing) must
    inherit from this class and implement its abstract methods.
    """
    
    @abstractmethod
    def search(self, query: str, params: Dict) -> Dict:
        """
        Execute a search query and return raw results.
        
        Args:
            query: The search query string
            params: Dictionary of search parameters (location, filters, etc.)
            
        Returns:
            Dictionary containing raw search results from the provider
            
        Raises:
            Exception: If the search fails or times out
        """
        pass
    
    @abstractmethod
    def parse_results(self, raw_results: Dict):
        """
        Parse provider-specific results into standard SearchResults format.
        
        Args:
            raw_results: Raw results dictionary from the provider's API
            
        Returns:
            SearchResults object with standardized format
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the provider is configured and available.
        
        Returns:
            True if the provider has valid configuration (API key, etc.)
            and is ready to use, False otherwise
        """
        pass
