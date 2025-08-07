#!/usr/bin/env bash

# Exit on error
set -e

echo "🔄 Activating virtual environment..."
source .venv/Scripts/activate  # For Windows Git Bash / WSL

# Optional: export environment variables
export APP_ENV=development
export DATABASE_URL=your_database_url_here

echo "🚀 Starting FastAPI server with Uvicorn..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
