@echo off

SET jacs_path=%~dp0jacs\jacs.py

python %jacs_path% %*

exit /b 0