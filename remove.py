import json

www=[]
file=open('C:\Users\lenovo\PycharmProjects\user\movieplus.json','r+',encoding='utf-8')
for line in file.readlines():
    we=json.loads(line)
    print(we)
    www.append(we)
result=[]
for le in www:
    if le not in result:
        result.append(le)
print(len(result))
print(result[0])
for item in result:
    tyu = open('movie.json', 'a', encoding='utf-8')
    content = json.dumps(dict(item), ensure_ascii=False) + '\n'
    tyu.write(content)