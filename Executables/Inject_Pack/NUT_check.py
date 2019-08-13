import sys
import struct
from struct import pack
import os
from util import *
import string
import math

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

nut = open(sys.argv[1], "rb+")

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
        ddssize = size
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
        nut.seek(-4,1)
        trueID = readu32be(nut)
        nut.seek(4,1)
        ddsFormat = ""
        if(gfxFormat==0):
                ddsFormat = "BC1/DXT1"
        elif(gfxFormat==1):
                ddsFormat = "BC2/DXT3"
        elif(gfxFormat==2):
                ddsFormat = "BC3/DXT5"
        elif(gfxFormat==21):
                ddsFormat = "BC4/ATI1"
        elif(gfxFormat==22):
                ddsFormat = "BC5/ATI2"
        elif(gfxFormat==14):
                ddsFormat = "ABGR_8888/A8B8G8R8"
        elif(gfxFormat==17):
                ddsFormat = "ARGB_8888/A8R8G8B8"
        print("Slot %i\tID %i\t%i Mipmaps\t%s" % (skinNum/4,i,mipsFlag,ddsFormat))
        if NTWU == 0x4E545755:
                if i == 0:
                        offsetHeader = offset3
                if i > 0:
                        offset1 += paddingFix
                        offsetHeader += 0x80
                backNTime = nut.tell()
                nut.seek(offsetHeader)
                fileStr = ("%d"  % i)
                outfile = open(os.path.join(__location__,"Convert" + "/" + fileStr + ".gtx"), "wb")
                outfile.write("\x47\x66\x78\x32\x00\x00\x00\x20\x00\x00\x00\x07\x00\x00\x00\x01\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x42\x4C\x4B\x7B\x00\x00\x00\x20\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0B\x00\x00\x00\x9C\x00\x00\x00\x00\x00\x00\x00\x00")
                outfile.write(nut.read(0x80))
                outfile.write("\x00\x00\x00\x01\x00\x01\x02\x03\x1F\xF8\x7F\x21\xC4\x00\x03\xFF\x06\x88\x80\x00\x00\x00\x00\x0A\x80\x00\x00\x10\x42\x4C\x4B\x7B\x00\x00\x00\x20\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x0C\x00\x08\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
                outfile.seek(0x50)
                outfile.write(struct.pack(">I",1))
                outfile.seek(0xf0)
                outfile.write(struct.pack(">I",size))
                outfile.seek(8,1)
                nut.seek(offset1)
                outfile.write(nut.read(size))
                outfile.write("\x42\x4C\x4B\x7B\x00\x00\x00\x20\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
                outfile.close()
                nut.seek(backNTime)
        if NTWU == 0x4E545033:
                backNTime = nut.tell()
                fileStr = ("%d"  % fileNum)
                outfile = open(os.path.join(__location__, "DDS" + "/" + fileStr + ".dds"), "wb")
                outfile.write("\x44\x44\x53\x20\x7C\x00\x00\x00\x07\x10\x08\x00\x80\x00\x00\x00\x80\x00\x00\x00\x00\x20\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00\x04\x00\x00\x00\x44\x58\x54\x31\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
                if i > 0:
                        offset1 += paddingFix
                nut.seek(offset1)
                outfile.write(nut.read(ddssize))
                outfile.seek(0x0C)
                outfile.write(struct.pack("B",height1))
                outfile.write(struct.pack("B",height2))
                outfile.seek(0x10)
                outfile.write(struct.pack("B",width1))
                outfile.write(struct.pack("B",width2))

                if gfxFormat == 2:
                        outfile.seek(0x54)
                        outfile.write("\x44\x58\x54\x35")
                if gfxFormat == 14 or 17:
                        outfile.seek(0x50)
                        outfile.write("\x41\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00\x00\x00\xFF\x00\x00\xFF\x00\x00\xFF\x00\x00\x00\x00\x00\x00\xFF\x08\x10\x40\x00")
                outfile.close()
                nut.seek(backNTime)
nut.close()
