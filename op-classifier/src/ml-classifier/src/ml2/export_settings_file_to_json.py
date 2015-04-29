#!/usr/bin/env python
# encoding: utf-8
"""
export_settings_file_to_json.py

This utility can be used to convert old style txt settings files to json settings files.

Created by Faiyaz Zamal on 2012-08-29.
Copyright (c) 2012 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import json



def main():
	if(len(sys.argv)<2):
		print 'Usage export_settings_file_to_json settings_file'
		return
	input_file=sys.argv[1]
	settings=eval(open(input_file,'r').read())
	output_file=sys.argv[1][0:sys.argv[1].find('.txt')]+'.json'
	fout=open(output_file,'w')
	fout.write(json.dumps(settings,fout))
	fout.close()

if __name__ == '__main__':
	main()

