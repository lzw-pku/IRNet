import json
with open('data/train_spider.json') as f:
    data = json.load(f)
with open('data/tables.json') as f:
    table = json.load(f)
with open('data/train.json') as f:
    semql = json.load(f)


d = data[0]
print(d)
exit(0)

for t in table:
    if t['db_id'] == 'college_1':
        print(t)
        break
print(semql[0].keys())
#exit(0)
for s in semql:
    if s['question'] == 'Find the first name of student who is taking classes from accounting and Computer Info. Systems departments':
        print(s)
        print(s['rule_label'])
        print(s['query'])
        exit(0)
        break
print(data[0].keys())
print(data[0]['query'])
print(data[0]['db_id'])
for d in data:
    if len(d['query'].split()) > 80:
        print(d['question'])
        print(d['query'])
        print(d['db_id'])
