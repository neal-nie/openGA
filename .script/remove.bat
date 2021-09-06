@REM this file is used to remove files and folders, could run with cmd

@REM args: wildcard to search file and folders

@echo off

@REM remove folders
for /d %%x in (%*) do (
    @REM scan each input arg
    echo remove folder: %%x
    @REM recursive, quiet (rd not support wildcard)
    rd /s /q %%x

)
@REM remove files
for %%x in (%*) do (
    echo remove file: %%x
    @REM forced, quiet
    del /f /q %%x
)
