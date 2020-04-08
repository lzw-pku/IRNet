'''
import pickle
with open('generate_data.pkl', 'rb') as f:
    data = pickle.load(f)
print(len(data))
print(data[0])
exit(0)
'''
'''
import pickle
import copy
with open('new_data.pkl', 'rb') as f:
    data = pickle.load(f)
new_data = []
# ['db_id', 'query', 'query_toks', 'query_toks_no_value', 'question', 'question_toks', 'sql']
for d in data:
    #print(d['question'])
    #print(d['rule_label'])
    #print(d['mutate'])
    #exit(0)
    #print(d.keys())
    #print(d['query_toks'], d['query_toks_no_value'], d['question_toks'], d['question'])
    #exit(0)
    mutate = d['mutate']
    for q, a in zip(mutate[0], mutate[1]):
        new_d =  {'db_id': d['db_id'],
                  'query': d['query'],
                  'query_toks': d['query_toks'],
                  'query_toks_no_value': d['query_toks_no_value'],
                  'sql': d['sql'],
                  'question': q,
                  'question_toks': q.lower().split(),
                  'rule_label': a}# copy.deepcopy(d)
        #new_d.pop('mutate')
        #new_d['question'] = q
        #new_d['rule_label'] = a
        new_data.append(new_d)
    #print(d.keys())
    #exit(0)
with open('new_data.json', 'w') as f:
    import json
    json.dump(new_data, f)
    exit(0)
'''
import json
with open('data/train_spider.json') as f:
    data = json.load(f)
    print(data[0].keys())
with open('preprocess/process.json') as f:
    data = json.load(f)
    print(data[0].keys())
with open('preprocess/output.json') as f:
    data = json.load(f)
    print(data[0].keys())
    exit(0)
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