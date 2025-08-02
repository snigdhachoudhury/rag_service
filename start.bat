@echo off
echo Starting SUPER FAST FREE RAG Service...
echo.
echo Make sure your .env file has:
echo - GEMINI_API_KEY
echo - PINECONE_API_KEY
echo.
cd /d "%~dp0"
python main.py
pause
