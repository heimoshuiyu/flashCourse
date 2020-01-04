import requests
import json
import time
import random

sleep_time = 0.25
sleep_time_exam = 1
sleep_time_exam_random_range = 3

# 以下代码是为2019 UIC 军训安全教育课程设计的，如要用到其他课程中请注意courseId和projectId
# 打开chrome,随便你用什么手段,查到cookie acw_tc,填下去
cookies = dict()
cookies['acw_tc'] = '2760827915781535321134534e5764f397eeb4470019168b411142ecdb1a94'
#cookies['Hm_lvt_a371a0af679e5ae55fe240040f35942e'] = '1578093784'
#cookies['Hm_lpvt_a371a0af679e5ae55fe240040f35942e'] = '1578093784'

# Chrome打开到登录,在课程列表页面按下F12,
# 然后进入课程页面
# 在抓到的文件中选择listCourse.do?timestamp=xxx这个文件,xxx表示一串数字
# 选择Header,滚动到最下方,找到FromData,按下view source,复制到下面
data = 'userProjectId=a1114cff-1111-4449-a38b-71114bb711bf&chooseType=3&tenantCode=123088801&name=&userId=2b11110f-0d8a-4ace-8fda-eab4f7f29286&token=1119c813-9f69-4111-a4b8-8b56b511da96'

userId = data[data.index('userId=')+len('userId='):data.index('&token')]
tenantCode = data[data.index('tenantCode=')+len('tenantCode='):data.index('&name')]
token = data[data.index('token=')+len('token='):]




data_ent = data + '&courseId=...'
data_ent = data_ent.replace('&chooseType=3', '')
data_ent = data_ent.replace('&name=', '')

url_finished = 'https://weiban.mycourse.cn/pharos/usercourse/finish.do?userCourseId=...&tenantCode=%s&_=1578110131524' % (tenantCode)

