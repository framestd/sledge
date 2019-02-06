@ECHO OFF
setlocal
set SPECURL=https://framestd.github.io/remarkup/spec/x/
set RMH=https://framestd.github.io/sledge/
set SPECMD=-spec
set RM=remarkup
set RHELP=--help
set VER=--version
set SLH=help
set SLL=license
set SLU=-u
set SLC=contact
set SLI=issue
set RMV=Remarkup version X.0
set SLV=Sledge 1.0
set CONTACT=framestd@gmail.com
set ISSUEURL=https://github.com/framestd/sledge/issues

if %1 == %SPECMD% (
    start %SPECURL%
    goto END
)

for /F "tokens=1-4" %%G in ("%*") do (
    if %%G == %RM% (
        if %%H == %RHELP% (
            set ARGS=%RMH% %%I
            call :FURTHER %ARGS%
            goto END
        ) else if %%H == %VER% (
            call :INFORM %%I
            goto END
        ) else (
            goto RMHELPF
        )
    ) else if %%G == %VER% (
        if "%%H" == "" (
            echo %SLV%
            goto END
        ) else (
            goto SLF
        )
    ) else if %%G == %SLH% (
        if "%%H" == "" (
            goto SLEDGEHELP
        ) else (
            goto SLF
        )
    ) else if %%G == %SLL% (
        if "%%H" == "" (
            more %~dp0LICENSE
            goto END
        ) else if %%H == %SLU% (
            more %~dp0LICENSE
        ) else (
            goto SLF
        )
    ) else if %%G == %SLC% (
        if "%%H" == "" (
            echo %CONTACT%
            goto END
        ) else (
            goto SLF
        )
    ) else if %%G == %SLI% (
        if "%%H" == "" (
            start %ISSUEURL%
            goto END
        ) else (
            goto SLF
        )
    ) else (
        goto END
    )
)

:FURTHER
if "%2" == "" (
    start %1
    goto END 
) else (
    goto RMHELPF
)

:INFORM
if "%1" == "" (
    echo %RMV%
    goto END
) else (
    goto RMHELPF
)

:SLF
echo type "sledge help" to get help or "sledge --version" to know the version of sledge
goto END

:RMHELPF
echo type "sledge remarkup [--help/-h]" to get help or "sledge remarkup --version" to know the version you are using
goto END

:SLEDGEHELP
type HELP.txt

:END