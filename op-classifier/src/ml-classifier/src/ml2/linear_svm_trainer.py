#!/usr/bin/env python
# encoding: utf-8
"""
linear_svm_trainer.py

Created by Faiyaz Zamal on 2011-09-16.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import time
from trainer import Trainer
from linear_svm_model import LinearSVMModel
import subprocess

class LinearSVMTrainer(Trainer):
	_file_suffix=0
		
	def configure(self,settings):
		"""
		This method configures the trainer.  settings is a dictionary of attributes (keys) and attribute values (values).
		
		This method is called directly after the trainer object is instantiated.
		"""
		#
		'''
		'trainer_settings':\
		{\
		'training_program_path':'/Users/faiyaz/Research/codes/DemographicInference/liblinear-1.8/train',\
		'trainer_package_parameters':{'-s':'2','-c':'1','-B':'-1','-v':'2'},\
		'training_set_directory':'/Users/faiyaz/Research/codes/DemographicInference/liblinear-1.8/experiment_runs/',\
		'training_set_filename':'training_set.libsvm',\
		'model_file_directory':'/Users/faiyaz/Research/codes/DemographicInference/liblinear-1.8/experiment_runs/',\
		'model_filename':'learned_model_file.liblinear',\
		'validation_set_directory':'/Users/faiyaz/Research/codes/DemographicInference/liblinear-1.8/experiment_runs/',
		'validation_set_filename':'test_set.libsvm',
		'output_file_directory':'/Users/faiyaz/Research/codes/DemographicInference/liblinear-1.8/experiment_runs/',
		'output_filename':'prediction_output',
		'predictor_program_path':'/Users/faiyaz/Research/codes/DemographicInference/liblinear-1.8/predict'\
		}\
		'''
		self.trainer_settings=settings
		# Add fixed trainer parameters
		self.trainer_settings['training_program_path']='ml2/algs/liblinear-1.8/train'
		self.trainer_settings['temporary_folder_location']='ml2/tmp/'
		self.trainer_settings['training_set_filename']='training_set.libsvm'
		self.trainer_settings['model_filename']='learned_model_file.liblinear'
		
	def train(self,data_set):
		"""
		This method accepts a data set and returns a model which has been trained on
		the data set.
		"""
		#print 'File Suffix: '+str(LinearSVMTrainer._file_suffix)
		
		print 'Training on dataset '
		print data_set.get_items()
		
		'''
		`train' Usage
		=============

		Usage: train [options] training_set_file [model_file]
		options:
		-s type : set type of solver (default 1)
		        0 -- L2-regularized logistic regression (primal)
		        1 -- L2-regularized L2-loss support vector classification (dual)
		        2 -- L2-regularized L2-loss support vector classification (primal)
		        3 -- L2-regularized L1-loss support vector classification (dual)
		        4 -- multi-class support vector classification by Crammer and Singer
		        5 -- L1-regularized L2-loss support vector classification
		        6 -- L1-regularized logistic regression
		        7 -- L2-regularized logistic regression (dual)
		-c cost : set the parameter C (default 1)
		-e epsilon : set tolerance of termination criterion
		        -s 0 and 2
		                |f'(w)|_2 <= eps*min(pos,neg)/l*|f'(w0)|_2,
		                where f is the primal function and pos/neg are # of
		                positive/negative data (default 0.01)
		        -s 1, 3, 4 and 7
		                Dual maximal violation <= eps; similar to libsvm (default 0.1)
		        -s 5 and 6
		                |f'(w)|_inf <= eps*min(pos,neg)/l*|f'(w0)|_inf,
		                where f is the primal function (default 0.01)
		-B bias : if bias >= 0, instance x becomes [x; bias]; if < 0, no bias term added (default -1)
		-wi weight: weights adjust the parameter C of different classes (see README for details)
		-v n: n-fold cross validation mode
		-q : quiet mode (no outputs)

		Option -v randomly splits the data into n parts and calculates cross
		validation accuracy on them.





		'''
		#
		trainer_package_parameters=self.trainer_settings['trainer_package_parameters']
		args=[]
		args.append(self.trainer_settings['training_program_path'])
		for param in trainer_package_parameters:
			args.append(param)
			args.append(str(trainer_package_parameters[param]))
		self.create_training_set_file_from_dataset(data_set)
		training_file_name=self.trainer_settings['temporary_folder_location']+self.trainer_settings['training_set_filename']+'_'+str(LinearSVMTrainer._file_suffix)
		
		args.append(training_file_name)
		
		model_file=self.trainer_settings['temporary_folder_location']+self.trainer_settings['model_filename']+'_'+str(LinearSVMTrainer._file_suffix)
		
		args.append(model_file)
		print args
		#print 'args for train'
		#print args
		# call train
		#os.system('touch '+model_file)
		#p=subprocess.Popen(args,stdout=subprocess.PIPE)
		fnull = open(os.devnull, 'w')
		
		p=subprocess.call(args,stdout=fnull)
		fnull.close()
		
		# TODO the persistance of models
		learned_model_object=LinearSVMModel(self.trainer_settings['temporary_folder_location'],self.trainer_settings['model_filename']+'_'+str(LinearSVMTrainer._file_suffix))
		#print learned_model_object.learned_model
		LinearSVMTrainer._file_suffix+=1
		
		return(learned_model_object)
	#
	#
	# Helper method
	# creates a training set file for the liblinear package
	def create_training_set_file_from_dataset(self,data_set):
		fout=open(self.trainer_settings['temporary_folder_location']+self.trainer_settings['training_set_filename']+'_'+str(LinearSVMTrainer._file_suffix),'w')
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
		
		
		
