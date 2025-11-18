# __init__.py

# Makes this folder a Python package
# Adds the folder to Python path automatically (for nested imports)

import os
import sys

# Get the absolute path of this directory
package_path = os.path.dirname(os.path.abspath(__file__))

# Add this path to sys.path if not already present
if package_path not in sys.path:
    sys.path.append(package_path)

