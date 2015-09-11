import sys
#read the amount left.
data_file = open("foreignshoes.dat")

num_lines = int(data_file.readline())

for line in data_file:
	data = line.split(" ")
	increment = 1
	country = "US"

	if data[0] == "Women":
		increment = 2
	if data[1] == "UK":
		increment *= -1
		country = "US"
	else:
		country = "UK"

	print "%s %s %i" % (data[0], country, int(data[2])+increment)


'''
IF US -> UK, increase size.
if UK -> US, decrease size.

if Women, change by 2.
if Men, change by 1.
'''