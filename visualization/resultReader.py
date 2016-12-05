import re

fileName = ['type' + str(i) +'.txt'  for i in range(0,15)]

for file in fileName:
	with open(file, 'r') as _read:
		string = _read.read().replace('\n','').replace('[','').replace(']','').replace('"','')
		datalist = re.findall(r'\((.+?)\)', string)
		with open(file.replace('.txt','.csv'), 'w') as f:
			for data in datalist:
				f.write(data+'\n')