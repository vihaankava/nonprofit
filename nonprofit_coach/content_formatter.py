"""
Content Formatter for search-enhanced content generation.

This module provides utilities for formatting AI-generated content with
HTML tables, citations, and clickable links based on search results.
"""

import re
from typing import List, Optional
from search_service import Organization, Grant, Resource, SearchResults


class ContentFormatter:
    """
    Utilities for formatting content with tables, citations, and links.
    
    This class provides static methods to enhance AI-generated content
    with structured HTML elements based on search results.
    """
    
    @staticmethod
    def format_with_tables(content: str, data: List, table_type: str) -> str:
        """
        Insert HTML tables into content based on data type.
        
        Args:
            content: The AI-generated content string
            data: List of data objects (Organization, Grant, or Resource)
            table_type: Type of table ('organization', 'grant', 'resource')
            
        Returns:
            Content with embedded HTML table
        """
        if not data:
            return content
        
        # Generate appropriate table based on type
        if table_type == 'organization':
            table_html = ContentFormatter.format_organization_table(data)
        elif table_type == 'grant':
            table_html = ContentFormatter.format_grant_table(data)
        elif table_type == 'resource':
            table_html = ContentFormatter.format_resource_table(data)
        else:
            return content
        
        # Insert table at the end of content or before citations
        if '## Sources' in content or '## Citations' in content:
            # Insert before citations section
            content = re.sub(
                r'(## (?:Sources|Citations))',
                f'\n\n{table_html}\n\n\\1',
                content,
                count=1
            )
        else:
            # Append to end
            content = f"{content}\n\n{table_html}"
        
        return content
    
    @staticmethod
    def add_citations(content: str, sources: List[SearchResults]) -> str:
        """
        Append citation section with source links.
        
        Args:
            content: The AI-generated content string
            sources: List of SearchResults objects used in generation
            
        Returns:
            Content with citations section appended
        """
        if not sources:
            return content
        
        # Build citations section
        citations_html = '\n\n<div class="citations">\n<h3>Sources</h3>\n<ol class="citation-list">\n'
        
        citation_num = 1
        for source in sources:
            if hasattr(source, 'results'):
                for result in source.results[:5]:  # Limit to top 5 per source
                    citations_html += f'  <li>\n'
                    citations_html += f'    <a href="{result.url}" target="_blank" rel="noopener noreferrer">{result.title}</a>\n'
                    citations_html += f'    <p class="citation-snippet">{result.snippet}</p>\n'
                    citations_html += f'  </li>\n'
                    citation_num += 1
        
        citations_html += '</ol>\n</div>\n'
        
        return content + citations_html
    
    @staticmethod
    def ensure_links_clickable(content: str) -> str:
        """
        Convert plain URLs to HTML anchor tags.
        
        Args:
            content: The content string that may contain plain URLs
            
        Returns:
            Content with URLs converted to clickable links
        """
        # Pattern to match URLs that aren't already in anchor tags
        # This looks for http(s):// URLs not preceded by href=" or >
        url_pattern = r'(?<!href=")(?<!>)(https?://[^\s<>"]+)'
        
        def replace_url(match):
            url = match.group(1)
            # Clean up trailing punctuation
            url = url.rstrip('.,;:!?)')
            return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>'
        
        content = re.sub(url_pattern, replace_url, content)
        
        return content
    
    @staticmethod
    def format_organization_table(orgs: List[Organization]) -> str:
        """
        Create HTML table for local organizations.
        
        Args:
            orgs: List of Organization objects
            
        Returns:
            HTML table string with responsive classes
        """
        if not orgs:
            return ""
        
        html = '<div class="table-wrapper">\n'
        html += '<table class="search-table organization-table">\n'
        html += '  <caption>Local Organizations and Resources</caption>\n'
        html += '  <thead>\n'
        html += '    <tr>\n'
        html += '      <th>Organization</th>\n'
        html += '      <th>Description</th>\n'
        html += '      <th>Location</th>\n'
        html += '      <th>Website</th>\n'
        html += '    </tr>\n'
        html += '  </thead>\n'
        html += '  <tbody>\n'
        
        for org in orgs:
            html += '    <tr>\n'
            html += f'      <td class="org-name">{ContentFormatter._escape_html(org.name)}</td>\n'
            html += f'      <td class="org-description">{ContentFormatter._escape_html(org.description)}</td>\n'
            html += f'      <td class="org-location">{ContentFormatter._escape_html(org.location)}</td>\n'
            
            if org.website:
                html += f'      <td class="org-website"><a href="{org.website}" target="_blank" rel="noopener noreferrer">Visit Website</a></td>\n'
            else:
                html += '      <td class="org-website">N/A</td>\n'
            
            html += '    </tr>\n'
        
        html += '  </tbody>\n'
        html += '</table>\n'
        html += '</div>\n'
        
        return html
    
    @staticmethod
    def format_grant_table(grants: List[Grant]) -> str:
        """
        Create HTML table for funding opportunities.
        
        Args:
            grants: List of Grant objects
            
        Returns:
            HTML table string with responsive classes
        """
        if not grants:
            return ""
        
        html = '<div class="table-wrapper">\n'
        html += '<table class="search-table grant-table">\n'
        html += '  <caption>Grant Opportunities</caption>\n'
        html += '  <thead>\n'
        html += '    <tr>\n'
        html += '      <th>Grant Name</th>\n'
        html += '      <th>Funder</th>\n'
        html += '      <th>Amount</th>\n'
        html += '      <th>Deadline</th>\n'
        html += '      <th>Application</th>\n'
        html += '    </tr>\n'
        html += '  </thead>\n'
        html += '  <tbody>\n'
        
        for grant in grants:
            html += '    <tr>\n'
            html += f'      <td class="grant-name">{ContentFormatter._escape_html(grant.name)}</td>\n'
            html += f'      <td class="grant-funder">{ContentFormatter._escape_html(grant.funder)}</td>\n'
            html += f'      <td class="grant-amount">{ContentFormatter._escape_html(grant.amount or "Varies")}</td>\n'
            html += f'      <td class="grant-deadline">{ContentFormatter._escape_html(grant.deadline or "See website")}</td>\n'
            html += f'      <td class="grant-link"><a href="{grant.application_url}" target="_blank" rel="noopener noreferrer">Apply</a></td>\n'
            html += '    </tr>\n'
        
        html += '  </tbody>\n'
        html += '</table>\n'
        html += '</div>\n'
        
        return html
    
    @staticmethod
    def format_resource_table(resources: List[Resource]) -> str:
        """
        Create HTML table for tools and platforms.
        
        Args:
            resources: List of Resource objects
            
        Returns:
            HTML table string with responsive classes
        """
        if not resources:
            return ""
        
        html = '<div class="table-wrapper">\n'
        html += '<table class="search-table resource-table">\n'
        html += '  <caption>Tools and Resources</caption>\n'
        html += '  <thead>\n'
        html += '    <tr>\n'
        html += '      <th>Resource</th>\n'
        html += '      <th>Description</th>\n'
        html += '      <th>Type</th>\n'
        html += '      <th>Cost</th>\n'
        html += '      <th>Link</th>\n'
        html += '    </tr>\n'
        html += '  </thead>\n'
        html += '  <tbody>\n'
        
        for resource in resources:
            html += '    <tr>\n'
            html += f'      <td class="resource-title">{ContentFormatter._escape_html(resource.title)}</td>\n'
            html += f'      <td class="resource-description">{ContentFormatter._escape_html(resource.description)}</td>\n'
            html += f'      <td class="resource-type">{ContentFormatter._escape_html(resource.resource_type.title())}</td>\n'
            html += f'      <td class="resource-cost">{ContentFormatter._escape_html(resource.cost or "Unknown")}</td>\n'
            html += f'      <td class="resource-link"><a href="{resource.url}" target="_blank" rel="noopener noreferrer">Visit</a></td>\n'
            html += '    </tr>\n'
        
        html += '  </tbody>\n'
        html += '</table>\n'
        html += '</div>\n'
        
        return html
    
    @staticmethod
    def _escape_html(text: str) -> str:
        """
        Escape HTML special characters to prevent XSS.
        
        Args:
            text: Text to escape
            
        Returns:
            HTML-escaped text
        """
        if not text:
            return ""
        
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))
