#!/usr/bin/env python3
"""
Python Backend Server Startup Script
"""
import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

if __name__ == '__main__':
    print("🐍 Starting Python Backend Server...")
    print("📡 API endpoints will be available at:")
    print("   - Health: http://localhost:5000/api/health")
    print("   - Users: http://localhost:5000/api/users") 
    print("   - Process: http://localhost:5000/api/process")
    print("   - Predict: http://localhost:5000/api/predict")
    print()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
