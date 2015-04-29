import json
import logging
import os
import time

from tfx import errors, features, users, utils


class FeatureExtractor:
    def __init__(self, conf, tweet_dir):
        self.conf = conf
	self.tweet_dir = tweet_dir

        # If it isn't explicitly set, will default to conf filename + _output
        output_file = conf.output_file

        # Make sure the file doesn't already exist!
        #if os.path.isfile(output_file):
        #    raise errors.FileExistsError("The output file %s already "
        #                                  "exists! Either delete it or "
        #                                  "specify a different output file "
        #                                  "in the conf file." % output_file)

        # Initialise the user set
        user_set = users.UserSet(conf, tweet_dir)

        # Load the names of all the default features from tfx/features.py
        # Anything that doesn't start with an underscore or end with a base
        default_features = filter(utils.is_a_feature, dir(features))

        enabled_features = []
        default_params = conf.features.get('default_params', {})

        # Now load all the features
        for feature_name, params in conf.features['enabled'].iteritems():
            # First try to get it from the default features
            if feature_name in default_features:
                feature_class = getattr(features, feature_name)
                feature = feature_class(params, default_params)
                enabled_features.append(feature)

            # If that doesn't work, try to import it directly
            # Must be an instance of FeatureBase!
            # Do this later

        # Now figure out all the entities we need
        needed_entities = []
        for enabled_feature in enabled_features:
            needed_entities.extend(enabled_feature.get_needed_entities())

        needed_entities = set(needed_entities)
        # Now, save the list of entities needed
        user_set.process_entities(needed_entities)

        # Now create the JSON dictionary we will need to write
        data = {
            "parameters": {
                "attribute": conf.attribute,
                "labels": conf.labels,
                "network": conf.network,
                "limit": conf.limit,
            },
            "features": [],
            "users": {},
            "timestamp": time.time(),
            # For miscellaneous data
            "other": {}
        }

        # Now we initialise all of the needed features with the users
        features_needing_users = []
        for feature in enabled_features:
            feature.initialise(user_set.labels)

            # For features (like k-top) that need them all first
            if feature.needs_users:
                features_needing_users.append(feature)

        # Initialise things as necessary (can't avoid this)
        for label in user_set.labels:
            for user in user_set.get_users(label):
                for feature in features_needing_users:
                    feature.init_with_user(label, user)

        for feature in features_needing_users:
            feature.finish_init()

        for feature in enabled_features:
            # Also put in the feature info in the features dict above
            # Can't do it at the beginning because might not be info
            feature_info = feature.get_info()
            feature_info['name'] = str(feature)
            data['features'].append(feature_info)

        # Now we extract everything for all of the enabled features
        for label in user_set.labels:
            for user in user_set.get_users(label):
                try:
                    feature_vector = user.generate_feature_vector(enabled_features)
                except errors.UserNotNeeded as e:
                    # We don't need the data for this user. Skip this one.
                    unused_users = data['other'].get('unused_users', {})
                    unused_users[e.user_id] = e.label
                    data['other']['unused_users'] = unused_users
                    continue

                data['users'][user.user_id] = {
                    "username": user.username,
                    "feature_vector": feature_vector,
                    "label": label
                }

        #print "Saving results to file %s" % output_file

        json.dump(data, open(output_file, 'wt'), indent=4)
