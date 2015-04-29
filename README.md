# Humanizr: Bringing back the humanity to Twitter

# Summary

Humanizr is a software library and off-the-shelf tool for classifying Twitter
accounts as belonging to either an individual or an organization (e.g., a
corporation or social group).

# Why you need Humanizr:

Humanizr is an essential tool for researchers working on Twitter who want perform studies such as:

  * Model human populations through their content and social connections
  * Use the content of Twitter accounts to predict phenomenon such as elections,
    epidemics, or rumor-spreading
  * Observe the dynamics of how information flows between accounts over time.

Humanizr lets you clearly identify which account belong to individual people and
those representing organizations.  Without Humanizr, all Twitter accounts appear
the same, which runs the significant risk when modeling <em>people</em>-specific
phenomena of incorporating a noise from non-human accounts.  For example, a
study looking for flu-related keywords could be mis-influenced by News-media
accounts reporting about flu symptoms elsewhere; or, when trying to predict
elections by candidate interest, a study could be thrown off by news reporting
of the candidates.  Humanizr solves these problems by identifying individuals'
Twitter accounts.

Alternately, Humanizr provides an unparalleled view in <em>organizations</em>
and how they they behave.  Humanizr enables researchers to study how individuals
and organizations interact, all the way from examining how content created by
organizations reaches individuals to how individuals converse with organizations
(e.g., local clubs or small businesses).

# Installation and Usage:

In the top level directory, run:

<code>./install.sh [--user]</code>

Once installed, to use the classifier

    ./classify_organizations.sh [-h] [-o] tweet_dir
     -h Help. Display this message and quit
     -o Output_path/filename. If no path is specified, default is current_directory/output.tsv
     tweet_dir Directory to tweet JSON files</code>

The directory of tweet JSON files must be a path to a directory where files
contain tweet JSON objects in the [Twitter
format](https://dev.twitter.com/overview/api/tweets). The objects can be spread
across any number of files, and one file can contain any number of JSON objects
(one per line), but each object can only contain one tweet. In other words, each
tweet will have its own JSON object including tweet and user information as
returned by the Twitter REST API.

The output of the classifier is a two-column .tsv file where for each line, the
first column is a user ID, and the second column is the classification (org =
organization/per = individual).
