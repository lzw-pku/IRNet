import json


with open('data/dev.json') as f:
    data = json.load(f)
print(len(data))
data = list(filter(lambda d: 'JOIN' not in d['query'], data))
with open('new_dev.json', 'w') as f:
    json.dump(data, f)
print(len(data))