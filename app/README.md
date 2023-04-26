 # Author: Anna Hyer Spring 2023 Class: Fundamentals of Software Engineering

API instructions:
path: ...\GitHub\Agricultural_Monitoring_App\app

first time: pip install "fastapi[all]"

first time: create virtual environment: py -3 venv venv

every time: make sure venv is activated: view -> command palette ->                      .\venv\Scripts\python.exe
OR on command line:
  \\venv\Scripts\python.exe

on command line: activate.bat (should be automatic after first time)

start server on command line: uvicorn main:app --reload (OR uvicorn app.main:app --reload)
