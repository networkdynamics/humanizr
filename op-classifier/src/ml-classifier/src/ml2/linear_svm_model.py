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



class LinearSVMModel(Model):
	# Liblinear package model
	# each model is actually referring to a file
	
	_file_suffix=0
	def __init__(self,tmp_folder_location,model_file):
		self._model_file=tmp_folder_location+model_file
		
		self._predictor_package_path='ml2/algs/liblinear-1.8/predict'
		
		self._output_filename=tmp_folder_location+'output_file'
		self._test_file_name=tmp_folder_location+'test_set.libsvm'+'_'+str(LinearSVMModel._file_suffix)
		LinearSVMModel._file_suffix+=1
		
	def predict(self,data_set):
		
		"""
		This method uses the model to assign a label to each item in the data set.  The return value
		is a Prediction object.
		"""
		test_file_name=self._test_file_name
		
		model_filename=self._model_file
		output_filename=self._output_filename
		predictor_package_path=self._predictor_package_path
		
		item_order=self.create_validation_set_file_from_dataset(data_set,test_file_name)
		
		args=[]
		
		args.append(predictor_package_path)
		args.append(test_file_name)
		args.append(model_filename)
		
		args.append(output_filename)
		args.append(' >/dev/null')
		#print 'args for predict'
		#print args
		#p=subprocess.Popen(args,stdout=subprocess.PIPE)
		fnull=open(os.devnull,'w')
		p=subprocess.call(args,stdout=fnull)
		fnull.close()
		'''
		for line in p.stdout:
			#print line
			if(line.startswith('Accuracy')):
				accuracy=float(line.split()[2].split('%')[0])/100.0
				print accuracy
				break
		#
		'''
		predicted_values=Prediction(data_set)
		#print 'Count '+str(predicted_values.predicted_count())
		
		
		#print output_filename
		fin=open(output_filename,'r')
		i=0
		for line in fin:
			#print 'Output file :'+line
			item=item_order[i]
			predicted_values.set_est_label(item,line.split()[0])
			print 'setting label for '+item
			i+=1
		fin.close()
		return(predicted_values)
	#
	#
	# helper method
	# Given the dataset object, this method creates a validation file
	
	def create_validation_set_file_from_dataset(self,data_set,test_file_name):
		fout=open(test_file_name,'w')
		items=data_set.get_items()
		
		if(items is not None):
			for item in items:
				# find the label
				label=data_set.get_label(item)
				# find the feature vector
				# it is a numpy array
				features=data_set.get_features(item)
				fout.write(str(label)+' ')
				for i in range(len(features)):
					# As the index starts from 1
					fout.write(str(i+1)+':'+str(features[i])+' ')
				fout.write('\n')
			
			
		fout.close()
		return items
	
