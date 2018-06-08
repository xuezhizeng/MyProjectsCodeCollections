import os
import shutil

save=raw_input('target folder: ')

this=os.listdir('.')
this=[i for i in this if i.find('.')<0 and i!=save]

for i in this:
	for j in os.listdir(i):
		try:
			shutil.move(i+'/'+j, save)
		except:
			print 'X',j
