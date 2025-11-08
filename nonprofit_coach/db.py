import sqlite3
import os
from datetime import datetime
from typing import Optional, Dict, List, Any

DB_PATH = os.path.join(os.path.dirname(__file__), 'nonprofit.db')


def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the database with required tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create ideas table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ideas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            importance TEXT,
            beneficiaries TEXT,
            implementation TEXT,
            significance TEXT,
            uniqueness TEXT,
            location TEXT,
            api_key TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'draft'
        )
    ''')
    
    # Create content table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idea_id INTEGER NOT NULL,
            section TEXT NOT NULL,
            content_type TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (idea_id) REFERENCES ideas (id)
        )
    ''')
    
    # Create volunteers table (optional)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS volunteers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idea_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            address TEXT,
            task TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (idea_id) REFERENCES ideas (id)
        )
    ''')
    
    conn.commit()
    conn.close()


def save_idea(idea_data: Dict[str, Any]) -> int:
    """
    Save a new idea or update an existing one.
    
    Args:
        idea_data: Dictionary containing idea fields
        
    Returns:
        The ID of the saved idea
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if 'id' in idea_data and idea_data['id']:
        # Update existing idea
        cursor.execute('''
            UPDATE ideas 
            SET title = ?, description = ?, importance = ?, 
                beneficiaries = ?, implementation = ?, significance = ?, 
                uniqueness = ?, location = ?, api_key = ?, status = ?
            WHERE id = ?
        ''', (
            idea_data.get('title', ''),
            idea_data.get('description', ''),
            idea_data.get('importance', ''),
            idea_data.get('beneficiaries', ''),
            idea_data.get('implementation', ''),
            idea_data.get('significance', ''),
            idea_data.get('uniqueness', ''),
            idea_data.get('location', ''),
            idea_data.get('api_key'),
            idea_data.get('status', 'draft'),
            idea_data['id']
        ))
        idea_id = idea_data['id']
    else:
        # Insert new idea
        cursor.execute('''
            INSERT INTO ideas (title, description, importance, beneficiaries, 
                             implementation, significance, uniqueness, location, api_key, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            idea_data.get('title', ''),
            idea_data.get('description', ''),
            idea_data.get('importance', ''),
            idea_data.get('beneficiaries', ''),
            idea_data.get('implementation', ''),
            idea_data.get('significance', ''),
            idea_data.get('uniqueness', ''),
            idea_data.get('location', ''),
            idea_data.get('api_key'),
            idea_data.get('status', 'draft')
        ))
        idea_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return idea_id


def get_idea_by_id(idea_id: int) -> Optional[Dict[str, Any]]:
    """
    Retrieve an idea by its ID.
    
    Args:
        idea_id: The ID of the idea to retrieve
        
    Returns:
        Dictionary containing idea data or None if not found
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM ideas WHERE id = ?', (idea_id,))
    row = cursor.fetchone()
    
    conn.close()
    
    if row:
        return dict(row)
    return None


def get_all_ideas() -> List[Dict[str, Any]]:
    """
    Retrieve all ideas ordered by creation date (newest first).
    
    Returns:
        List of dictionaries containing idea data
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM ideas ORDER BY created_at DESC')
    rows = cursor.fetchall()
    
    conn.close()
    
    return [dict(row) for row in rows]


def save_content(idea_id: int, section: str, content_type: str, content: str) -> int:
    """
    Save generated content for an idea.
    
    Args:
        idea_id: The ID of the associated idea
        section: The section name (marketing, team, funding, research)
        content_type: The type of content (email, flyer, etc.)
        content: The generated content text
        
    Returns:
        The ID of the saved content
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO content (idea_id, section, content_type, content)
        VALUES (?, ?, ?, ?)
    ''', (idea_id, section, content_type, content))
    
    content_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return content_id


def get_content_by_idea_and_section(idea_id: int, section: str, content_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieve content for a specific idea and section.
    
    Args:
        idea_id: The ID of the idea
        section: The section name (marketing, team, funding, research)
        content_type: Optional content type filter
        
    Returns:
        List of dictionaries containing content data
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if content_type:
        cursor.execute('''
            SELECT * FROM content 
            WHERE idea_id = ? AND section = ? AND content_type = ?
            ORDER BY created_at DESC
        ''', (idea_id, section, content_type))
    else:
        cursor.execute('''
            SELECT * FROM content 
            WHERE idea_id = ? AND section = ?
            ORDER BY created_at DESC
        ''', (idea_id, section))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def save_volunteer(idea_id: int, volunteer_data: Dict[str, Any]) -> int:
    """
    Save volunteer information.
    
    Args:
        idea_id: The ID of the associated idea
        volunteer_data: Dictionary containing volunteer fields
        
    Returns:
        The ID of the saved volunteer
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO volunteers (idea_id, name, email, phone, address, task)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        idea_id,
        volunteer_data.get('name', ''),
        volunteer_data.get('email', ''),
        volunteer_data.get('phone', ''),
        volunteer_data.get('address', ''),
        volunteer_data.get('task', '')
    ))
    
    volunteer_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return volunteer_id


def get_volunteers_by_idea(idea_id: int) -> List[Dict[str, Any]]:
    """
    Retrieve all volunteers for a specific idea.
    
    Args:
        idea_id: The ID of the idea
        
    Returns:
        List of dictionaries containing volunteer data
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM volunteers 
        WHERE idea_id = ?
        ORDER BY created_at DESC
    ''', (idea_id,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def delete_idea(idea_id: int) -> bool:
    """
    Delete an idea and all associated content and volunteers.
    
    Args:
        idea_id: The ID of the idea to delete
        
    Returns:
        True if successful, False otherwise
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Delete associated content
        cursor.execute('DELETE FROM content WHERE idea_id = ?', (idea_id,))
        
        # Delete associated volunteers
        cursor.execute('DELETE FROM volunteers WHERE idea_id = ?', (idea_id,))
        
        # Delete the idea
        cursor.execute('DELETE FROM ideas WHERE id = ?', (idea_id,))
        
        conn.commit()
        conn.close()
        
        return True
    except Exception as e:
        print(f"Error deleting idea: {e}")
        return False


# Initialize database on module import
init_db()
