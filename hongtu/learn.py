from bs4 import BeautifulSoup
import json
import os


filename = 'answer_final_5.htm'

if os.path.exists('answer.json'):
    with open('answer.json', 'r') as f:
        jsondata = json.loads(f.read())
else:
    jsondata = {}
old = len(jsondata)
print('现有答案数量%d' % len(jsondata))

with open(filename,'rb') as f:
    raw_data = f.read()

soup = BeautifulSoup(raw_data, features='html.parser')

for i in range(1,51):
    #print(i)
    id = 'divqst' + str(i)
    div_soup = soup.find('div', id=id)
    question_all = div_soup.div.p.text
    question_font = div_soup.div.p.font.text
    question = question_all[len(question_font):]

    answer_soup = div_soup.find_all('font')[1]
    answer = answer_soup.p.next_sibling.b.text
    answer = answer[len('标准答案:['):-1]
    
    if answer == '正确':
        answer = 'YES'
    elif answer == '错误':
        answer = 'NO'

    jsondata[question] = answer
    #print(question)
    #print(answer)

with open('answer.json', 'w') as f:
    f.write(json.dumps(jsondata))
print(len(jsondata) - old)
