-------------- Twitter Account Organization-Personal Classifier ----------------------

Author: James McCorriston, Faiyaz Zamal, Wendy Liu
License: 


Installation Instructions:

	run ./install.sh in the top-level directory (run with --user for local installation)


Run Instructions:

	Usage: ./classify_organizations.sh [-h] [-o] tweet_dir
		  -h  Help. Display this message and quit.
		  -o  Output_path/filename. If no path is specified, current directory is default.
		  tweet_dir   Directory to tweet JSON files.



Directory of tweet JSON files:

	Path to a directory containing tweet JSON objects. The objects can be spread across any number of files,
	and one file can contain any number of JSON objects (one per line), but each object can only contain one
	tweet. In other words, each tweet will have its own JSON object including tweet and user information as
	returned by the Twitter rest API.

Output:

	The output of the classifier is a two-column .tsv file where for each line, the first column is a user ID, 
	and the second column is the classification (org = organization/per = individual).
