@echo off
:: exit on error
setlocal EnableDelayedExpansion
set "ERROR_FLAG="
if not exist "povenv\Scripts\activate" (
    echo Error: Virtual environment not found.
    set "ERROR_FLAG=1"
)
if not exist "pyproject.toml" (
    echo Error: pyproject.toml not found.
    set "ERROR_FLAG=1"
)

if defined ERROR_FLAG (
    exit /b 1
)

:: Activate the virtual environment
call povenv\Scripts\activate

:: Install dependencies using Poetry
poetry install

:: Run Django management commands
set RENDER=python manage.py collectstatic --no-input
python manage.py migrate

:: Deactivate the virtual environment
deactivate
