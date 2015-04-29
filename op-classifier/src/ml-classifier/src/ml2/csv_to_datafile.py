import csv
import json
import sys
import time
# This program converts a csv file to a training set datafile.
# The datafile json format is as follows:
# 
# 1. timestamp: The timestamp
# 2. features: List of features.
# 3. Parameters: dictionary of parameters: subfields, attribute, labels (a dict defining the labels), limit, network.
# 4. users: a dict of users (or datapoint) keyed by id. each entry contains username, feature_vector and label.
 

def read_params(argv):
	if(len(argv)<3):
		print 'Usage: csv_to_datafile.py csv_file_path data_file_path'
		sys.exit()
	params=dict()
	params['csv_file_path']=argv[1]
	params['data_file_path']=argv[2]
	return params



def main():
	params=read_params(sys.argv)
	fin=open(params['csv_file_path'])
	reader=csv.DictReader(fin)
	label_field=reader.fieldnames[-1]
	feature_fields=reader.fieldnames[:-1]


	labels= dict()
	json_file_data=dict()
	json_file_data['timestamp']=time.time()
	json_file_data['features']=feature_fields
	json_file_data['parameters']=dict()
	
	json_file_data['users']=dict()

	count=0
	label_count=0
	labels=dict()
	for line_data in reader:
		user_code=str(count)
		count+=1
		label=line_data[label_field]
		feature_vector=[]
		for field in feature_fields:
			feature_vector.append(float(line_data[field]))

		json_file_data['users'][user_code]=dict()
		json_file_data['users'][user_code]['feature_vector']=feature_vector
		json_file_data['users'][user_code]['username']=user_code


		if(label not in labels.keys()):
			label_count+=1
			labels[label]=label_count

		json_file_data['users'][user_code]['label']=label
	json_file_data['parameters']['labels']=labels
	print 'Writing '+str(len(json_file_data['users']))+' records to output file '+params['data_file_path']
	json.dump(json_file_data,open(params['data_file_path'],'w'))








	fin.close()

if __name__=='__main__':
	main()
