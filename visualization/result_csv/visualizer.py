import matplotlib.pyplot as plt
import datetime
import numpy as np
import os
debug = 1


class Visualizer():
	def __init__(self, filePath):
		print('visualizer setting up')
		self.filePath = filePath
	

	"""	
		get the data from the file name
		return the data list
	"""
	def getAllFile(self, fileName):
		data_list = []
		with open(os.path.join(self.filePath,fileName), 'r') as r:
			line = r.readline()
			while line:
				data_list.append(line.split(','))
				line = r.readline()
		if debug:
			print (data_list)
		return data_list
	""" input single time string with format
		%YY-%mm-%dd
		output: datetime object. """

	def _parseTime(self,time_string):
		# trim space
		time_string = time_string.strip()
		# conversion from str to object
		return datetime.datetime.strptime(time_string, "%Y-%m-%d")
	def _generateImageName(self, typeName):
		import random as rand
		return 'image_' + typeName + '_' + str(rand.randint(1,10000)) + '.png'
	""" array or nparray of X and y
		output: image """
	def timeSeriesVisualization(self, data_X, data_y, x_label, y_label, title):
		# validation:
		if not len(data_X) == len(data_y):
			raise ValueError('X data (%d) is not consistent with y(%d) in ' % (len(data_X),len(data_y)))
		# setting up for input
		X = np.array([self._parseTime(i) for i in data_X])
		y = np.array(data_y)

		plt.plot(X,y)
		plt.grid(True)
		plt.xlabel(x_label)
		plt.ylabel(y_label)
		plt.title(title)
		plt.savefig(os.path.join(self.filePath, self._generateImageName(title)),bbox_inches='tight',dpi=100)

if __name__ == '__main__':
	visualizer = Visualizer(os.getcwd())
	data_X = ['2016-11-' + str(i) for i in range(1,31)] + ['2016-12-' + str(i) for i in range(1, 7)]
	data_y = np.random.normal(0, 1, len(data_X))
	visualizer.timeSeriesVisualization(data_X, data_y,'time','random','testing')