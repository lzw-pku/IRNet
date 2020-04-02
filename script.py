import json

with open('data/train.json') as f:
    data = json.load(f)

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