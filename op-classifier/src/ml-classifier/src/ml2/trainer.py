
class Trainer:
	"""
	The trainer is an object that produces models based on training data.
	
	It is configured by calling the configure(...) method.  The constructor takes no arguments - ever.
	
	To produce a new model, the train(...) method is called.
	"""
	def configure(self,settings):
		"""
		This method configures the trainer.  settings is a dictionary of attributes (keys) and attribute values (values).
		
		This method is called directly after the trainer object is instantiated.
		"""
		return
	
	def train(self,data_set):
		"""
		This method accepts a data set and returns a model which has been trained on
		the data set.
		"""
		raise Exception, 'train method is not implemented'
