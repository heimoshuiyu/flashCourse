import json


with open('answer.json', 'r') as f:
    data = f.read()
right_answer = json.loads(data)

with open('review.json', 'rb') as f:
    data = f.read()
    data = data.decode('utf-8')
jsondata = json.loads(data)
question_list = jsondata['data']['questions']

for question in question_list:
    answers = list()
    option_list = question['optionList']
    for option in option_list:
        if option['isCorrect'] == 1:
            answers.append(option['id'])
    answer = ','.join(answers)
    right_answer[question['id']] = answer

with open('answer.json', 'w') as f:
    f.write(json.dumps(right_answer))

print(len(right_answer))
