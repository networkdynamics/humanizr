Twitter feature extractor
=========================

By [Wendy Liu](http://github.networkdynamics.org/dellsystem)

Dependencies
------------

You will need the following dependencies installed on your system:

* Python 2.7
* cjson

Optional dependencies:

* [nose](http://nose.readthedocs.org/en/latest/) for unit testing. Only if you
  want to develop. Install with `pip install nose` and run the unit tests in
  the root of the repository with `nosetests`.

Usage
-----

Clone this repository:

```
git clone git@github.networkdynamics.org:demographic-inference/twitter-feature-extractor.git
```

From within the `twitter-feature-extractor` directory, run (with sudo):

```
python setup.py install
```

This will install the Python modules and will make the `tfx` script executable
from any directory. Note that this process will need to be repeated whenever
updates are released.

To use the `tfx` script, run:

```
$ tfx [path to conf file] [--debug]
```

Specify the configuration parameters in a configuration file, and pass its
filename as the first positional argument. The configuration parameters are
listed [in the next section](#configuration-parameters).

If the debug flag is specified, you'll get some debugging information as
well as the time it took to run the feature extraction.

Configuration parameters
------------------------

The configuration file should be a plain text file containing a [JSON](http://www.json.org/) dictionary. For a sample configuration file, see sample.conf.json. The keys of the dictionary are listed below, with explanations.

* `mysql`: a dictionary with the following keys: `host`, `user`, `passwd`,
  `db`, representing the hostname, username, password, and database name,
  respectively.
* `attribute`: a human-readable name for the attribute being studied (e.g.,
  "gender").  `labels`: a dictionary with two entries, one for each binary
  label. Each key is the human-readable name of the label (e.g., "male" or
* "female); each value is the ID of the label as is indicated in the `labels`
  table of the database.
* `limit`: the number of users to study per limit (an integer)
* `features`: a dictionary with two entries.
    * The value for the `enabled` key should be a dictionary, with the each key
      in this dictionary being the class name of a feature, case-sensitive
      (e.g., `KTopWords`, `NameFeature`, etc). The value for each key should be
      a dictionary containing any parameters specific to that feature. Features
      that don't require parameters (or whose parameters have been set in
      `default_params`, explained next) can simply use an empty dictionary as
      the value (`{}`).
    * The value for the `default_params` key should be a dictionary. The
      default parameters for any enabled features can be found here. For
      example, instead of having to declare a value of `k` for every k-top
      feature, one can simply set a value for `k` in `default_params`; any
      feature that makes use of a `k` parameter will first search for it within
      its own parameter dictionary (see above). If it is not present, it will
      fall back to the `k` value specified in `default_params`. This means that
      you can set different values of `k` (or any other parameter) for one or
      more particular features while using another, "default", value for the
      rest.
    * Feature file support: currently, only the k-top features support using
      the data extracted from a training set. To use the k-top entities from a
      training set, add the path to the relevant output file as `features_file`
      in either the `default_params` dictionary or the parameter dictionary for
      the specified feature(s).
* `output_file`: the path to the output file (e.g., `/tmp/somefile.json` or
  `somefile.json`)

Database schema
---------------

This script expects the following tables in your database, with at least the
following columns (additional columns are fine):

* `user_label_assignments`
    * `label_id`: int
    * `user_id`: int
* `user_profiles`
    * `user_id`: int
    * `json_source`: string representation of a JSON dictionary containing information about a user's profile, as provided by Twitter
    * `user_timestamp`: timestamp indicating when the profile data was _retrieved_
* `user_tweets`
    * `user_id`: int
    * `status_text`: string representation of a JSON dictionary containing information about the given tweet, as provided by Twitter
    * `tweet_timestamp`: timestamp indicating when the tweet was _created_

Getting help
------------

If you've found a bug, feel free to open an issue about it in the
[issue tracker](http://github.networkdynamics.org/demographic-inference/twitter-feature-extractor/issues).

You can also contact Wendy by email at ilostwaldo@gmail.com.

Contributing changes
--------------------

If you would like to make some changes and have them merged upstream, do the following:

1. Fork this repository under your personal account.
2. Clone your fork onto your computer.
3. Make the changes. Your Python style should follow [PEP 8](http://www.python.org/dev/peps/pep-0008/). Write or update unit tests if applicable. Run the tests and fix them if they don't all pass.
4. Commit your changes. Use [this style](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html) when writing your commit messages. Any unrelated changes should be part of separate commits.
5. Send a [pull request](http://github.networkdynamics.org/demographic-inference/twitter-feature-extractor/pull/new/master) from your fork!
