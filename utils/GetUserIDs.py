import glob
import json

for f in glob.glob('twitter-users/*.json'):
    data = json.load(file(f))
    screen_name = data['screen_name']
    print(f.split('/')[1].split('.')[0], screen_name)