for %%f in (Convert/*.gtx) do texconv2 -i Convert//%%f -o OutDDS/%%~nf.dds
for %%f in (Convert/*.gtx) do texconv2 -i Convert//%%f -f GX2_SURFACE_FORMAT_TCS_R8_G8_B8_A8_UNORM  -o %%~nf.gtx
for %%f in (Convert/*.gtx) do texconv2 -i %%f -o %%~nf.dds

del *.gtx
cd Convert
del *.gtx
cd..
