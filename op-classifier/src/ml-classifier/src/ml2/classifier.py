
from dataset import DataSet
import random
import logging
import argparse
import sys
import os
import json


class Classifier:
	"""
	This class runs cross-validation on a data set and trainer combination.
	"""
	
	def __init__(self,trainer,training_data_set,test_data_set,use_saved_model=False,saved_model_file="",normalization_min_values=None):
		self._trainer = trainer
		self._training_data_set = training_data_set
		self._test_dataset=test_data_set
		self._prediction=None
		self._model=None
		self.normalization_min_values=normalization_min_values
		if(use_saved_model==True):
			self._model=self._trainer.load_model(saved_model_file)
		self._saved_model_file=saved_model_file
		
		
	
	def predictions(self):
		return(self._prediction.predictions())
	def accuracy(self):
		return(self._prediction.accuracy())
		
	
	def classify(self):
		
		if(self._model==None):
			self._model = self._trainer.train(self._training_data_set)
			if(self._saved_model_file<>""):
				self._model.save(self._saved_model_file,self.normalization_min_values)
		self._prediction=self._model.predict(self._test_dataset)
		
		
			
	
	def prediction_composition(self):
		composition_dict=dict()
		for pred in self._prediction.predictions():
			est_label=self._prediction.predictions()[pred]
			if(est_label not in composition_dict):
				composition_dict[est_label]=0
			composition_dict[est_label]+=1
		return(composition_dict)
	
	
		
#
#

def read_model_file_normalization_min_values(model_file):
	# load the model_file
	fin_model=open(model_file,'r')
	model_file_contents=json.load(fin_model)
	fin_model.close()
	return(model_file_contents['normalization_min_values'])

	
class InvalidModelFileToReadException(Exception):
	pass
		
	
		
if __name__ == '__main__':
	
	from trainer_factory import TrainerFactory
	from dataset import DataSet
	import sys
	
	parser = argparse.ArgumentParser(prog='classifier',description='Classify using a machine learning algorithm.')
	parser.add_argument('settings_file', help='Settings file for configuring the machine learning algorithm')
	parser.add_argument('test_ds_file', help='Test Dataset file ')
	#parser.add_argument('training_ds_file', help='Training Dataset file (default directory datagen)')
	parser.add_argument('-m','--model_file',action='store',default=None,help='Model file to load/save.')
	parser.add_argument('-t','--training_file',action='store',help='Training Dataset file',default=None)
	parser.add_argument('-o','--output_file',action='store',default=None,help='output file to save')
	parser.add_argument('-d','--debug',action='store_true',help='Debug mode')
	
	
	
	args=parser.parse_args()
	
	# read in arguments
	settings_file = args.settings_file
	training_ds_file = args.training_file
	test_ds_file = args.test_ds_file
	model_file=args.model_file
	
	# Redirecting the stdout to the output file.
	if(args.output_file<>None):
		sys.stdout=open(args.output_file,'w')
	
	
	
	
	if(args.debug):
		logging.basicConfig(level=logging.DEBUG,filename='classifier_log_'+os.path.basename(test_ds_file)+'_'+str(os.getpid())+'.log')
	else:
		logging.basicConfig(level=logging.INFO)
	#
	training_file_provided=False
	if(training_ds_file <> None):
		#print(training_ds_file)
		training_file_provided=True
		
	else:
		# No training file provided.
		# Therefore, the model file needs to exist.
		# if not, raise an exception.
		if(model_file==None):
			raise InvalidModelFileToReadException
		# check if the model_file actually exists
		if(os.path.exists(model_file)==False):
			raise InvalidModelFileToReadException
			
			
		
	
	# load the data set
	if(training_file_provided):
		training_data_set = DataSet(training_ds_file)
		#training_data_set.normalize_to_unit_vector()
		observed_min_values=training_data_set.log_normalize()
		
		
	else:
		# No training file provided.
		# But the model file contains info about normalization min_values
		observed_min_values=read_model_file_normalization_min_values(model_file)
		
	
	test_data_set=DataSet(test_ds_file)
	#test_data_set.normalize_to_unit_vector()
	test_data_set.log_normalize_using_training_set_values(observed_min_values)
		
		
	'''	
	test_data_set=DataSet(test_ds_file)
	#data_set.filter_features([0])
	#data_set.normalize_linear(0,1)
	#data_set.smart_normalize()
	# Faiyaz: Commenting out the next two lines for testing July 7 2012
	#observed_min_values=training_data_set.log_normalize()
	#test_data_set.log_normalize_using_training_set_values(observed_min_values)
	# Faiyaz: These two lines are for test purpose; July 7 2012
	test_data_set.normalize_to_unit_vector()
	#training_data_set.rescale_feature_values(1000)
	#test_data_set.rescale_feature_values(1)
	
	test_data_set.log_normalize_using_training_set_values(observed_min_values)
	
	'''	
	#data_set.normalize_linear(-1,1)
	#data_set.normalize_to_unit_vector()
	# create the trainer
	tfact = TrainerFactory()
	trainer = tfact.make_trainer(settings_file)
	if(training_file_provided and model_file==None): # Only the training file is provided. But no model file to save.
		cl = Classifier(trainer,training_data_set,test_data_set)
	elif(training_file_provided and model_file<>None): #  the training file and model file, both provided. Model file will be used for output (save).
		cl = Classifier(trainer,training_data_set,test_data_set,use_saved_model=False,saved_model_file=model_file,normalization_min_values=observed_min_values)
		
	
	else: # No training file provided. So model_file is used to get the model
		cl = Classifier(trainer,None,test_data_set,use_saved_model=True,saved_model_file=model_file)
	
	cl.classify()
	
	translate = {'1':'org', '2':'per'}
	# print out some statistics
	for uid,label in cl.predictions().items():
		print '%s\t%s' % (uid, translate[label])
	#print cl.accuracy()
	#print cl.prediction_composition()
		
	'''
	'''
