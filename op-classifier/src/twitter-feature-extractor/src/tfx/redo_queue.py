import json
import MySQLdb

HOST_NAME = "enterprise.cs.mcgill.ca"
DB_NAME = "JM_random_network_sample"

if __name__ == '__main__':
	if len(sys.argv) == 2:
		profile = sys.argv[1]
	else:
		exit()
	db = MySQLdb.connect(host=HOST_NAME, user="jmccorriston", passwd="260409387", db=DB_NAME)
	cursor = db.cursor()

	#profiles
	temp = []
	cursor.execute('select * from %s_profiles_queue', profile)
	for row in cursor.fetchall():
		temp.append([row[0], row[1]])
	
	cursor.execute('drop table %s_profiles_queue', profile)
	cursor.execute('create table %s_profiles_queue (dbid INT not null primary key auto_increment, user_id BIGINT(15) not null, qtime DATETIME not null)' % profile)
	cursor.execute('create index %s_profiles_queue_user_id on %s_profiles_queue (user_id)', (profile, profile))
	cursor.execute('create index %s_profiles_queue_qtime on %s_profiles_queue (qtime)', (profile, profile))
	for row in temp:
		cursor.execute('insert into %s_profiles_queue values (%s, %s, %s)', ('', row[0], row[1]))
	db.commit()

	#friends
	temp = []
	cursor.execute('select * from %s_profiles_queue', profile)
	for row in cursor.fetchall():
		temp.append([row[0], row[1], row[2]])
	
	cursor.execute('drop table %s_profiles_queue', profile)
	cursor.execute('create table %s_friends_queue (dbid INT not null primary key auto_increment, user_id BIGINT(20) not null, cursor_id BIGINT(30) not null, qtime DATETIME not null)' % profile)
	cursor.execute('create index %s_friends_queue_user_id on %s_friends_queue (user_id)', (profile, profile))
	cursor.execute('create index %s_friends_queue_qtime on %s_friends_queue (qtime)', (profile, profile))
	for row in temp:
		cursor.execute('insert into %s_friends_queue values (%s, %s, %s, %s)', ('', row[0], row[1], row[2]))
	db.commit()
	
	#followers
	temp = []
	cursor.execute('select * from %s_friends_queue', profile)
	for row in cursor.fetchall():
		temp.append([row[0], row[1], row[2]])
	
	cursor.execute('drop table %s_profiles_queue', profile)
	cursor.execute('create table %s_followers_queue (dbid INT not null primary key auto_increment, user_id BIGINT(20) not null, cursor_id BIGINT(30) not null, qtime DATETIME not null)' % profile)
	cursor.execute('create index %s_followers_queue_user_id on %s_followers_queue (user_id)', (profile, profile))
	cursor.execute('create index %s_followers_queue_qtime on %s_followers_queue (qtime)', (profile, profile))
	for row in temp:
		cursor.execute('insert into %s_followers_queue values (%s, %s, %s, %s)', ('', row[0], row[1], row[2]))
	db.commit()

	#tweets
	temp = []
	cursor.execute('select * from %s_profiles_queue', profile)
	for row in cursor.fetchall():
		temp.append([row[0], row[1]])
	
	cursor.execute('drop table %s_profiles_queue', profile)
	cursor.execute('create table %s_tweets_queue (dbid INT not null primary key auto_increment, user_id BIGINT(20) not null, qtime DATETIME not null)' % profile)
	cursor.execute('create index %s_tweets_queue_user_id on %s_tweets_queue (user_id)', (profile, profile))
	cursor.execute('create index %s_tweets_queue_qtime on %s_tweets_queue (qtime)', (profile, profile))
	for row in temp:
		cursor.execute('insert into %s_tweets_queue values (%s, %s, %s)', ('', row[0], row[1]))
	db.commit()

