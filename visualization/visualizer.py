import matplotlib.pyplot as plt
import datetime
import numpy as np
import os
debug = 0

titleDic = {
	'0': 'assignment-normalize-student',
	'1': 'quiz-normalize-student',
	'2': 'participation-normalize-student',
	'3': 'presentation-normalize-student',
	'4': 'project-normalize-student',
	'5': 'form-usage-normalize-student',
	'6': 'average-assignment-grade-course',
	'7': 'average-quiz-grade-course',
	'8': 'average-participation-grade-course',
	'9': 'average-presentation-grade-course',
	'10':'average-project-grade-course',
	'11':'form-usage-normalize-course',
	'12':'form-utility-normalize-course',
	'13':'online-learning-time-normalize-course',
	'14':'online-social-activity-normalize-course',
}
class Visualizer():

    def __init__(self, filePath,imagePath):
        if debug:
            print('visualizer setting up')
        # filepath means data path
        self.filePath = filePath
        self.imagePath = imagePath

    """
		get the data from the file name
		return the data list
	"""

    def getDataFromFile(self):
    	if self.figure_type is None:
    		raise Exception('no option setting, please check')
    	else:
    		fileName = os.path.join(self.filePath, 'type'+str(self.figure_type)+'.csv')
    		data_list = []
    	with open(os.path.join(self.filePath, fileName), 'r') as r:
    		line = r.readline()
    		while line:
    			data_list.append(line.split(','))
    			line = r.readline()
    	if debug:
    		print(data_list)
    	return data_list

    def getOption(self, courseID=None, studentID=None, figure_type=None):
        if figure_type is None:
            raise Exception('no option setting, please check')
        self.figure_type = figure_type
        self.courseID = courseID
        if studentID is not None:
            self.studentID = studentID
        else:
            self.studentID = -1  # -1 means all students which is used in the course visualization
    """ input single time string with format
		%Y-%m-%d
		output: datetime object. """

    def _parseTime(self, time_string):
        # trim space
        time_string = time_string.strip()
        # conversion from str to object
        return datetime.datetime.strptime(time_string, "%Y-%m-%d")

    def _generateImageName(self, typeName):
        import random as rand
        return 'image_' + typeName + '_' + str(rand.randint(1, 10000)) + '.png'
    def _parseY(self,data, studentID, courseID): 
    	y = []
    	if studentID == -1: 
    		for i in data: 
    			if int(i[1]) == int(courseID): 
    				y.append(i)
    	else: 
    		for i in data:
    			if int(i[0]) == int(studentID) and int(i[1]) == int(courseID): 
    				y.append(i) 
    	return y


	
	# """ array or nparray of X and y
	# 	output: image """
    def timeSeriesVisualization(self, data, x_label, y_label):
        # validation:
        
        if self.courseID is None:
            raise ValueError('no setting')
        # setting up for input
        data = np.array(self._parseY(data, self.studentID, self.courseID))
        X = np.array([self._parseTime(i[3]) for i in data])
        y = np.array([float(i[4].replace('\n','')) for i in data])
        # setting up for parameter name
        title = titleDic[str(self.figure_type)]
        fig = plt.plot(X, y,color='#cf6f82')
        plt.grid(True)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.tight_layout()
        fig[0].autofmt_xdate()
        name = self._generateImageName(title)
        fig.savefig(os.path.join(self.imagePath, name))
        return name

if __name__ == '__main__':

    visualizer = Visualizer(os.path.join(os.getcwd(),'result_csv'),os.getcwd())
    # data_X = ['2016-11-' + str(i) for i in range(1,31)] + ['2016-12-' + str(i) for i in range(1, 7)]
    # data_y = np.random.normal(0, 1, len(data_X))
    #registration for type
    visualizer.getOption(0,0,0)
    data = np.array(visualizer.getDataFromFile())
    visualizer.timeSeriesVisualization(
    	data, 'time', 'corresponding_result')
