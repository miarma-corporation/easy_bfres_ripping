setlocal
set PATH=C:\Users\smb12\Desktop\Skins\Utility\Convert;C:\Python27
for %%f in (*.dds) do for %%b in (*.nut) do python C:\Users\smb12\Desktop\Skins\Utility\Convert\NUT_Inject_old.py %%b %%f %%~nf 