#!/bin/bash

# Path to your project directory
PROJECT_DIR="/home/ec2-user/your-project-folder"

echo "📁 Navigating to project directory: $PROJECT_DIR"
cd "$PROJECT_DIR" || { echo "❌ Project directory not found!"; exit 1; }

echo "🔄 Pulling latest changes from Git..."
git pull origin main

echo "🧪 Checking for virtual environment..."
if [ ! -d ".venv" ]; then
  echo "🔧 .venv not found. Creating a new virtual environment..."
  python3 -m venv .venv
fi

echo "⚙️ Activating virtual environment..."
source .venv/bin/activate

echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "🛑 Stopping any existing Uvicorn process..."
pkill -f "uvicorn main:app" || true

echo "🚀 Starting FastAPI server with Uvicorn..."
nohup uvicorn chat_fastAPI:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

echo "✅ Deployment complete. App should be running at http://<your-ec2-ip>:8000"
