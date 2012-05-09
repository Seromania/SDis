#!/usr/bin/env python

import struct
from binascii import unhexlify
import sys


Special = {0x01:"JSR", 0x08:"INT", 0x09:"IAG", 0x0a:"IAS", 0x0b:"RFI a", 0x0c:"IAQ", 0x10:"HWN", 0x11:"HWQ", 0x12:"HWI"}

Opcode = {0x01:"SET", 0x02:"ADD", 0x03:"SUB", 0x04:"MUL", 0x05:"MLI", 0x06:"DIV",
	  0x07:"DVI", 0x08:"MOD", 0x09:"MDI", 0x0a:"AND", 0x0b:"BOR", 0x0c:"XOR", 0x0d:"SHR", 0x0e:"ASR", 0x0f:"SHL",
	  0x10:"IFB", 0x11:"IFC", 0x12:"IFE", 0x13:"IFN", 0x14:"IFG", 0x15:"IFA", 0x16:"IFL", 0x17:"IFU", 0x1a:"ADX",
	  0x1b:"SBX", 0x1e:"STI", 0x1f:"STD"}
Values = {0x00:"A", 0x01:"B", 0x02:"C", 0x03:"X", 0x04:"Y", 0x05:"Z", 0x06:"I", 0x07:"J",
	  0x08:"[A]", 0x09:"[B]", 0xA:"[C]", 0xB:"[X]", 0xC:"[Y]", 0xD:"[Z]", 0xE:"[I]", 0xF:"[J]",
	  0x19:"[SP]", 0x1a:"[SP + next word]", 0x1b: "SP", 0x1c: "PC", 0x1d: "EX", 0x1e: "[next word]"}

def disassemble(bindata,Wordpointer):
	"Start des Disassemblen"
	global Wp
 	dBinary = "0b{0:016b}".format(int(bin(int(bindata[Wordpointer],16)),2))
	#print ("dBinary: %s" % dBinary)
	dA = dBinary[2:8]
	dO = dBinary[13:18]
	if int(dO,2) == 0b000000:
		#print ("Special Opcode")
		dA = dBinary[2:8]
		dO = dBinary[8:13]
		dO = Special.get(int(dO,2))
		#print ("dA: %s" % dA)
		if int(dA,2) == 0x1f:
			dA = int(bindata[Wordpointer+1],16)
			Wordpointer += 1
		elif int(dA,2) == 0x18:
			dA = "POP"
		elif int(dA,2) >=0x20 and int(dA,2) <=0x3f:
			dA = int(dA,2)-0x20-1
		else:
			dA = Values.get(int(dA,2))
		print ("%s: %s %s" % ("0x{0:00004x}".format(Wp)[2:], dO, dA))
		Wordpointer += 1
		Wp = Wordpointer
		return
	#print ("A: %s" % dA)
	if int(dA,2) == 0x1f:
		#print ("Next Word")
		dA = int(bindata[Wordpointer+1],16)
		Wordpointer += 1
		#print dA
		dB = dBinary[8:13]
		if int(dB,2) == 0x1f:
			dB = int(bindata[Wordpointer+1],16)
			Wordpointer += 1
		dO = dBinary[13:18]
		#print ("a: %s" % dA)
		#print ("b: %s" % dB)
		#print ("o: %s" % dO)
		#print dBinary[2:]
		dO = Opcode.get(int(dO,2))
		dB = Values.get(int(dB,2))
		print ("%s: %s %s, %s" % ("0x{0:00004x}".format(Wp)[2:], dO, dB, dA))
		Wordpointer += 1
		Wp = Wordpointer
		return

	dB = dBinary[8:13]
	#print ("a: %s" % dA)
	#print ("b: %s" % dB)
	#print ("o: %s" % dO)
	#print dBinary[2:]
	dO = Opcode.get(int(dO,2))
	#Variable 0x18 verschieden in a und b
	if int(dA,2) == "0x18":
		dA = "POP"
	if int(dB,2) == "0x18":
		dB = "PUSH"
	else:
		dB = Values.get(int(dB,2))
	if int(dA,2) >=0x20 and int(dA,2) <=0x3f:
		dA = int(dA,2)-0x20-1
	else:
		dA = Values.get(int(dA,2))
	print ("%s: %s %s, %s" % ("0x{0:00004x}".format(Wp)[2:], dO, dB, dA))
	Wordpointer += 1
	Wp = Wordpointer



def parseHex(bdata,count):
	"Parsing the Hex"
	if int(bdata[count],16)<4095:
		bdata[count]='0'+bdata[count]

count=0
count2=0
f = open("chess1.bin","rb")
a = f.read()
data=[]
bindata=[]
#Binarys kriegen
for i,b in enumerate(a):
	#print ("%s | %s" % (i, b))
	data.append(hex(ord(a[i])))

#Binarys 
while count < i:
	bindata.append(hex((int(data[count],16)<<8)+int(data[count+1],16))[2:])
	parseHex(bindata,count2)
	print bindata[count2].upper()
	count+=2
	count2+=1

print ("--------------")
Wp=0
while Wp < len(bindata):
	disassemble(bindata,Wp)
#print ("Wordpointer: %s" % Wp)

