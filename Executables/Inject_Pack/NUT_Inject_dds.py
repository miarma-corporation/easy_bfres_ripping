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
                resLocation = nut.tell()
                print(hex(resLocation))
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
                if NTWU == 0x4E545033:
                        ddsOpen = open(dds, 'rb')
                        nut.seek(resLocation)
                        ddsOpen.seek(0x11)
                        nut.write(ddsOpen.read(1))
                        ddsOpen.seek(0x10)
                        nut.write(ddsOpen.read(1))
                        ddsOpen.seek(0x0D)
                        nut.write(ddsOpen.read(1))
                        ddsOpen.seek(0x0C)
                        nut.write(ddsOpen.read(1))
                        nut.seek(0x10)
                        nut.write(struct.pack(">I",os.path.getsize(dds) - 0x80 + headerSize))
                        nut.seek(4,1)
                        nut.write(struct.pack(">I",os.path.getsize(dds)))
                        nut.seek(offset1)
                        ddsOpen.seek(0x80)
                        texEnd = (os.path.getsize(dds) - 0x80)
                        nut.write(ddsOpen.read(texEnd))
                        ddsOpen.close()
        nut.seek(backNTime)
nut.close()
