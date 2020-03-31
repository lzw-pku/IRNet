import json
for i in range(7000):
    with open(f'./data/sql/{i}.sql') as f:
        x = f.readlines()[0]
    with open(f'./data/sqlout/{i}.sql') as f:
        y = f.readlines()[0]
    '''
    if x != y:
        print(i)
        print(x)
        print(y)
        break
    '''
    if len(x.split()) > 80:
        print(x)