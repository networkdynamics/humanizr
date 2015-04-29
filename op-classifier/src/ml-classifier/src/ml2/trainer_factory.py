import linear_svm_trainer
import libsvm_trainer
#import gbm_trainer # commented out for now. If u need to use GBDT, please uncomment. rpy2 needs to be installed.


class TrainerFactory:
	"""
	The TrainerFactory instantiates and configures a specific trainer object from a settings file.
	The settings file contains a single python dictionary which contains two entries:
	
		- trainer_class 	which is the complete python name of the trainer class to be instantiated
		- trainer_settings 	this is a dictionary of settings that will be passed to the trainer.configure(...) method.
	"""
	def __init__(self):
		self.settings=None
	
	def make_trainer(self,settings_file):
		"""
		This method constructs and configures a trainer object.  The specific type of trainer built
		is specified using the trainer_name.  settings is a dictionary that is used to configure the
		trainer.
		"""
		# load the appropriate information from the settings file
		self.read_configuration_info(settings_file)
		
		
		#  build the trainer object associated with the trainer_class
		class_name=self.settings['trainer_class']
		
		trainer = eval(class_name+'()')
		
		
		#  configure the trainer
		trainer.configure(self.settings['trainer_settings'])
		
		
		return trainer
	#
	def read_configuration_info(self,settings_file):
		if('.txt' in settings_file):
			#
			try:

				with open(settings_file,'r') as f:
					self.settings=eval(f.read())	

			except IOError:
				raise
		
		elif('.json' in settings_file):
			import json
			try:
				self.settings=json.load(open(settings_file,'r'))
			except IOError:
				raise
		
		
