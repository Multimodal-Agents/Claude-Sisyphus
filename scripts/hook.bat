@echo off

set HOOK_SRC=hooks\pre-push
set HOOK_DEST=.git\hooks\pre-push

if "%1"=="on" goto ON
if "%1"=="off" goto OFF

echo Usage: scripts\hook.bat [on^|off]
echo.
if exist "%HOOK_DEST%" (
    echo Current status: ON ^(pushes are blocked^)
) else (
    echo Current status: OFF ^(pushes are allowed^)
)
goto END

:ON
if exist "%HOOK_DEST%" (
    echo Push protection is already ON.
) else (
    copy "%HOOK_SRC%" "%HOOK_DEST%" >nul
    echo Push protection is now ON. Git push is blocked.
)
goto END

:OFF
if not exist "%HOOK_DEST%" (
    echo Push protection is already OFF.
) else (
    del "%HOOK_DEST%"
    echo Push protection is now OFF. Git push is allowed.
)
goto END

:END
