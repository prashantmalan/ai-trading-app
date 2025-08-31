#!/bin/bash

echo "Starting AI-Powered Trading Application..."

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing/updating dependencies..."
pip install -r requirements.txt

echo ""
echo "Checking environment variables..."
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "Please edit the .env file and add your API keys:"
    echo "- OPENAI_API_KEY=your_openai_api_key_here"
    echo "- ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here"
    echo ""
    echo "Press Enter to continue after editing .env file..."
    read
fi

echo ""
echo "Starting backend server..."
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

echo ""
echo "Waiting for backend to start..."
sleep 5

echo ""
echo "Starting frontend application..."
streamlit run frontend/main.py --server.port 8501 &
FRONTEND_PID=$!

echo ""
echo "Application is now running!"
echo "Backend API: http://localhost:8000"
echo "Frontend UI: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application..."

# Wait for user interrupt
trap "echo 'Stopping application...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
