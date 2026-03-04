"""
Pytest configuration file.
This file is automatically loaded by pytest and configures the test environment.
"""

import sys
from pathlib import Path

# Add the project root to sys.path so tests can import modules
project_root = Path(__file__).parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))