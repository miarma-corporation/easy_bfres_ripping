import sys
import struct
from struct import pack
import os
from util import *


nut = open(sys.argv[1], "rb+")
dds = str(sys.argv[2])
texID = int(sys.argv[3])
NTWU = readu32be(nut)
Version = readu16be(nut)
fileTotal = readu16be(nut)
nut.seek(0x10)
paddingFix = 0
for i in range(fileTotal):
        if i > 0:
                paddingFix = paddingFix + headerSize
        fullSize = readu32be(nut)
        nut.seek(4,1)
        size = readu32be(nut)
        headerSize = readu16be(nut)
        nut.seek(2,1)
        mipsFlag = readu16be(nut)
        gfxFormat = readu16be(nut)
        if NTWU == 0x4E545755:
                width = readu16be(nut)
                height = readu16be(nut)
        if NTWU == 0x4E545033:
                width2 = readByte(nut)
                width1 = readByte(nut)
                height2 = readByte(nut)
                height1 = readByte(nut)
        numOfMips = readu32be(nut)
        nut.seek(4,1)
        offset1 = (readu32be(nut) + 16)
        offset2 = (readu32be(nut) + 16)
        offset3 = (readu32be(nut) + 16)
        nut.seek(4,1)
        if headerSize == 0x60:
                size1 = readu32be(nut)
                nut.seek(12,1)
        if headerSize == 0x70:
                size1 = readu32be(nut)
                nut.seek(0x1C,1)
        if headerSize == 0x80:
                size1 = readu32be(nut)
                nut.seek(0x2C,1)
        if headerSize == 0x90:
                size1 = readu32be(nut)
                nut.seek(0x3C,1)
        eXt = readu32be(nut)
        nut.seek(12,1)
        GIDX = readu32be(nut)
        nut.seek(6,1)
        skinNum = readByte(nut)
        fileNum = readByte(nut)
        nut.seek(4,1)
        print("Slot Number %i Texture id %i has %i mipmaps. Format is %i" % (skinNum/4,fileNum,mipsFlag,gfxFormat))
        if i == 0:
                offsetHeader = offset3
        if i > 0:
                offset1 += paddingFix
                offsetHeader += 0x80
        backNTime = nut.tell()
        nut.seek(offsetHeader + 0x36)
        swizzing = readByte(nut)
        print("Offset for texture is %s and swizzing # is %s" % (hex(offset1),hex(swizzing)))
        if fileNum == texID:
                os.system("TexConv2.exe -i %s -o tmp.gtx -swizzle %s -minmip 1" %(dds,swizzing))
                GTX = open("tmp.gtx", 'rb')
                GTX.seek(0xFC)
                magic = 0
                while magic != 0x424C4B7B00000020:
                        magic = readu64be(GTX)
                GTX.seek(-8,1)
                texOffset = (GTX.tell() - 0xFC)
                texEnd = (os.path.getsize("tmp.gtx") - 0x11C)
                texSec = (texEnd - (texOffset + 0x20))
                GTX.seek(0xFC)
                nut.seek(offset1)
                print(hex(texOffset))
                print(hex(texEnd))
                print(hex(texSec))
                nut.write(GTX.read(texOffset))
                if (texEnd != texOffset and mipsFlag != 1):
                        currentPos = nut.tell()
                        texSec = (size - (currentPos - offset1))
                        print(hex(size))
                        print(hex(texSec))
                        GTX.seek(0x20,1)
                        nut.write(GTX.read(texSec))
        nut.seek(backNTime)
GTX.close()
nut.close()
