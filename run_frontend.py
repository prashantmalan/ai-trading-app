import sys
import os

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Now import and run the frontend
import streamlit as st
from frontend.main import main

if __name__ == "__main__":
    main()
