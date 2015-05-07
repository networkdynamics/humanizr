#!/bin/bash

usage() {
    echo "Usage: $0 [-h] [-o] tweet_dir"
    echo "  -h  Help. Display this message and quit."
    echo "  -o  Output_path/filename. If no path is specified, current directory is default."
    echo "  tweet_dir   Directory to tweet JSON files."
    exit
}

if [[ $# == 0 ]]; then
    usage
fi

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
OUTPUT_FNAME=$DIR/output.tsv

while [[ $# > 1 ]]
do
key="$1"
case $key in
    -h|--help)
    usage
    ;;
    -o|--output)
    OUTPUT_FNAME="$2"
    shift
    ;;
esac
shift
done
OUTPUT="${OUTPUT_FNAME}"
if [[ -n $1 ]]; 
    then
        TWEET_DIR=$1
    else
        usage
fi

./op-classifier/src/twitter-feature-extractor/bin/tfx $DIR/op-classifier/src/twitter-feature-extractor/src/tfx/account_types_testing.conf $TWEET_DIR
./op-classifier/src/ml-classifier/scripts/classifier --model_file resources/model.model -o $OUTPUT $DIR/op-classifier/src/ml-classifier/src/ml2/libsvm_settings.txt /tmp/organization_personal_testing.json
