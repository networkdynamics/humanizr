import sys
import os
import numpy

# This program assumes that the output file contains the output from multiple runs of xvalidator.

def read_params(argv):
	if(len(argv)<2):
		print 'Usage: analyze_xvalidator_output_file.py output_file '
		sys.exit()
	params=dict()
	params['output_file']=argv[1]
	
	return params
def extract_accuracy(line):
	return(float(line.split()[-1]))

def update_labelwise_precision_recall_dict(line,current_run_labelwise_precision_recall_dict):
	# the line contains information about the current fold's labelwise accuracy
	exec('current_fold_labelwise_accuracy=dict('+line+')')

	labels=current_fold_labelwise_accuracy.keys()
	if(len(labels)==1):
		# if a singleton label sample, do not consider.
		return {}
	#print line
	other_label_dict=dict()
	other_label_dict[labels[0]]=labels[1]
	other_label_dict[labels[1]]=labels[0]

	
	if(len(labels)>2):
		print 'Non binary classification.'
		return {}
	
	if(current_run_labelwise_precision_recall_dict=={}):
		for label in labels:
			current_run_labelwise_precision_recall_dict[label]={'TP':0,'TN':0,'FP':0,'FN':0}
			
	for label in labels:

		fold_true_positive_this_label=round(current_fold_labelwise_accuracy[label]['total_count']*current_fold_labelwise_accuracy[label]['accuracy'])
		fold_false_negative_this_label=round(current_fold_labelwise_accuracy[label]['total_count']*(1.0-current_fold_labelwise_accuracy[label]['accuracy']))
		fold_true_negative_this_label=round(current_fold_labelwise_accuracy[other_label_dict[label]]['total_count']*current_fold_labelwise_accuracy[other_label_dict[label]]['accuracy'])
		fold_false_positive_this_label=round(current_fold_labelwise_accuracy[other_label_dict[label]]['total_count']*(1.0-current_fold_labelwise_accuracy[other_label_dict[label]]['accuracy']))
		current_run_labelwise_precision_recall_dict[label]['TP']+=fold_true_positive_this_label
		current_run_labelwise_precision_recall_dict[label]['FN']+=fold_false_negative_this_label
		current_run_labelwise_precision_recall_dict[label]['TN']+=fold_true_negative_this_label
		current_run_labelwise_precision_recall_dict[label]['FP']+=fold_false_positive_this_label

def compute_labelwise_fscore(current_run_labelwise_precision_recall_dict):
	labelwise_fscore_dict=dict()
	for label in current_run_labelwise_precision_recall_dict:
		entry=current_run_labelwise_precision_recall_dict[label]
		precision=entry['TP']*1.0/(entry['TP']+entry['FP'])
		recall=entry['TP']*1.0/(entry['TP']+entry['FN'])
		f_score=2*precision*recall/(precision+recall)
		labelwise_fscore_dict[label]={'precision':precision,'recall':recall,'f_score':f_score}
	return labelwise_fscore_dict
#
def print_info(labelwise_fscore_dict_list):
	labels=labelwise_fscore_dict_list[0].keys()
	for label in labels:
		precision_array=[x[label]['precision'] for x in labelwise_fscore_dict_list]
		recall_array=[x[label]['recall'] for x in labelwise_fscore_dict_list]
		fscore_array=[x[label]['f_score'] for x in labelwise_fscore_dict_list]
		print 'label'+str(label)
		print 'Avg Precision '
		print numpy.mean(precision_array)
		print 'std Precision '
		print numpy.std(precision_array)
		print 'Avg Recall '
		print numpy.mean(recall_array)
		print 'std Recall '
		print numpy.std(recall_array)
		print 'Avg F score '
		print numpy.mean(fscore_array)
		print 'std F score '
		print numpy.std(fscore_array)




def read_file(filename):
	fin=open(filename)
	run_count=0
	run_accuracy_array=[]
	labelwise_fscore_dict_list=[]

	while(True):
		# skip three lines.
		fold_accuracy_array=[]

		for i in range(0,3):
			if(fin.readline()==''):
				break
		# next lines are fold accuracy
		run_count+=1
		fold_count=0
		#print run_count
		while(True):
			line=fin.readline()
			if(line.startswith('Accuracy ')):
				fold_accuracy=extract_accuracy(line)
				fold_accuracy_array.append(fold_accuracy)
				fold_count+=1
			else:
				break
		# Now line contains the first line of the predicted labels
		# for now, we just skip these lines
		for i in range(1,fold_count):
			line=fin.readline()
		line=fin.readline()

		if(line.startswith('Average')):
			avg_run_accuracy=extract_accuracy(line)
			run_accuracy_array.append(avg_run_accuracy)
		else:
			run_count-=1
			break
		current_run_labelwise_precision_recall_dict=dict()
		for i in range(fold_count):
			line=fin.readline()
			
			update_labelwise_precision_recall_dict(line,current_run_labelwise_precision_recall_dict)
		#print current_run_labelwise_precision_recall_dict
		labelwise_fscore= compute_labelwise_fscore(current_run_labelwise_precision_recall_dict)
		labelwise_fscore_dict_list.append(labelwise_fscore)
		#print labelwise_fscore
	print 'Total number of runs'
	print run_count
	print 'Avergae accuracy'
	print numpy.mean(run_accuracy_array)
	print 'Std accuracy'
	
	print numpy.std(run_accuracy_array)
	print 'Labelwise Fscores'
	print_info(labelwise_fscore_dict_list)


def main():
	params=read_params(sys.argv)
	read_file(params['output_file'])
if __name__=='__main__':
	main()
