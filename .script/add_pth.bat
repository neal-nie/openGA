@REM this script is used to create .pth
    
@REM 1st arg is asb. path of package's parent dir.
@REM 2nd arg is abs. path of site-packages
echo off

if not exist %2 (
    echo %2 not exist
) else (
    echo generate %2/user_packages.pth
    echo %1 > %2/user_packages.pth
)