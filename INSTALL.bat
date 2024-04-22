@echo off
set PYTHON_CMD=not found

py --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    set PYTHON_CMD=py
    goto execute
)

python --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    set PYTHON_CMD=python
    goto execute
)

python3 --version >nul 2>&1
if %ERRORLEVEL% == 0 (
    set PYTHON_CMD=python3
    goto execute
)

echo Python not found.
goto end

:execute
echo Python using '%PYTHON_CMD%'
%PYTHON_CMD% -m pip install -r requirements.txt
pause

:end
