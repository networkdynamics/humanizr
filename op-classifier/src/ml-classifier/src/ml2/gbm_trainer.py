#!/usr/bin/env python
# encoding: utf-8
"""
gbm_trainer.py

Created by Faiyaz Zamal on 2011-09-16.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import logging

from trainer import Trainer
from gbm_model import GBMModel

from dataset import DataSet
import rpy2.robjects as ro
from rpy2.robjects.packages import importr

class GBMTrainer(Trainer):
	
	def configure(self,settings):
		"""
		This method configures the trainer.  settings is a dictionary of attributes (keys) and attribute values (values).
		
		This method is called directly after the trainer object is instantiated.
		"""
		
		self.trainer_settings=settings
		
	#
	def load_model(self,saved_model_file):
		"""
		This method is used to return the saved model object.
		"""	
		return(GBMModel.load(saved_model_file))
		
	def train(self,data_set):
		"""
		This method accepts a data set and returns a model which has been trained on
		the data set.
		"""
		logging.debug ('Training on dataset ')
		logging.debug (data_set.get_items())
		
		#
		trainer_package_parameters=self.trainer_settings['trainer_package_parameters']
		if('shrinkage' not in trainer_package_parameters):
			trainer_package_parameters['shrinkage']=0.001
		#
		if('n_trees' not in trainer_package_parameters):
			trainer_package_parameters['n_trees']=10000
		
		
		[features,labels,label_conversion_dict]=self.create_training_set(data_set)
		gbm_package=importr('gbm')
		
		gbm_object=gbm_package.gbm_fit(features,labels,shrinkage=trainer_package_parameters['shrinkage'],n_trees=trainer_package_parameters['n_trees'],verbose=True)
		model_object=GBMModel(gbm_object,label_conversion_dict)
		
		return(model_object)
		#return(learned_model_object)
	#
	#
	# Helper method
	# creates a training set file for the gbm package
	# returns a tuple (feature_matrix,label_matrix,label_conversion_dict)
	# The dictionary is needed because GBM accepts only 0/1 labeling for bernoulli distribution.
	# same label conversion dict should be used by the predictors. 
	
	def create_training_set(self,data_set):
		feature_matrix=[]
		label_vector=[]
		items=data_set.get_items()
		label_conversion_dict={}
		current_label=0
		if(items is not None):
			for item in items:
				# find the label
				label=data_set.get_label(item)
				if(label not in label_conversion_dict):
					label_conversion_dict[label]=current_label
					current_label+=1
				#
				label_vector.append(label_conversion_dict[label])
				
				# find the feature vector
				# it is a numpy array
				features=data_set.get_features(item)
				feature_matrix.extend(features)
		#
		# Now convert the feature_matrix and label_vector to r objects
		r_label_vector=ro.FloatVector(label_vector)
		r_feature_vector=ro.FloatVector(feature_matrix)
		r_feature_matrix=ro.r.matrix(r_feature_vector,nrow=len(items),byrow=True)
		return(r_feature_matrix,r_label_vector,label_conversion_dict)
				
			
