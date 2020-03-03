once = False

RETRY = 39

import requests
from bs4 import BeautifulSoup
import time
import json
import random
from requests.adapters import HTTPAdapter


__author__ = '''
适用对象：岭南师范2020春季军事理论课（其他课程理论上也可
备注：如本程序生效，纯属巧合，本人不对本程序负任何法律责任
备注：出于某种奇怪的原因，密码不得少于6位字符
'''
print(__author__)

# 定义头部
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko',
'Referer': 'http://www.sjhtbook.cn/WEB/trainproject/StuClassDetail.aspx?clsno=XM000002',
'X-Requested-With': 'XMLHttpRequest',
'Content-Type': 'application/x-www-form-urlencoded',
'Origin': 'http://www.sjhtbook.cn'}

# cookies = {'ASP.NET_SessionId': 'ukgbalkqf2juh4ihirgt4nvm'}

def super_sleep(t):
    for i in range(t):
        print('\r睡眠%s/%s' % (i+1, t), end='')
        time.sleep(1)
        


# data模板样本
data_tmp = 'stuNo=_stdNo_&clsNo=_clsNo_&caiNo=_caiNo_&cst_id=_cst_id_&Exmtimes=_Exmtimes_'
# 答题url样本
exam_url_tmp = 'http://www.sjhtbook.cn/Students/XMLRequest/XMLSutGenPaper.aspx'
# 登录数据样本
login_data_tmp = 'UserNo=_UserNo_&UserPassword=_UserPassword_&UserName=&UnitNo=&LoginType=0'
# 登录url样本
login_url_tmp = 'http://www.sjhtbook.cn/Students/Ajax/ChkPoliceLogin.aspx?time=_time_'
# exam data
exam_data_tmp = '''<?xml version="1.0"?>
<genpaper>
	<ExmClsId>_ExmClsId_</ExmClsId>
	<ExmStuNo>_ExmStuNo_</ExmStuNo>
	<ExamNo>_ExamNo_</ExamNo>
	<genmode>0</genmode>
</genpaper>
'''

s = requests.Session()
s.mount('http://', HTTPAdapter(max_retries=RETRY))
s.mount('https://', HTTPAdapter(max_retries=RETRY))
s.headers.update(headers)
#s.cookies.update(cookies)

# 输入用户名密码
print('输入数据时，请不要有多余的空格或其他字符')
UserNo = input('请输入用户名 >>>')
UserPassword = input('请输入密码（留空代表123456） >>>')
if len(UserPassword) < 6:
    UserPassword = '123456'
isOnce = input('输入任意字符并按回车为单次考试模式，直接按回车为全部考试模式>>>')
if isOnce:
    once = True
else:
    once = False

# 获取主页

homepage_r = s.get('http://www.sjhtbook.cn/')
login_data = login_data_tmp.replace('_UserNo_', UserNo).replace('_UserPassword_', UserPassword)
login_r = s.post(login_url_tmp.replace('_time_', str(time.time()-1)), data=login_data)

lastiscourse = False




