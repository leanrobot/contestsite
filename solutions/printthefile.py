import sys
filehandle = open("printthefile.txt")

for line in filehandle:
	sys.stdout.write(line)