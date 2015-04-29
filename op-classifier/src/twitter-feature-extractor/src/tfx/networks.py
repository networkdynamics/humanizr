class NetworkBase:
	def __init__(self, **kwargs):
		self.k = kwargs['k']

class EntireNetwork(NetworkBase):
	def get(self, user):
		return user.get_friends()

class KClosestForward(NetworkBase):
	def get(self, user):
		return user.get_mentioned_friends(self.k)

class KMostConnected(NetworkBase):
	def get(self, user):
		return user.get_popular_friends(self.k)

class KLeastConnected(NetworkBase):
	def get(self, user):
		# Try to use operator for this eventually
		return user.get_popular_friends(self.k, popular_first=False)



class PolicyBase:
	def __init__(self, all_features, network_type, k):
		self.all_features = all_features
		self.network_type = network_type
		self.k = k

class JustUserPolicy(PolicyBase):
	# Just the user ...
	def get_features(self, user):
		user_features = []
		for feature in self.all_features:
			user_features.extend(feature.extract_feature(user))
		return user_features

class JustNetworkPolicy(PolicyBase):
	# Just the friends of the user ... get the average
	# map(sum,zip(listA,listB))
	def get_features(self, user):
		features_to_average = []
		num_friends = 0
		network = self.network_type(k=self.k).get(user)
		if network:
			for friend in network:
				friend_features = []
				for feature in self.all_features:
					friend_features.extend(feature.extract_feature(friend))
				features_to_average.append(friend_features)
				num_friends += 1 # will hold the number of users we have data for (can't use user.data['num_friends'])

			return [n / num_friends for n in map(sum, zip(*features_to_average))] # passing the list as *args
		else:
			return []

class AveragePolicy(PolicyBase): # Treat the user as a really important user in the network (not just another user etc)
	# Use the JustNetworkPolicy and JustUserPolicy classes
	def get_features(self, user):
		just_network = JustNetworkPolicy(self.all_features, self.network_type, self.k).get_features(user)
		just_user = JustUserPolicy(self.all_features, self.network_type, self.k).get_features(user)
		return [n / 2.0 for n in map(sum, zip(just_network, just_user))] # divide by two (average etc)

class JoinPolicy(PolicyBase): # So user | network (averaged)
	# Instead of summing, concatenation or something lol
	def get_features(self, user):
		just_network = JustNetworkPolicy(self.all_features, self.network_type, self.k).get_features(user)
		just_user = JustUserPolicy(self.all_features, self.network_type, self.k).get_features(user)
		return just_user + just_network




types = {
	'entire': EntireNetwork,
	'closest': KClosestForward,
	'most': KMostConnected,
	'least': KLeastConnected
}

policies = {
	'user': JustUserPolicy,
	'network': JustNetworkPolicy,
	'average': AveragePolicy,
	'join': JoinPolicy,
}
