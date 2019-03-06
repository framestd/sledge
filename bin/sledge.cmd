@echo off
:: Sledge Command Line API (CLAPI) Entry
:: Copyright (c) 2019 Caleb Adepitan
:: Licensed under the MIT License

title Frame Studios -- Sledge

setlocal
set SCRIPT=%~dp0sledge_cli.py
set PYTHON_EXE=python.exe
%PYTHON_EXE% --version >NUL 2>&1
if "%ERRORLEVEL%" == "0" goto init else goto no_python
:no_python
echo [error]: python command not found
echo     you either don't have python installed or you have not included it in your PATH
echo     if you have python, you should consider running the following command
echo     "set PATH=%%PATH%%;C:\<python_directory>"::set PATH only for this session
echo     "setx PATH=%%PATH%%;C:\<python_directory>"::set PATH permanently
echo     replace "<python_directory>" with the directory where you have python installed
goto end
:init
%PYTHON_EXE% %SCRIPT% %*
goto end
:end
