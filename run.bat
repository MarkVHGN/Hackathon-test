@echo off
echo Starting Reverse Turing Detective...
echo.
echo Making sure dependencies are installed...
pip install -r requirements.txt
echo.
echo Starting Flask backend on http://localhost:5000
echo.
python game_backend.py
