import cPickle as pickle
class Prediction:
	
	def __init__(self,data_set,predictions=None):
		"""
		predictions is a dictionary mapping item id's (keys) to the predicted label (values).
		"""
		self._data_set = data_set
		if(predictions==None):
			self._predictions={}
		else:
			self._predictions = predictions
		
		
	def items(self):
		return self._data_set.get_items()
		
	def true_label(self,item):
		return self._data_set.get_label(item)
		
	def est_label(self,item):
		return self._predictions[item]
	def set_est_label(self,item,label):
		self._predictions[item]=label
	
		
	def sensitivity(self):
		# TP/TP+FN
		# Not implemented
		return 0
		
	def specificity(self):
		return 0
	def labels(self):
		# returns set of all the labels
		labels=set()
		for item in self.items():
			if(self.true_label(item) not in labels):
				labels.add(self.true_label(item))
		return(labels)
	def sensitivity_by_label(self):
		labels=self.labels()
		num_label=len(labels)
		sensitivity_dict=dict()
		
		for label in labels:
			sensitivity_dict[label]={'total_count':0,'accurate_count':0}
			
		for item in self.items():
			sensitivity_dict[self.true_label(item)]['total_count']+=1
			if(int(self.true_label(item))==int(self.est_label(item))):
				sensitivity_dict[self.true_label(item)]['accurate_count']+=1
		
		for label in labels:
			sensitivity_dict[label]['accuracy']=1.0*sensitivity_dict[label]['accurate_count']/sensitivity_dict[label]['total_count']
			del sensitivity_dict[label]['accurate_count']
			#del sensitivity_dict[label]['total_count']
			
			
		return sensitivity_dict
			
			
			
			
		
		
		
	def accuracy(self):
		total_count=0
		accurate_count=0
		for item in self._data_set.get_items():
			total_count+=1
			#print self.true_label(item),self.est_label(item)
			if(int(self.true_label(item))==int(self.est_label(item))):
				accurate_count+=1
		return accurate_count*1.0/total_count
	def size(self):
		return len(self._data_set.get_items())
	def predicted_count(self):
		return len(self._predictions)
	def predictions(self):
		return self._predictions

class Model:
	
	
		
	def predict(self,data_set):
		"""
		This method uses the model to assign a label to each item in the data set.  The return value
		is a Prediction object.
		"""
		raise Exception, 'predict is not implemented'
