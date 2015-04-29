import json

from tfx import errors
import os

open_files = {}


class ResultParser:
    """
    Reads a result file, provides some methods for accessing things (like the
    list of features). Memoised.
    """
    def load(self, filename):
        self.filename = filename

        if filename in open_files:
            result = open_files[filename]
        else:
            try:
                result_file = open('/'.join(__file__.split('/')[:-1]) + '/' + filename, 'rt')
            except IOError:
                raise errors.ResultFileError("The specified result file '%s' "
                                             "cannot be read." % filename)
            try:
                result = json.load(result_file)
            except ValueError:
                raise errors.ResultFileError("The specified result file '%s' "
                                             "does not contain valid JSON.")

        # Store the contents of this file in a dict for easy retrieval
        open_files[filename] = result

        self.parse(result)

    def parse(self, result):
        self.result = result
        self.features = {}

        # Store the features data in a dictionary
        for i, feature in enumerate(self.result['features']):
            if 'name' in feature:
                self.features[feature['name']] = feature
            else:
                raise errors.ResultFileError("The result file does not "
                                             "contain a name for feature "
                                             "number %d" % (i + 1))

    def get_feature_data(self, feature_name):
        # Look through the features list until we find the right one
        if feature_name in self.features:
            return self.features[feature_name]
        else:
            raise errors.ResultFileError("Can't find a feature with name "
                                         "%s in the result file %s." %
                                         (feature_name, self.filename))

    def __unicode__(self):
        return self.filename
