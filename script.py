'''
import pickle
with open('generate_data.pkl', 'rb') as f:
    data = pickle.load(f)
print(len(data))
print(data[0])
exit(0)
'''



import json

with open('data/train.json') as f:
    data = json.load(f)


count = 0
for d in data:
    #print(d['query'])
    #print(' > ' in d['query'])
    #exit(0)
    if 'JOIN' in d['query']:continue
    if 'avg' in d['query']:
        count += 1

print(count)
exit(0)

with open('data/process_data.json') as f:
    process_data = json.load(f)

with open('data/train_spider.json') as f:
    init_data = json.load(f)

d = data[0]
p = process_data[0]
i = init_data[0]
print(list(sorted(d.keys())))
print(list(sorted(p.keys())))
print(list(sorted(i.keys())))

print('*' * 80)

with open('data/new_data.json') as f:
    data = json.load(f)
print(list(sorted(data[0].keys())))
with open('data/new_process_data.json') as f:
    data = json.load(f)
print(list(sorted(data[0].keys())))
with open('data/new_train.json') as f:
    data = json.load(f)
print(list(sorted(data[0].keys())))