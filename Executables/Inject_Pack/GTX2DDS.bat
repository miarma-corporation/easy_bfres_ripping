@echo off
for %%f in ("%~dp0/Convert/*.gtx") do "%~dp0TexConv2" -i "%~dp0/Convert/%%~nf.gtx" -o "%~dp0/OutDDS/%%~nf.dds"
pause