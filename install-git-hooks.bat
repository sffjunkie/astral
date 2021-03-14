@echo off
IF "%1" == "--help" (
    echo "Use to install a git hook in the appropriate place"
    echo.
    echo "./install-git-hooks.bat <hook-name>"
    echo.
    echo "e.g. ./install-git-hooks.bat pre-commit"
) ELSE (
    copy src\git-hooks\%1 .git\hooks\
)
