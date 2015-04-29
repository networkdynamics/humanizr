import json

from tfx import errors, utils


class ConfParser:
    """
    Only checks for correctly-formatted conf files, with all the
    necessary keys present, etc. It will check that all the values (and the
    values of any nested dictionaries and lists) are the right type and
    length and whatever else it can check. It won't check things like
    valid database arguments or feature names (done by the relevant module).
    """
    def load(self, filename):
        self.filename = filename
        # Make sure the file exists and is readable
        try:
            conf_file = open(filename, 'rt')
        except IOError:
            raise errors.ConfFileError("The conf file cannot be read.")

        # Make sure the file is properly-structured JSON
        try:
            conf = json.load(conf_file)
        except ValueError:
            raise errors.ConfFileError("The conf file does not contain valid "
                                       "JSON.")

        self.parse(conf)

    def parse(self, conf):
        self.conf = conf

        # mysql must be undefined or a dictionary
        #if type(self.mysql) is not dict:
            #raise errors.ConfFileError("mysql must contain a dictionary.")

        # Make sure the MySQL dictionary has all the needed keys
        #mysql_keys = ('host', 'user', 'passwd', 'db')
        #if any(map(lambda k: k not in self.mysql, mysql_keys)):
        #    raise errors.ConfFileError("The MySQL dictionary needs: %s" %
        #                      ', '.join(mysql_keys))

        # Attribute must be defined as a string and must not be empty
        if (not utils.is_str(self.attribute) or
            self.attribute == ''):
            raise errors.ConfFileError("The dataset's attribute is required.")

        # Labels must be defined
        if type(self.labels) is not dict:
            raise errors.ConfFileError("Labels must be a dictionary.")

        # There must be exactly two labels (binary classifier)
        if len(self.labels) < 1:
            raise errors.ConfFileError("There must be at least 1 label.")

        # Limit must be set (a non-negative integer)
        if type(self.limit) is not int or self.limit < 0:
            raise errors.ConfFileError("The limit must be >= 0.")

        # If ignore_start is set, it should be a non-negative int
        if (self.ignore_start is not None and
            (type(self.ignore_start) is not int or
                self.ignore_start < 0)):
                raise errors.ConfFileError("The starting index of the section "
                                           "to ignore must be a "
                                           "non-negative integer.")

        # If ignore_number is set, it should be a non-negative int
        if (self.ignore_number is not None and
            (type(self.ignore_number) is not int or
                self.ignore_number < 0)):
                raise errors.ConfFileError("The number to ignore must be a "
                                           "non-negative integer.")

        # If one is set, the other must be set too
        ignore_start_set = self.ignore_start is not None
        ignore_number_set = self.ignore_number is not None
        if ignore_start_set != ignore_number_set:
            raise errors.ConfFileError("Both the number to ignore and the "
                                       "starting index of the section to "
                                       "ignore must be set.")

        # Make sure both values for the features dictionary are ints
        if any(map(lambda v: type(v) is not int, self.labels.values())):
            raise errors.ConfFileError("The label values must be integers.")

        # Features must be defined (each must be explicitly enabled)
        if type(self.features) is not dict:
            raise errors.ConfFileError("Features must be a dictionary.")

        if 'enabled' not in self.features:
            raise errors.ConfFileError("You must set the enabled features.")

        enabled = self.features['enabled']
        # enabled must be defined - non-empty dict, keys are non-empty strings
        if (type(enabled) is not dict or len(enabled) < 1 or
            any(map(lambda x: x == '' or not utils.is_str(x), enabled))):
            raise errors.ConfFileError("features.enabled must be a dict of "
                                       "at least 1 non-empty string.")

        # All of the values in the enabled dictionary must be dictionaries
        if any(map(lambda x: type(x) is not dict, enabled.values())):
            raise errors.ConfFileError("All the values in features.enabled "
                                       "must be dictionaries.")


        # All the keys in default_params must also be strings
        if 'default_params' in self.features:
            params = self.features['default_params']
            if any(map(lambda x: x == '' or not utils.is_str(x), params)):
                raise errors.ConfFileError("All the keys in default_params "
                                           "dictionary must be strings.")

        # Output file must be either undefined or a non-empty string
        if (self.output_file is not None and
            (not utils.is_str(self.output_file) or self.output_file == '')):
            raise errors.ConfFileError("The output file must be a non-empty "
                                       "string.")

        # Output file was not specified - default to the filename + _output
        if not self.output_file:
            if self.filename.endswith('.json'):
                self.conf['output_file'] = self.filename[:-5] + '_output' + '.json'
            else:
                self.conf['output_file'] = self.filename + '_output'

        # Everything is fine. Return true.
        return True

    def __contains__(self, name):
        return name in self.conf

    def __getattr__(self, name):
        # Looks it up in the self.conf dictionary; if not there, return None
        if name in self.conf:
            return self.conf[name]
