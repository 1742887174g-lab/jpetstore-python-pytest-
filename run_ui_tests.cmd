@echo off
cd /d "%~dp0automation"
..\.venv\Scripts\python.exe run_tests.py --suite ui
