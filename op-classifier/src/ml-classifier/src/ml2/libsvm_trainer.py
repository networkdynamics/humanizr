#!/usr/bin/env python
# encoding: utf-8
"""
libsvm_trainer.py

Created by Faiyaz Zamal on 2011-09-16.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import shutil
#import matplotlib as mplib
#mplib.use('macosx')
from trainer import Trainer
from libsvm_model import LibSVMModel
import subprocess
import numpy
from dataset import DataSet
import logging
import matplotlib.pyplot as plt
import tempfile
 
class LibSVMTrainer(Trainer):
	_file_suffix=os.getpid()
	
	def configure(self,settings):
		"""
		This method configures the trainer.  settings is a dictionary of attributes (keys) and attribute values (values).
		
		This method is called directly after the trainer object is instantiated.
		"""
		self.trainer_settings=settings
		# Add fixed trainer parameters
		base_directory=os.path.dirname(os.path.realpath(__file__))
		#print '******************'
		self.trainer_settings['training_program_path']='svm-train'
		
		#self.trainer_settings['temporary_folder_location']=os.path.join(base_directory,'tmp/')
		#if(os.path.exists(self.trainer_settings['temporary_folder_location'])==False):
		#	os.mkdir(self.trainer_settings['temporary_folder_location'])

		self.trainer_settings['temporary_folder_location']=tempfile.mkdtemp()

		
		

		self.trainer_settings['training_set_filename']='training_set.libsvm'+'_'+str(LibSVMTrainer._file_suffix)
		

		self.trainer_settings['model_filename']='learned_model_file.libsvm'+'_'+str(LibSVMTrainer._file_suffix)
		logging.debug('Temporary folder:' +self.trainer_settings['temporary_folder_location'])
	#
	def load_model(self,saved_model_file):
		"""
		This method is used to return the saved model object.
		"""	
		return(LibSVMModel.load(saved_model_file))
			
	def train(self,data_set):
		"""
		This method accepts a data set and returns a model which has been trained on
		the data set.
		"""
		logging.debug ('Training on dataset ')
		logging.debug (data_set.get_items())
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
		if(self.trainer_settings['perform_grid_search']==True):
			# perform grid search to find the best parameters
			
			(c_opt,g_opt)=self.grid_search(data_set)
			trainer_package_parameters['-c']=str(c_opt)

			trainer_package_parameters['-g']=str(g_opt)
			
		args=[]
		
		
		args.append(self.trainer_settings['training_program_path'])
		for param in trainer_package_parameters:
			args.append(param)
			args.append(str(trainer_package_parameters[param]))
		self.create_training_set_file_from_dataset(data_set)
		training_file_name=os.path.join(self.trainer_settings['temporary_folder_location'],self.trainer_settings['training_set_filename'])
		
		args.append(training_file_name)
		
		model_file=os.path.join(self.trainer_settings['temporary_folder_location'],self.trainer_settings['model_filename'])
		args.append(model_file)
		logging.debug (args)
		#logging.debug 'args for train'
		#logging.debug args
		# call train 
		#p=subprocess.Popen(args,stdout=subprocess.PIPE)
		fnull=open(os.devnull,'w')
		p=subprocess.call(args,stdout=fnull)
		fnull.close()
		
		# TODO the persistance of models
		learned_model_object=LibSVMModel(self.trainer_settings['temporary_folder_location'],self.trainer_settings['model_filename'])
		#logging.debug learned_model_object.learned_model
		#LibSVMTrainer._file_suffix+=1
		
		return(learned_model_object)
	#
	#
	# Helper method
	# creates a training set file for the liblinear package
	def create_training_set_file_from_dataset(self,data_set,outfile=''):
		if(outfile==''):
			fout=open(os.path.join(self.trainer_settings['temporary_folder_location'],self.trainer_settings['training_set_filename']),'w')#+'_'+str(LibSVMTrainer._file_suffix),'w')
		else:
			fout=open(outfile,'w')
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
	#
	def generate_folds(self,data_set,num_fold):
		"""
		Generate smaller, non-overlapping data sets from the master data set.
		The folds should be returned in a list of tuples.  Each tuple corresponds to a fold.
		t[0] is the testing fold of the data 
		, t[1] is the inverse of the fold (training fold: all the rest of the data).
		"""
		items=data_set.get_items()
		folds=[] 
		if(items is not None):
			
			for i in range(num_fold):
				# Each fold is a tuple of datasets
				# First one is the test fold,
				# The inverse fold is used for training
				folds.append((DataSet(),DataSet()))
			current_fold=0
			
			for item in items:
				
				
				folds[current_fold][0].add_item(item,data_set.get_features(item),data_set.get_label(item))
				for j in range(num_fold):
					if(j<>current_fold):
						folds[j][1].add_item(item,data_set.get_features(item),data_set.get_label(item))
						
						
				
				current_fold+=1
				if(current_fold==num_fold):
					current_fold=0
		return folds
	def grid_search(self,data_set):
		# returns the optimal c and g values for the given dataset.
		# Performs cross-validation on the training set.
		logging.debug ('Grid Search')
		logging.debug ('-----------')
		
		trainer_package_parameters=self.trainer_settings['trainer_package_parameters']
		
		c_min=self.trainer_settings['grid_search_parameters']['c_min']
		c_max=self.trainer_settings['grid_search_parameters']['c_max']
		g_min=self.trainer_settings['grid_search_parameters']['g_min']
		g_max=self.trainer_settings['grid_search_parameters']['g_max']
		accuracy_matrix=numpy.zeros((c_max-c_min+1,g_max-g_min+1))
		for c in xrange(c_min,c_max):
			logging.debug ('c :'+str(c))
			for g in xrange(g_min,g_max):
				logging.debug ('g :'+str(g))
				# Change the package parameters accrodingly
				if(self.trainer_settings['grid_search_parameters']['exp']==True):
					self.trainer_settings['trainer_package_parameters']['-c']=str(2**c)
					self.trainer_settings['trainer_package_parameters']['-g']=str(2**g)
				else:
					self.trainer_settings['trainer_package_parameters']['-c']=str(c)
					self.trainer_settings['trainer_package_parameters']['-g']=str(g)
				
				
					
				num_folds=self.trainer_settings['grid_search_parameters']['num_folds']
				self.trainer_settings['trainer_package_parameters']['-v']=str(num_folds)
				
				
				args=[]
				args.append(self.trainer_settings['training_program_path'])
				for param in trainer_package_parameters:
					args.append(param)
					args.append(str(trainer_package_parameters[param]))
				training_file_name=os.path.join(self.trainer_settings['temporary_folder_location'],'grid_search_training_set_'+'_'+str(LibSVMTrainer._file_suffix))#+str(c)+'_'+str(g)
				self.create_training_set_file_from_dataset(data_set,training_file_name)
				
				args.append(training_file_name)

				#model_file=self.trainer_settings['temporary_folder_location']+'grid_search_model_'#+str(c)+'_'+str(g)
				
				#args.append(model_file)
				logging.debug (args)
				#logging.debug 'args for train'
				#logging.debug args
				# call train 
				#p=subprocess.Popen(args,stdout=subprocess.PIPE)
				#fnull=open(os.devnull,'w')
				foutput=open(os.path.join(self.trainer_settings['temporary_folder_location'],'cross_validation_results'+'_'+str(LibSVMTrainer._file_suffix)),'w')
				p=subprocess.call(args,stdout=foutput)
				foutput.close()
				
				foutput=open(os.path.join(self.trainer_settings['temporary_folder_location'],'cross_validation_results'+'_'+str(LibSVMTrainer._file_suffix)),'r')
				
				#fnull.close()
				for line in foutput:
					if(line.startswith("Cross Validation Accuracy")):
						tokens=line.split()
						accuracy=float(tokens[4].strip('%'))
						logging.debug (accuracy)
						break
						
				
				accuracy_matrix[c-c_min,g-g_min]=accuracy
				foutput.close()
				#logging.debug 'Accuracy of '+str(c)+' '+str(g)+': '+str(numpy.mean(fold_accuracy))
		
		[c_array,g_array]=numpy.where(accuracy_matrix==accuracy_matrix.max())
		#plt.imshow(accuracy_matrix)
		#plt.colorbar()
		#plt.show()
		del self.trainer_settings['trainer_package_parameters']['-v']
		logging.debug (c_array)
		logging.debug (g_array)
		logging.debug (accuracy_matrix.max())
		
		
		
		c_value=c_array[0]
		g_value=g_array[0]
		if(self.trainer_settings['grid_search_parameters']['finer_search']==True):
			step_size=self.trainer_settings['grid_search_parameters']['step_size']
			
			# Perform a finer grid search around the c_array and g_array returned values.
			# Algorithm proposed: Start from the maximum scoring point and randomly look at the neighbours.
			# Take the best neighbor and move on until you cannot improve.
			prev_c=c_value
			prev_g=g_value
			prev_accuracy=accuracy_matrix[prev_c][prev_g]
			max_accuracy=prev_accuracy
			opt_c=prev_c
			opt_g=prev_g
			while(True):
				logging.debug('Searching for c '+str(prev_c)+' and g '+str(prev_g))
				neighbors=[(prev_c+step_size,prev_g+step_size),(prev_c+step_size,prev_g-step_size),(prev_c-step_size,prev_g+step_size),(prev_c-step_size,prev_g-step_size)]
				for (new_c,new_g) in neighbors:
					# compute the accuracy
					if(self.trainer_settings['grid_search_parameters']['exp']==True):
						self.trainer_settings['trainer_package_parameters']['-c']=str(2**(c_min+new_c))
						self.trainer_settings['trainer_package_parameters']['-g']=str(2**(g_min+new_g))
					else:
						self.trainer_settings['trainer_package_parameters']['-c']=str(c_min+new_c)
						self.trainer_settings['trainer_package_parameters']['-g']=str(g_min+new_g)



					num_folds=self.trainer_settings['grid_search_parameters']['num_folds']
					self.trainer_settings['trainer_package_parameters']['-v']=str(num_folds)


					args=[]
					args.append(self.trainer_settings['training_program_path'])
					for param in trainer_package_parameters:
						args.append(param)
						args.append(str(trainer_package_parameters[param]))
					training_file_name=os.path.join(self.trainer_settings['temporary_folder_location'],'finer_grid_search_training_set_'+'_'+str(LibSVMTrainer._file_suffix))#+str(c)+'_'+str(g)
					self.create_training_set_file_from_dataset(data_set,training_file_name)

					args.append(training_file_name)

					#model_file=self.trainer_settings['temporary_folder_location']+'grid_search_model_'#+str(c)+'_'+str(g)

					#args.append(model_file)
					logging.debug (args)
					#logging.debug 'args for train'
					#logging.debug args
					# call train 
					#p=subprocess.Popen(args,stdout=subprocess.PIPE)
					#fnull=open(os.devnull,'w')
					foutput=open(os.path.join(self.trainer_settings['temporary_folder_location'],'cross_validation_results'+'_'+str(LibSVMTrainer._file_suffix),'w'))
					p=subprocess.call(args,stdout=foutput)
					foutput.close()

					foutput=open(os.path.join(self.trainer_settings['temporary_folder_location'],'cross_validation_results'+'_'+str(LibSVMTrainer._file_suffix),'r'))

					#fnull.close()
					for line in foutput:
						if(line.startswith("Cross Validation Accuracy")):
							tokens=line.split()
							accuracy=float(tokens[4].strip('%'))
							logging.debug (accuracy)
							break
					if(accuracy>max_accuracy):
						opt_c=new_c
						opt_g=new_g
						max_accuracy=accuracy
						break
				# if no change
				if(opt_c==prev_c and opt_g==prev_g): 
					break
				else:
					prev_c=opt_c
					prev_g=opt_g
			c_value=opt_c
			g_value=opt_g				
				
		
		if(self.trainer_settings['grid_search_parameters']['exp']==True):
			return(2**(c_value+c_min),2**(g_value+g_min))
		else:
			return(c_value+c_min,g_value+g_min)
			
		
					
						
							
						
					
					
					
		
		
		
		
	
	
		
		
