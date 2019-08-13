*Sm4sh Injector PACK*
Vertion 2.0

*REQUIRES TexConv2*
Requires Python 2.7 installed

NEW FEATURES!!
Extract files and convert via A.Extract.A
Better GUI
True lazyness on mips. (Now it staps it from overwriting preshus data)

*Extraction*

*Easy*
Drag your nut file onto A.Extract.A
You will get your DDS files in OutDDS

*Harder*
Open cmd in the directoru of convert
type
python Nut_check.py "Your Nut file"
Then run
GTX2DDS


*Clean Up*
Open CleanUp

*Injection*

*Easy*
Use my easy injector via editing EasyInject.bat to change the folder to NUT_Inject and TexConv2
Copy that EasyInject.bat to the folder where your new dds and nut file
Open EasyInject and boom you are done
*Harder*
Inject via 'python NUT_Inject.py Model.nut myTexture.dds (Slot Number IE: 9 10 25 ect)'

*Specal*
**This is for AMDCompress and Nvidia Plugin**
ARGB_8888 is what AMDCompress opens ABGR_8888 dds files, so in editing swap the Red and Blue then when done with edits Swap them back....
The new EasyInject_ARGB_png.bat can convert your png export from AMDCompressCLI.exe

*Usage of AMDCompressCLI.exe*
AMDCompressCLI.exe DDSfile(in) PNGfile(out)


*Update*
If you have a dds file in the DDS folder, use the EasyInject_S_DDS.bat

Update your bat files, If you have spaces like c:/User/Bob/Desktop/Meme Oh/Convert me/ Then add quoits "c:/User/Bob/Desktop/Meme Oh/Convert me/"

USE INTEL DDS PLUGIN FOR THOES PESKY A8B8G8R8
http://gametechdev.github.io/Intel-Texture-Works-Plugin/
and if you dont have Photoshop use amd compress but swap Red and Blue chanels.
http://developer.amd.com/tools-and-sdks/graphics-development/amdcompress/ 
