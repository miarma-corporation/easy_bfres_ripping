import sys
import struct
from struct import pack
import os
from util import *


numDDS = int(sys.argv[1])
outfile = open("model.nut", "wb")

outfile.write(struct.pack(">I",0x4E545033))
outfile.write(struct.pack(">H",0x0200))
outfile.write(struct.pack(">H",numDDS))
outfile.seek(0x10)
offset = 0x50*numDDS
for i in range(2, 2 + numDDS):
        dds = open(sys.argv[i], "rb")
        ddsName = sys.argv[i]
        ddsSize = os.stat(sys.argv[i])
        if i > 2:
                print("This is loop %d" % i)
                offset = offset - 0x80 + int(ddsSize.st_size)
        print(ddsSize)
        outfile.write(struct.pack(">I",(int(ddsSize.st_size) - 0x30)))
        outfile.seek(4,1)
        outfile.write(struct.pack(">I",int(ddsSize.st_size)-0x80))
        outfile.write(struct.pack(">H",0x50))
        outfile.seek(3,1)
        dds.seek(0x1C)
        outfile.write(dds.read(1))
        dds.seek(0x54)
        preFormat = readu32be(dds)
        texFormat = 0
        if preFormat == 0x44585433:
                texFormat = 1
        elif preFormat == 0x44585435:
                texFormat = 2
        elif preFormat == 0:
                texFormat = 14
        outfile.write(struct.pack(">H",texFormat))
        dds.seek(0x11)
        outfile.write(dds.read(1))
        dds.seek(0x10)
        outfile.write(dds.read(1))
        dds.seek(0x0D)
        outfile.write(dds.read(1))
        dds.seek(0x0C)
        outfile.write(dds.read(1))
        outfile.seek(8,1)
        outfile.write(struct.pack(">I",offset))
        outfile.seek(0xC,1)
        outfile.write(struct.pack(">I",0x65587400))
        for o in range(0x20,-0x10,-0x10):
                outfile.write(struct.pack(">I",o))
        outfile.write(struct.pack(">I",0x47494458))
        outfile.write(struct.pack(">I",0x10))
        outfile.write(struct.pack(">I",int((ddsName.replace(".dds","")),16)))
        outfile.seek(4,1)
        backInTime = outfile.tell()
        outfile.seek(offset + 0x10)
        dds.seek(0x80)
        outfile.write(dds.read(int(ddsSize.st_size)-0x80))
        outfile.seek(backInTime)
        dds.close()
        
outfile.close()

