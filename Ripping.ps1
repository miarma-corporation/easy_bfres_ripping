$path_model_input = "Model_input"
$path_model_output = "Model_output"

Remove-Item -Force $path_model_output\*
cp $path_model_input\* $path_model_output\

echo "Wii U Easy Model Extractor"

$files = Get-ChildItem $path_model_output\*.sbfres
foreach ($file in $files) {
	Executables\szstools\yaz0dec $file
	Remove-Item -Force $file
}

ls $path_model_output\*.rarc | Rename-Item -NewName {$_.name -replace " 0.rarc",""}
ls $path_model_output\*.sbfres | Rename-Item -NewName {$_.name -replace ".sbfres",".bfres"}

$files = Get-ChildItem $path_model_output\*.Tex*
foreach ($file in $files) {
	Executables\quickbms\quickbms Executables\BotW-SBFRES-to-FBX-master\bfresextraction\Libraries\WiiU_BFREStoGTX\BFRES_Textures_NoMips_BotWTex1Only.bms $file $path_model_output
	Remove-Item -Force $file
}

$dirs = Get-ChildItem -Directory $path_model_output
foreach ($dir in $dirs) {
	cp $path_model_output\$dir/* Executables\Inject_Pack\Convert\
	Remove-Item -Force -Recurse $path_model_output\$dir
}

./Executables\Inject_Pack\GTX2DDS.bat
Remove-Item -Force Executables\Inject_Pack\Convert\*
cp Executables\Inject_Pack\OutDDS\* $path_model_output
Remove-Item -Force  Executables\Inject_Pack\OutDDS\*

pause