while True:
    # 获取课程列表
    print('获取课程列表')
    r = s.get('http://www.sjhtbook.cn/WEB/trainproject/StuClassDetail.aspx?clsno=XM000002')
    soup = BeautifulSoup(r.content, features='html.parser')
    a_list = soup.find_all('a', class_='style38')
    if a_list[-1].text == '进入答题':
        print('这是考试，生成试卷，然后跳过，继续刷课')
        if lastiscourse:
            break
        else:
            lastiscourse = True
        # time.sleep(5)
        #exit()
        word = a_list[-1]['onclick'][len('insertForm'):-1]
        word = str(word).replace('(','[').replace(')',']').replace("'", '"')
        print(word)
        exm_data = json.loads(word)
        exmClsId = exm_data[0]
        # 判断期末考试
        if exmClsId == '1210':
            print('这是期末考试，退出刷课流程')
            break
        #input('危险保护')
        stu_no = exm_data[6]
        ExamNo = exm_data[1]
        exam_data = exam_data_tmp.replace('_ExmClsId_', exmClsId).replace('_ExmStuNo_',stu_no).replace('_ExamNo_',ExamNo)
        exam_r = s.post(exam_url_tmp, data=exam_data)
        continue
    lastiscourse = False
    url = 'http://www.sjhtbook.cn/' + a_list[-1]['onclick'][len('winopen(d../../'):-3]
    print('Enter to learn %s' % url)


    # 进入课程
    print('进入课程')

    r = s.get(url)
    course_soup = BeautifulSoup(r.content, features='html.parser')

    # 解析课程中的参数
    cst_id = course_soup.find('input', id='hidcst_id')['value']
    stdNo = course_soup.find('input', id='hidstuno')['value']
    clsNo = course_soup.find('input', id='hidclsno')['value']
    caiNo = course_soup.find('input', id='hidcaino')['value']
    Exmtimes = '1'
    data = {'cst_id': cst_id, 'stdNo': stdNo, 'clsNo': clsNo, 'caiNo': caiNo, 'Exmtimes': Exmtimes}

    data = 'stuNo=201904144215&clsNo=XM000002&caiNo=KJ000251&cst_id=343061&Exmtimes=1'
    data = data_tmp.replace('_cst_id_', cst_id)
    data = data.replace('_stdNo_', stdNo)
    data = data.replace('_clsNo_', clsNo)
    data = data.replace('_caiNo_', caiNo)
    data = data.replace('_Exmtimes_', Exmtimes)


    # 解析课程中的StudyTime
    times_str = course_soup.find_all('span', id='LabStudyTime')[0].text
    print('We will learn %s mins' % times_str)
    times = int(times_str)



    s.headers.update({'Referer': url})
    #print(s.headers)
    print(data)


    for i in range(times):
        print('\r%s分 ' % str(i+1), end='')
        r = s.post('http://www.sjhtbook.cn/Students/XMLRequest/XMLSaveStudyTime3.aspx', data=data)
        #print(r.content.decode())
        #time.sleep(3)


exam_page_url_tmp = 'http://www.sjhtbook.cn/PaperAllN.aspx?exmClsId=_exmClsId_&stu_no=_stu_no_'
exam_question_data_tmp = 'ExmClsId=_ExmClsId_&ExmStuNo=_ExmStuNo_&ExmQstNo=_ExmQstNo_&ExmAsw=_ExmAsw_'
exam_finish_data_tmp = '''<?xml version="1.0"?>
<sendPaper>
	<ExmClsId>_ExmClsId_</ExmClsId>
	<ExmStuNo>_ExmStuNo_</ExmStuNo>
</sendPaper>
'''
exam_val_tmp = '''<?xml version="1.0"?>
<site><serverOK>OK</serverOK></site>
'''
final_step_tmp = 'http://www.sjhtbook.cn/psaveN.aspx?exmNo=_exmNo_&stuno=_stuno_&exmClsId=_exmClsId_&exmType=False&exmPaperLock=False&clsName=岭南师范2020春季军事理论课&exmName=_exmName_'
#&clsName=%E5%B2%AD%E5%8D%97%E5%B8%88%E8%8C%832020%E6%98%A5%E5%AD%A3%E5%86%9B%E4%BA%8B%E7%90%86%E8%AE%BA%E8%AF%BE&exmName=%E7%BB%83%E4%B9%A0%E4%B8%80
real_fin_url_tmp = 'http://www.sjhtbook.cn/aspAjax/AjaxCheckExam.aspx?stuno=_stuno_&exmClsId=_exmClsId_&cur_id=&islookscore=1&type=getresult'
abandon_data = '''<?xml version="1.0"?>
<sendPaper>
	<ExmClsId>_ExmClsId_</ExmClsId>
	<ExmStuNo>_ExmStuNo_</ExmStuNo>
</sendPaper>
'''
judge_data_tmp = '''<?xml version="1.0"?>
<judge><stuno>_stuno_</stuno><exmno>_exmno_</exmno><exmClsId>_exmClsId_</exmClsId></judge>
'''

print('进入考试流程')

examlist = []
for a in a_list:
    if a.text == '进入答题':
        examlist.append(a)

with open('answer.json', 'r') as f:
    jsondata = json.loads(f.read())



