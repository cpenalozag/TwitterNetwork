import glob
import os
import json
import argparse
import sys
from collections import defaultdict

reload(sys)
sys.setdefaultencoding('utf-8')


ap = argparse.ArgumentParser()
ap.add_argument("-s", "--screen-name", required=True, help="Screen name of twitter user")
args = vars(ap.parse_args())

SEED = args['screen_name']

users = defaultdict(lambda: {'followers': 0})
ids = []

for f in glob.glob('twitter-users/*.json'):
    print "loading " + str(f)
    data = json.load(file(f))
    screen_name = data['screen_name']
    users[screen_name] = {'followers': data['followers_count'], 'friends': data['friends_count'], 'id': data['id'],
                          'follower_ids': data['followers_ids'], 'description': data['description']. replace('\n', ' '),
                          'verified': data['verified'], 'created_at': int(data['created_at'][0:4]),
                          'listed_count': data['listed_count']}
    ids.append(data['id'])


def process_follower_list(screen_name, edges=[], depth=0, max_depth=5):
    f = os.path.join('following', screen_name + '.csv')

    if not os.path.exists(f):
        return edges

    following = [line.strip().split('\t') for line in file(f)]

    for follower_data in following:
        if len(follower_data) < 2:
            continue

        screen_name_2 = follower_data[1]

        edges.append([users[screen_name]['id'], follower_data[0]])

        if depth + 1 < max_depth:
            process_follower_list(screen_name_2, edges, depth + 1, max_depth)

    return edges


edges = process_follower_list(SEED, max_depth=5)

for user in users:
    for id in users[user]['follower_ids']:
        if id in ids:
            edges.append([id, users[user]['id']])

with open('network-data/vertices.csv', 'w') as outf:
    outf.write('id,screen_name,followers,friends,verified,description,created_at,listed\n')
    for user in users:
        outf.write(
            '%d,%s,%d,%d,%s,%s,%s,%s\n' % (users[user]['id'], user, users[user]['followers'], users[user]['friends'],
                                           users[user]['verified'], users[user]['description'].replace(',',';'),
                                           users[user]['created_at'], users[user]['listed_count']))

with open('network-data/edges.csv', 'w') as outf:
    outf.write('source,target\n')
    edge_exists = {}
    for edge in edges:
        key = ','.join([str(x) for x in edge])
        if not (key in edge_exists):
            outf.write('%s,%s\n' % (edge[0], edge[1]))
            edge_exists[key] = True
