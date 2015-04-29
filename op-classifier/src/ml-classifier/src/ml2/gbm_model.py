#!/usr/bin/env python
# encoding: utf-8
"""
linear_svm_model.py

Created by Faiyaz Zamal on 2011-09-16.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
from model import Model, Prediction
import subprocess
import logging
import rpy2.robjects as ro
from rpy2.robjects.packages import importr
import cPickle as pickle



class GBMModel(Model):
	# GBM Model
	# Each model is a gbm_object
	
	_file_suffix=0
	
	def __init__(self,gbm_model_object,label_conversion_dict):
		self._gbm_model_object=gbm_model_object
		self._label_conversion_dict=label_conversion_dict
		self._gbm_package=importr('gbm')
		#TODO find the best estimate of n_trees using cross validation.
		 
		self._n_trees=self._gbm_package.gbm_perf(self._gbm_model_object,method="OOB")
		print('Number of trees:')
		print(self._n_trees)
	#
	
	#
	def save(self,model_file_location):
		fout=open(model_file_location,'w')
		#pickle.dump(model_object,fout)
		save_dict=dict()
		save_dict['_gbm_model_object']=self._gbm_model_object
		save_dict['_label_conversion_dict']=self._label_conversion_dict
		pickle.dump(save_dict,fout)
		fout.close()
	@staticmethod
	def load(model_file_location):
		
		fin=open(model_file_location,'r')
		obj=pickle.load(fin)
		ret=GBMModel(obj['_gbm_model_object'],obj['_label_conversion_dict'])
		fin.close()
		return(ret)
	
	def predict(self,data_set):
		
		"""
		This method uses the model to assign a label to each item in the data set.  The return value
		is a Prediction object.
		"""
		
		predicted_values=Prediction(data_set)
		gbm_package=self._gbm_package
		gbm_object=self._gbm_model_object
		(features,labels,items)=self.create_validation_set(data_set)
		
		predicted=gbm_package.predict_gbm(gbm_object,features,n_trees=self._n_trees,type='response',verbose=False)
		item_count=0
		for item in items:
			predicted_values.set_est_label(item,self.convert_label(predicted[item_count]))
			item_count+=1
		
		
		return(predicted_values)
	#
	#
	# helper method
	# Given the dataset object, this method creates a validation file
	
	def create_validation_set(self,data_set):
		
		feature_matrix=[]
		label_vector=[]
		
		items=data_set.get_items()
		label_conversion_dict=self._label_conversion_dict
		
		if(items is not None):
			for item in items:
				# find the label
				label=data_set.get_label(item)
				if(label in label_conversion_dict):
					label_vector.append(label_conversion_dict[label])
				else:
					label_vector.append(-1)
				
				# find the feature vector
				# it is a numpy array
				features=data_set.get_features(item)
				feature_matrix.extend(features)
		#
		# Now convert the feature_matrix and label_vector to r objects
		r_label_vector=ro.FloatVector(label_vector)
		r_feature_vector=ro.FloatVector(feature_matrix)
		r_feature_matrix=ro.r.matrix(r_feature_vector,nrow=len(items),byrow=True)
		return(r_feature_matrix,r_label_vector,items)
	#
	def convert_label(self,predicted_value):
		binary_label=int(round(predicted_value))
		label_conversion_dict=self._label_conversion_dict
		rev_label_conversion_dict=dict(zip(label_conversion_dict.values(), label_conversion_dict.keys()))
		return(rev_label_conversion_dict[binary_label])
		
		
