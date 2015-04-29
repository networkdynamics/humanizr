import numpy
import json


class DataSet:
	def __init__(self,fname=None):
		self.__parameters = []
		self.__features = []
		self.__labels = []
		self.__items = {}
		
		if fname is not None:
			self.load(fname)

	def load(self, filename):
		#print '****'
		#print filename
		# If the file exists, open it for reading and store its contents in memory, then close it
		try:
			#file = open('census/datagen/' + filename, 'r')
			file = open(filename)
			try:
				data = json.load(file)
				file.close()

				self.__parameters = data['parameters']
				self.__features = data['features']
				self.__labels = data['parameters']['labels']
				self.__items = {}

				items = data['users']

				for item_name, item in items.iteritems():
					this_label = item['label']

					self.__items[item_name] = (item['feature_vector'], self.__labels[this_label])
			except (KeyError, ValueError):
				raise BadlyFormattedFile
		except IOError:
			raise FileNotFoundError

		# Now remove any rows that don't have the expected number of features
		# Temp measure for "Both" dataset as some users have no network data
		self.remove_problematic_rows()

	def remove_problematic_rows(self):
		try:
			max_num_features = max(len(row[0]) for row in self.__items.values())
		except:
			#print self.__items.values()
			raise
		# Uses items() instead of iteritems() because the dictionary size changes
		for key, value in self.__items.items():
			num_features = len(value[0])
			if num_features < max_num_features:
				del self.__items[key]

	def set_parameters(self, parameters):
		# Should be a list
		if type(parameters) == type([]):
			self.__parameters = parameters[:]
		else:
			raise ValueError("argument of wrong type (should be a list of parameters)")

	def get_parameters(self):
		return self.__parameters[:]

	def add_item(self, item, features, label):
		if (type(item) == type('') or type(item)==type(unicode(''))) and type(features) == type([]) and type(label) == type(1):
			self.__items[item] = (features, label)
		else:
			# Features should actually be a list of floats - how to enforce?
			raise ValueError("arguments of wrong type (should be: string, list, int)")

	def get_items(self):
		return self.__items.keys()

	def get_features(self, item):
		return self.__items[item][0][:]

	def set_feature_titles(self, titles):
		if type(titles) == type([]):
			self.__features = titles[:]
		else:
			raise ValueError

	def get_feature_titles(self):
		return self.__features[:]

	def get_label(self, item):
		return self.__items[item][1]

	def set_label_names(self, names):
		if type(names) == type([]):
			self.__labels = names[:]
		else:
			raise ValueError("label names must be a list")

	def get_label_names(self):
		return self.__labels[:]

	def rescale_feature_values(self,num_tweets):
		# This method will divide each item by the number of tweets
		# So, the feature values reflect the number of occurrence per tweets
		# TODO
		for item in self.get_items():
			features=self.__items[item][0]
			for feature_index in xrange(len(features)):
				try:
					features[feature_index]=features[feature_index]*1.0/num_tweets
				except ZeroDivisionError:
					raise
					
			
		
	def normalize_to_unit_vector(self):
		# Each feature vector is normalized to a unit vector
		for item in self.get_items():
			features=self.__items[item][0]
			# Find the norm of the feature vector
			norm=numpy.sqrt(numpy.dot(numpy.array(features),numpy.array(features)))
			for feature_index in xrange(len(features)):
				try:
			 		features[feature_index]=features[feature_index]*1.0/norm
					
				except ZeroDivisionError:
					# can only occur if the feature is a constant.
					# in this case, set the feature values to max_value
					pass
	
			
	#
	def smart_normalize(self):
		if(len(self.get_items())==0):
			return
		# else, there is at least one item.
		# we can compute the length of the feature vector.
		# assuming features are of the same length for every item.
		feature_vector_length=len(self.get_features(self.get_items()[0]))
			
		observed_min_values=[0]*feature_vector_length
		observed_max_values=[0]*feature_vector_length
		observed_mean=[0]*feature_vector_length
		observed_std=[0]*feature_vector_length
		#
		log_decision_dict=dict()
		
		for feature_index in xrange(feature_vector_length):
				feature_values=[self.get_features(item)[feature_index] for item in self.get_items()]
				
				
				observed_min_values[feature_index]=min(feature_values)
				observed_max_values[feature_index]=max(feature_values)
				observed_mean[feature_index]=numpy.mean(feature_values)
				observed_std[feature_index]=numpy.std(feature_values)
				if(observed_mean[feature_index]>observed_std[feature_index]):
					log_decision_dict[feature_index]=False
				else:
					log_decision_dict[feature_index]=True
					
		#
		for item in self.get_items():
				features=self.__items[item][0]
				for feature_index in xrange(feature_vector_length):
					if(log_decision_dict[feature_index]):
						try:
					 		features[feature_index]=numpy.log(features[feature_index]-observed_min_values[feature_index]+1)
						except :
							# can only occur if the feature is a constant.
							# in this case, set the feature values to max_value
							raise
					else:
						try:
							features[feature_index]=((features[feature_index]-observed_min_values[feature_index])*1.0/(observed_max_values[feature_index]-observed_min_values[feature_index]))*(1-0)+0
				 		except:
							pass
						
			
	def log_normalize_using_training_set_values(self,observed_min_values):
		
		if(len(self.get_items())==0):
			return
		feature_vector_length=len(self.get_features(self.get_items()[0]))
		if(feature_vector_length<>len(observed_min_values)):
				#print feature_vector_length
				#print len(observed_min_values)
				raise FeatureLengthMismatchException
		#
		for item in self.get_items():
				features=self.__items[item][0]
				for feature_index in xrange(feature_vector_length):
					try:
						#print "%f : %f" % (features[feature_index], observed_min_values[feature_index]) 
						if(features[feature_index]<observed_min_values[feature_index]):
							features[feature_index]=observed_min_values[feature_index]
					 	features[feature_index]=numpy.log(features[feature_index]-observed_min_values[feature_index]+1)
					except :
						# can only occur if the feature is a constant.
						# in this case, set the feature values to max_value
						raise
			
	def log_normalize(self):
		'''
		See http://www.cis.hut.fi/somtoolbox/package/docs2/som_norm_variable.html
		'''
		# transform the dataset into log values
		if(len(self.get_items())==0):
			return
		# else, there is at least one item.
		# we can compute the length of the feature vector.
		# assuming features are of the same length for every item.
		feature_vector_length=len(self.get_features(self.get_items()[0]))
			
		observed_min_values=[0]*feature_vector_length
		observed_max_values=[0]*feature_vector_length
		# For each feature
		for feature_index in xrange(feature_vector_length):
				feature_values=[self.get_features(item)[feature_index] for item in self.get_items()]
				
				
				observed_min_values[feature_index]=min(feature_values)
				observed_max_values[feature_index]=max(feature_values)
				
		
		
		for item in self.get_items():
				features=self.__items[item][0]
				for feature_index in xrange(feature_vector_length):
					try:
					 	features[feature_index]=numpy.log(features[feature_index]-observed_min_values[feature_index]+1)
					except :
						# can only occur if the feature is a constant.
						# in this case, set the feature values to max_value
						raise
		return(observed_min_values)
	def normalize_linear(self,min_value=0,max_value=1):
		# Normalize the dataset so that the values of all the features
		# ranges from min_value and max_value.
		# Linear normalization is used.
		if((type(min_value)==type(1.0) or type(min_value)==type(1))): #and (type(max_value)=type(1.0) or type(max_value)==type(1)) ):
			if(max_value<=min_value):
				raise ValueError("max_value must be less than min_value") 
			# if there is no item, nothing to do.
			if(len(self.get_items())==0):
				return
			# else, there is at least one item.
			# we can compute the length of the feature vector.
			# assuming features are of the same length for every item.
			feature_vector_length=len(self.get_features(self.get_items()[0]))
			# if empty feature vector, do nothing.
			if(feature_vector_length==0):
				return
			# First compute the observed min and max values for all the features.
			
			observed_min_values=[0]*feature_vector_length
			observed_max_values=[0]*feature_vector_length
			# For each feature
			for feature_index in xrange(feature_vector_length):
				feature_values=[self.get_features(item)[feature_index] for item in self.get_items()]
				
				
				observed_min_values[feature_index]=min(feature_values)
				observed_max_values[feature_index]=max(feature_values)
			
			
			# now that we know the range for each feature, we can apply the change into the dataset	
			
			for item in self.get_items():
					features=self.__items[item][0]
					for feature_index in xrange(feature_vector_length):
						try:
					 		features[feature_index]=((features[feature_index]-observed_min_values[feature_index])*1.0/(observed_max_values[feature_index]-observed_min_values[feature_index]))*(max_value-min_value)+min_value
							
						except ZeroDivisionError:
							# can only occur if the feature is a constant.
							# in this case, set the feature values to max_value
							features[feature_index]=max_value
					
			
				
				
		else:
			raise ValueError("min_value and max_value must be either float or int")
	#
	''' 		
	def filter_feature_by_name(self,features_to_filter):
		if type(feature_indices_to_filter) == type([]):
			# Compose the feature indices from feature names
			composite_feature_names=self.__features
			feature_indices_dict=dict()
			current_index=0
			for name in composite_feature_names:
				if(',' in composite_feature_names):
					# it is a composite features
					feature_name=name.split()[0]
					#num_member_features=name.split(',')
					k=int(self.__parameters[0].split('=')[1])
					
					num_member_features=k*2
					feature_indices_dict[feature_name]=[current_index:current_index+num_member_features-1]
					current_index+=num_member_features
				else:
					feature_name=name.split()[0]
					feature_indices_dict[feature_name]=[current_index]
					current_index+=1
			#
			feature_indices_to_filter=[]
			for feature_name in features_to_filter:
				feature_indices_to_filter.extend(feature_indices_dict[feature_name])
			#
			self._filter_features_by_index(feature_indices_to_filter)
			
			# TODO filtering the feature list
					
					
		else:
			raise ValueError("Features to filter must be a list")
			
	'''			
		
		
	# Filtering features by index
	# feature_indices_to_filter is a list of feature indices that need to be filtered.
	# This does not check if it is deleting part of  composite features, 
	# so it should not be called directly.
	def _filter_features_by_index(self,feature_indices_to_filter):
		if type(feature_indices_to_filter) == type([]):
			if(len(self.get_items())==0):
				return
			#
			feature_vector_length=len(self.get_features(self.get_items()[0]))
			# if empty feature vector, do nothing.
			if(feature_vector_length==0):
				return 
			# if feature_indices contain a feature index >= feature_vector_length raise error
			if(max(feature_indices_to_filter)>=feature_vector_length):
				raise ValueError("Feature indices exceed feature vector size")
			for item in self.get_items():
				orig_features=self.__items[item][0]
				label=self.__items[item][1]
				new_feature_vector=[]
				for feature_index in xrange(feature_vector_length):
					if(feature_index not in feature_indices_to_filter):
						new_feature_vector.append(orig_features[feature_index])
				# Now replace the items features by the new one
				self.__items[item] = (new_feature_vector, label)
			
				
			
					
				
				
			
		else:
			raise ValueError("Feature indices must be a list")
		
		
		
	  
	
		
		
		

class BadlyFormattedFile(Exception):
	pass
class FeatureLengthMismatchException(Exception):
	pass

class FileNotFoundError(Exception):
	pass
