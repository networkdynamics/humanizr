
from dataset import DataSet
import random
import logging
import argparse
import os


class XValidator:
	"""
	This class runs cross-validation on a data set and trainer combination.
	"""
	
	def __init__(self,trainer,data_set,num_folds):
		self._trainer = trainer
		self._master_dataset = data_set
		self._num_folds = num_folds
		self._predictions=[]
		self._models=[]
		self._folds=[]
		
	
	def generate_folds(self):
		"""
		Generate smaller, non-overlapping data sets from the master data set.
		The folds should be returned in a list of tuples.  Each tuple corresponds to a fold.
		t[0] is the testing fold of the data 
		, t[1] is the inverse of the fold (training fold:  the rest of the data).
		"""
		items=self._master_dataset.get_items()
		random.shuffle(items)
		num_fold=self._num_folds
		folds=[] 
		if(items is not None):
			
			for i in range(num_fold):
				# Each fold is a tuple of datasets
				# First one is the test fold,
				# The inverse fold is used for training
				folds.append((DataSet(),DataSet()))
			current_fold=0
			
			for item in items:
				
				#print type(self._master_dataset.get_label(item))
				folds[current_fold][0].add_item(item,self._master_dataset.get_features(item),self._master_dataset.get_label(item))
				
				for j in range(num_fold):
					if(j<>current_fold):
						folds[j][1].add_item(item,self._master_dataset.get_features(item),self._master_dataset.get_label(item))
						
						
				
				current_fold+=1
				if(current_fold==num_fold):
					current_fold=0
		return folds
	
	def run_xvalid(self):
		"""
		Run the cross-validation.  No result is returned.
		"""
		self._models = []
		self._predictions = []
		self._folds = self.generate_folds()
		
		for (fold,inverse_fold) in self.folds():
			# get the model
			model = self._trainer.train(inverse_fold)
			self._models.append(model)
			
			pred = model.predict(fold)
			'''
			print '******: Predictions returned'
			print pred.predictions()
			print 'Size '+str(pred.size())
			print 'Count '+str(pred.predicted_count())
			'''
			print 'Accuracy (computed) '+str(pred.accuracy())
			
			self._predictions.append(pred)
		for pred in self._predictions:
			print pred.predictions()
		
			
	def models(self):
		return self._models
		
	def folds(self):
		return self._folds
		
	def predictions(self):
		return self._predictions
		
if __name__ == '__main__':
	
	from trainer_factory import TrainerFactory
	from dataset import DataSet
	import sys
	
	parser = argparse.ArgumentParser(prog='xvalidator',description='Cross validate using a machine learning algorithm.')
	parser.add_argument('settings_file', help='Settings file for configuring the machine learning algorithm')
	parser.add_argument('ds_file', help='Dataset file')
	parser.add_argument('num_folds', help='Number of folds')
	parser.add_argument('-d','--debug',action='store_true',help='Debug mode')
	
	
	args=parser.parse_args()
	
	# read in arguments
	settings_file = args.settings_file
	ds_file = args.ds_file
	num_folds = int(args.num_folds)
	
	print(ds_file)
	if(args.debug):
		logging.basicConfig(level=logging.DEBUG,filename='xvalidator_log_'+os.path.basename(ds_file)+'_'+str(os.getpid())+'.log')
	else:
		logging.basicConfig(level=logging.INFO)
		
	
	# load the data set
	data_set = DataSet(ds_file)
	#data_set.filter_features([0])
	#data_set.normalize_linear(0,1)
	#data_set.smart_normalize()
	# Normalization, log normalize 
	data_set.log_normalize()
	#data_set.normalize_linear(-1,1)
	#data_set.normalize_to_unit_vector()
	# create the trainer
	tfact = TrainerFactory()
	trainer = tfact.make_trainer(settings_file)
	
	# run the cross validation 
	xv = XValidator(trainer,data_set,num_folds)
	xv.run_xvalid()
	
	# print out some statistics
	num_preds = float(len(xv.predictions()))
	avg_sense = sum([pred.sensitivity() for pred in xv.predictions()]) / num_preds
	avg_spec = sum([pred.sensitivity() for pred in xv.predictions()]) / num_preds
	avg_accuracy=sum([pred.accuracy() for pred in xv.predictions()]) / num_preds
	#print 'Average sensitivity:',avg_sense
	#print 'Average specificity:',avg_spec
	print 'Average accuracy:',avg_accuracy
	
	# label based sensitivity
	for pred in xv.predictions():
		print pred.sensitivity_by_label()
		
	
		
	'''
	'''
