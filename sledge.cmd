:: Sledge API MAIN ENTRY POINT 
:: Copyright 2019 Frame Studios. All rights reserved.
:: Author(s): Caleb Adepitan
:: Licensed under MIT
@ECHO OFF
title Frame - Sledge
setlocal
set ADDCMD=script
set PARAM=--update
set BUILDCMD=nail

set DIR=%~dp0env\
set F=PATH
set PATHFILE=%DIR%%F%

set SP=
if exist %PATHFILE% (
    set /p SP=<%PATHFILE%
) else (
    set SP=%~dp0sledge.py
)

rem store these before shifting
set A=%1
set B=%2
set C=%3

if "%1" == "" (
    more %~dp0description.txt
    goto END
)
if not %1 == %ADDCMD% (
    if not %1 == %BUILDCMD% (
        call argparse.cmd %*
        goto END
    )
)


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
        echo Starting script at "%SP%"
        echo.
    )
    python %SP% %CHOP%
    pause
    goto END
)

set MSG=Updated your script path to "%C%"
if %A% == %ADDCMD% (
    if %B% == %PARAM% (
        if not exist %DIR% (
            mkdir %DIR%
            echo %C%>%PATHFILE%
            echo %MSG%
            goto END
        ) else (
            echo %C%>%PATHFILE%
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
goto END
:END