:: Frame API entry point 
:: Copyright 2019 Frame Studios
:: This file has been modified by authors of the project at pyframe
:: to fit for the python language as pyframe is written in python
:: Licensed under GNU/GPL-2.0
@ECHO OFF
title Frame - pyframe
set ADDCMD=script
set PARAM=--update
set BUILDCMD=start
set DIR=%~dp0env\
set F=PATH
set PATHFILE=%DIR%%F%
set SP=
if exist %PATHFILE% (
	set /p SP=<%PATHFILE%
)

rem store these before shifting
set A=%1
set B=%2
set C=%3

set CHOP=
shift
:loop
if "%1" == "" (
	goto breakloop
)
set CHOP=%CHOP%%1 
shift
goto loop

:breakloop
if %A% == %BUILDCMD% (
	if exist %PATHFILE% (
		echo starting script at "%SP%"
		echo **************************************************************************************
		echo **************************************************************************************
		echo build process started...
		python %SP% %CHOP%
		goto END
	) else (
	  goto PathNotSet
	)
)

set MSG=Updated your script path to "%C%"
if %A% == %ADDCMD% (
	if %B% == %PARAM% (
		if not exist %DIR% (
			mkdir %DIR%
			echo %3>%DIR%%F%
			echo %MSG%
			goto END
		) else (
			echo %3>%DIR%%F%
			echo %MSG%
			goto END
		)
	)
)

:PathNotSet
echo [status]: failed
echo     No script to call
echo     Set the path to your python script to call.
echo     Using the "script --update path/to/script.py" command
echo     then you can use the "start" command to start your script with arguments following
echo.
:END