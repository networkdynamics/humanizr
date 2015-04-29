#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

if [ $1 == "--user" ];
    then
	#Installs the Feature Extractor
	echo 'Installing Feature Extractor'
        pushd $DIR/op-classifier/src/twitter-feature-extractor
        python setup.py install --user
        popd
        #Installs the SVM Classifier
	echo 'Installing SVM Classifier'
        pushd op-classifier/src/ml-classifier
        python setup.py install --user
        popd

	python setup.py install --user

    else
	#Installs the Feature Extractor
	echo 'Installing Feature Extractor'
	pushd $DIR/op-classifier/src/twitter-feature-extractor
	python setup.py install
	popd
	#Installs the SVM Classifier
	echo 'Installing SVM Classifier'
	pushd op-classifier/src/ml-classifier
	python setup.py install
	popd

	python setup.py install
fi

