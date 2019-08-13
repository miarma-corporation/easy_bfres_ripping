setlocal
set PATH=C:\Python27;C:\Python27\ArcGIS10.1
cls
python %~dp0NUT_check.py "%~1"
%~dp0GTX2DDS.bat
pause