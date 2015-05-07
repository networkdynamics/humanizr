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
import cPickle as pickle
import json
import tempfile



class LibSVMModel(Model):
	# Liblinear package model
	# each model is actually referring to a file
	_file_suffix=os.getpid()
	
	def __init__(self,tmp_folder_location,model_file,grid_search=False,c=0,g=0):
		self._tmp_folder_location=tmp_folder_location
		self._orig_model_file=model_file
		self._model_file=os.path.join(tmp_folder_location,model_file)
		self._predictor_package_path='svm-predict'
		
		self._output_filename=os.path.join(tmp_folder_location,'output_file')
		if(grid_search==False):
			self._test_file_name=os.path.join(tmp_folder_location,'test_set.libsvm'+'_'+str(LibSVMModel._file_suffix))
			self._output_filename=os.path.join(tmp_folder_location,'output_file'+'_'+str(LibSVMModel._file_suffix))
		else:
			self._test_file_name=os.path.join(tmp_folder_location,'grid_search_test_dataset.libsvm')#+'_'+str(c)+'_'+str(g)
			
	def change_file_suffix(self,new_suffix):
		LibSVMModel._file_suffix=new_suffix
	#
	def save(self,model_file_location,normalization_min_values=None):
		save_dict=dict()
		save_dict['normalization_min_values']=normalization_min_values
		#save_dict['_tmp_folder_location']=self._tmp_folder_location
		
		# commented out Nov 18. 2014
		#save_dict['_tmp_folder_location']="saved_model_information/"
		save_dict['_tmp_folder_location']=self._tmp_folder_location
		
		
		save_dict['_model_file']=self._orig_model_file
		save_dict['_file_suffix']=LibSVMModel._file_suffix
		
		# Now copy the _orig_model_file to the _tmp_folder_location
		# commented out Nov 18. 2014
		#os.system('cp '+self._tmp_folder_location+self._orig_model_file+' '+save_dict['_tmp_folder_location'])
		fin=open(os.path.join(self._tmp_folder_location,self._orig_model_file))

		save_dict['model_file_data']=fin.read()
		fin.close()
		#self._tmp_folder_location=save_dict['_tmp_folder_location']
		#fout=open(model_file_location,'w')
		#pickle.dump(save_dict,fout)
		#fout.close()
		fout=open(model_file_location,'w')
		fout.write(json.dumps(save_dict,fout))
		fout.close()
		
		
		
	@staticmethod
	def load(model_file_location):
		try:
			fin=open(model_file_location,'r')
		except:
			raise
			
		try:
			# For backward compatibility
			# try loading with pickle
			obj=pickle.load(fin)
		except: 
			try: # loading with json
				fin.close()
				fin=open(model_file_location,'r')
				
				obj=json.load(fin)
				fin.close()
			except:
				raise 
		# Now create the model file from the model_file_data
		# Nov 18. 2014
		temp_folder_location=tempfile.mkdtemp()
		fout=open(os.path.join(temp_folder_location,obj['_model_file']),'w')
		fout.write(obj['model_file_data'])
		fout.close()		
		ret=LibSVMModel(temp_folder_location,obj['_model_file'])
		ret.change_file_suffix(obj['_file_suffix'])
		fin.close()
		return(ret)
		
		
	def predict(self,data_set):
		
		"""
		This method uses the model to assign a label to each item in the data set.  The return value
		is a Prediction object.
		"""
		test_file_name=self._test_file_name+'_'+str(LibSVMModel._file_suffix)
		
		model_filename=self._model_file
		output_filename=self._output_filename
		predictor_package_path=self._predictor_package_path
		
		item_order=self.create_validation_set_file_from_dataset(data_set,test_file_name)
		
		args=[]
		
		args.append(predictor_package_path)
		args.append(test_file_name)
		args.append(model_filename)
		
		args.append(output_filename)
		#logging.debug( 'args for predict'
		#logging.debug( args
		#fnull=open(os.devnull,'w')
		#p=subprocess.Popen(args,stdout=subprocess.PIPE)
		
		p=subprocess.call(args)#,stdout=fnull)
		#fnull.close()
		'''
		for line in p.stdout:
			#logging.debug( line
			if(line.startswith('Accuracy')):
				accuracy=float(line.split()[2].split('%')[0])/100.0
				logging.debug( accuracy
				break
		'''
		#
		predicted_values=Prediction(data_set)
		#logging.debug( 'Count '+str(predicted_values.predicted_count())
		
		
		#logging.debug( output_filename
		fin=open(output_filename,'r')
		i=0
		for line in fin:
			#logging.debug( 'Output file :'+line
			item=item_order[i]
			predicted_values.set_est_label(item,line.split()[0])
			logging.debug( 'setting label for '+item)
			i+=1
		fin.close()
		#LibSVMModel._file_suffix+=1
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
