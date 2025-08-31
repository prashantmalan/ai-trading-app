@echo off
echo Starting AI-Powered Trading Application...

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing/updating dependencies...
pip install -r requirements.txt

echo.
echo Checking environment variables...
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo Please edit the .env file and add your API keys:
    echo - OPENAI_API_KEY=your_openai_api_key_here
    echo - ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key_here
    echo.
    echo Press any key to open .env file for editing...
    pause >nul
    notepad .env
)

echo.
echo Starting backend server...
start "Backend Server" cmd /k "venv\Scripts\activate && python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Starting frontend application...
start "Frontend Application" cmd /k "venv\Scripts\activate && streamlit run frontend/main.py --server.port 8501"

echo.
echo Application is starting...
echo Backend API: http://localhost:8000
echo Frontend UI: http://localhost:8501
echo.
echo Press any key to open the application in your browser...
pause >nul

start http://localhost:8501

echo.
echo Application is now running!
echo Press any key to exit this window...
pause >nul
