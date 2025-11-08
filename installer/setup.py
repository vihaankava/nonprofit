"""
Setup script for creating installers
"""
import os
import sys
from pathlib import Path

# Application metadata
APP_NAME = "Nonprofit Idea Coach"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Nonprofit Idea Coach Team"
APP_DESCRIPTION = "AI-powered nonprofit idea development and planning tool"

# Paths
ROOT_DIR = Path(__file__).parent.parent
APP_DIR = ROOT_DIR / "nonprofit_coach"

def get_data_files():
    """Collect all data files to include in the installer"""
    data_files = []
    
    # Templates
    templates = []
    for file in (APP_DIR / "templates").glob("*.html"):
        templates.append(str(file))
    data_files.append(("templates", templates))
    
    # Static files
    static_files = []
    for file in (APP_DIR / "static").glob("*"):
        if file.is_file():
            static_files.append(str(file))
    data_files.append(("static", static_files))
    
    # Search providers
    search_providers = []
    for file in (APP_DIR / "search_providers").glob("*.py"):
        search_providers.append(str(file))
    data_files.append(("search_providers", search_providers))
    
    # Config files
    config_files = [
        str(APP_DIR / ".env.example"),
        str(APP_DIR / "README.md"),
    ]
    data_files.append((".", config_files))
    
    return data_files

def get_python_files():
    """Get all Python source files"""
    python_files = []
    for file in APP_DIR.glob("*.py"):
        if file.name not in ["test_ai_service.py", "test_integration.py"]:
            python_files.append(str(file))
    return python_files

if __name__ == "__main__":
    print(f"Building {APP_NAME} v{APP_VERSION}")
    print(f"Platform: {sys.platform}")
    print(f"Python: {sys.version}")