for a in examlist:
    if once:
        a = examlist[int(input('once >>>'))]
    print(a.text)
    word = a['onclick'][len('insertForm'):-1]
    word = str(word).replace('(','[').replace(')',']').replace("'", '"')
    # print(word)
    exm_data = json.loads(word)
    exmClsId = exm_data[0]
    stu_no = exm_data[6]
    ExamNo = exm_data[1]
    exam_data = exam_data_tmp.replace('_ExmClsId_', exmClsId).replace('_ExmStuNo_',stu_no).replace('_ExamNo_',ExamNo)
    exam_r = s.post(exam_url_tmp, data=exam_data) # 生成考试试卷

    exam_page_resp = s.get(exam_page_url_tmp.replace('_exmClsId_', exmClsId).replace('_stu_no_', stu_no))

    examlist_soup = BeautifulSoup(exam_page_resp.content, features='html.parser')
    tbody_soup = examlist_soup.find('table', style='word-break: break-all;')
    #print(tbody_soup)
    question_soup_list = tbody_soup.contents
    n = 0
    for question_soup in question_soup_list:
        n += 1
        if not n % 2:
            continue
        else:
            pass
        #print(question_soup)
        ExmQstNo = str(question_soup['id'])[2:]
        tmp_soup = question_soup.find('td', style='width:870px;')
        question = tmp_soup.p.text
        #print('question is %s' % str(question))
        #print('Answer is %s' % jsondata[question])
        #print(ExmQstNo)
        now_data = exam_question_data_tmp.replace('_ExmClsId_', exmClsId).replace('_ExmStuNo_', stu_no)

        #随机错答案
        if jsondata[question] == 'A' and random.randint(1,100) > 75:
            json_answer = 'B'
            print('我随机制造了一个错误答案')
        else:
            json_answer = jsondata[question]
        now_data = now_data.replace('_ExmQstNo_', ExmQstNo).replace('_ExmAsw_', json_answer)
        s.post('http://www.sjhtbook.cn/Students/XMLRequest/XMLSaveQstAswToServer2.aspx', data=now_data)

    print('验证试卷') # 貌似没用反正留着先
    val_resp = s.post('http://www.sjhtbook.cn/Students/XMLRequest/XMLValidate.aspx', data=exam_val_tmp)

    print('提交试卷，下发输出结果')
    finish_data = exam_finish_data_tmp.replace('_ExmClsId_',exmClsId).replace('_ExmStuNo_',stu_no)
    result_resp = s.post('http://www.sjhtbook.cn/Students/XMLRequest/XMLUpLoadPaper.aspx', data=finish_data)
    print(result_resp.content.decode())

    print('最后一步')
    exam_page_exmno_soup = BeautifulSoup(exam_page_resp.content, features='html.parser')
    exmNo = exam_page_exmno_soup.find_all('input', attrs={'name': 'ExmNO'})[0]['value']
    exmName = exam_page_exmno_soup.find_all('input', attrs={'name':'frmExmName'})[0]['value']
    print('exmNo is %s' % str(exmNo))
    final_resp = s.get(final_step_tmp.replace('_exmNo_', exmNo).replace('_stuno_', stu_no).replace('_exmClsId_', exmClsId).replace('_exmName_',exmName))
    #print(final_resp.content.decode())

    '''
    print('WTF abandon')
    abandon_now = abandon_data.replace('_ExmClsId_',exmClsId).replace('_ExmStuNo_',stu_no)
    abandon_resp = s.post('http://www.sjhtbook.cn/Students/XMLRequest/XMLcheckabandoned.aspx',data=abandon_now)
    '''

    print('评分')
    judge_data = judge_data_tmp.replace('_stuno_',stu_no).replace('_exmno_',exmNo).replace('_exmClsId_',exmClsId)
    judge_resp = s.post('http://www.sjhtbook.cn/XMLPaperJudge.aspx',data=judge_data)


    print('这真的是最后一步') # get result，可能可以省略
    real_fin_resp = s.get(real_fin_url_tmp.replace('_stuno_', stu_no).replace('_exmClsId_',exmClsId))
    #print(real_fin_resp.content.decode())

    print('安全休息')
    if once:
        exit()
    if exmNo == 'SJ000008':
        exit()
    super_sleep(100+random.randint(1,60))