heads = dict()
heads['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
heads['Origin'] = 'http://weiban.mycourse.cn'
heads['Referer'] = 'http://weiban.mycourse.cn/'
heads['Content-Type'] = 'application/x-www-form-urlencoded'
heads['Sec-Fetch-Site'] = 'same-origin'
heads['Sec-Fetch-Mod'] = 'cors'

url = 'https://weiban.mycourse.cn/pharos/usercourse/listCourse.do?timestamp='
data = data.encode()

url_studyDo = 'https://weiban.mycourse.cn/pharos/usercourse/study.do?timestamp='

def processCourseId(data):
    i = data.index('userCourseId=') + len('userCourseId=')
    ii = data.index('&tenantCode')
    return data[:i] + '...' + data[ii:]

#url_finished = processCourseId(url_finished)

def get_time():
    return str(int(time.time() - 1))


def doCourse(courseId, resourcesId, s):
    global data_ent
    timeStep = get_time()
    data_ent_new = data_ent.replace('...', resourceId)
    data_ent_new = data_ent_new.encode()
    heads['Sec-Fetch-Site'] = 'cross-site'
    s.headers.update(heads)

    # study.do
    rep_study = s.post(url=url_studyDo + timeStep, data=data_ent_new)
    print('进入课程,返回以下状态')
    print(rep_study.content.decode())

    time.sleep(sleep_time)

    rep_finished = s.get(url=url_finished.replace('...', courseId))
    print(rep_finished.content.decode())


s = requests.Session()
s.headers.update(heads)
requests.utils.add_dict_to_cookiejar(s.cookies, cookies)
url = url + get_time()
print(url)

# 获取目录
rep = s.post(url=url, data=data)
courses = rep.json()['data']  # courses是一个列表,包含类,类是字典

n = 0
for category in courses:  # category是一个字典,key courseList包含同类所有课程,课程是字典
    for course in category['courseList']:
        name = course['resourceName']
        if course['finished'] == 2:
            print('开始通过课程', name)
            courseId = course['userCourseId']
            resourceId = course['resourceId']
            doCourse(courseId, resourceId, s)

            print('进入暂停状态')
            time.sleep(sleep_time)


        else:
            print('跳过课程', name, '原因:已完成')
        
        n += 1
        print('进度 %d/265' % n)

''' # 最开始的设想是手动输入答案，谁知道考试有三次机会，用过一次机会就可以获得review.json，里面就包含答案
resp = s.post('https://weiban.mycourse.cn/pharos/exam/startPaper.do?timestamp='+get_time(), data=exam_data)
print(resp.json())
question_list = resp.json()['data']

with open('answer.json', 'r') as f:
    jsondata = f.read()
right_answer = json.loads(jsondata)

for question in question_list:
    option_list = question['optionList']
    if question['type'] == 1:
        question_type = '单选题：'
    elif question['type'] == 2:
        question_type = '多选题：'
    else:
        print('错误，未知类型')
        exit()
    print(question_type + question['title'])
    n = 0
    for option in option_list:
        print(str(n) + ' ' + option['content'])
        n += 1
    
    if right_answer.get(question['id']):
        print('注意！已经选择了以下选项')
        already_answer_ids = right_answer[question['id']].split(',')
        for already_answer_id in already_answer_ids:
            for option in option_list:
                if option['id'] == already_answer_id:
                    print(option['content'])
    
    answerIndexs = input('请回答：')
    if not answerIndexs:
        print('')
        continue
    answerIndexs = answerIndexs.split(' ')
    answer_list = list()
    for answerIndex in answerIndexs:
        answerIndex = int(answerIndex)
        answer_list.append(option_list[answerIndex]['id'])
    answer = ','.join(answer_list)
    right_answer[question['id']] = answer

    jsondata = json.dumps(right_answer)
    with open('answer.json', 'w') as f:
        f.write(jsondata)
    
    print('已记录数据%d条' % len(right_answer))
    print('')
'''

# 根据review生成answer的代码
'''
with open('review.json', 'rb') as f:
    data = f.read()
    data = data.decode('utf-8')
jsondata = json.loads(data)
question_list = jsondata['data']['questions']

right_answer = {} # 用于储存正确答案id的键值对
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
'''

#input('是否进入考试？（回车确认）')


# 获取examPlanId
r_id = s.post('https://weiban.mycourse.cn/pharos/exam/listPlan.do?timestamp='+get_time(), data=data)
examPlanId = r_id.json()['data'][0]['id']
print(examPlanId)

exam_data = 'userExamPlanId=%s&tenantCode=%s&userId=%s&token=%s' % (examPlanId, tenantCode, userId, token)
exam_data = exam_data.encode()

# 进入考试
with open('answer.json', 'r') as f:
    data = f.read()
right_answer = json.loads(data)

print('开始考试，服务器返回以下状态')
resp = s.post('https://weiban.mycourse.cn/pharos/exam/startPaper.do?timestamp='+get_time(), data=exam_data)
print(resp.json())

# 答题
question_list = resp.json()['data']
n = 1
for question in question_list:
    random_sleep_time = sleep_time_exam + random.randint(0, sleep_time_exam_random_range)

    question_id = question['id']
    answer_id = right_answer[question_id]

    do_data = 'userExamPlanId=%s&questionId=%s&useTime=%d&answerIds=%s&tenantCode=%s&userId=%s&token=%s' % (examPlanId, question_id, random_sleep_time, answer_id, tenantCode, userId, token)
    do_data = do_data.encode()

    print('正在做第%d题' % n)
    resp_do = s.post('https://weiban.mycourse.cn/pharos/exam/recordQuestion.do?timestamp='+get_time(), data=do_data)

    print('服务器返回状态%s' % str(resp_do.content))
    #time.sleep(sleep_time)

    n += 1

exam_finish_data = 'userExamPlanId=%s&tenantCode=%s&userId=%s&token=%s' % (examPlanId, tenantCode, userId, token)
exam_finish_data = exam_finish_data.encode()

print('开始提交考试')
resp_finish = s.post('https://weiban.mycourse.cn/pharos/exam/submitPaper.do?timestamp='+get_time(), data=exam_finish_data)

print('服务器返回以下状态')
print(resp_finish.content)
