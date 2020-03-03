import json

with open('answer.json', 'r') as f:
    jsondata = json.loads(f.read())

f = open('answer.txt', 'wb')
for question in jsondata:
    answer = jsondata[question]
    f.write(question.encode() + b'\nAnswer: ' + answer.encode() + b'\n\n')