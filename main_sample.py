# 爬虫操作间隔,单位秒,建议不小于0.5
sleep_time = 0.5

# 下面有一些需要手动输入的参数
# 从原理上来说,是可以做到单靠一个用户名就完成整个刷课的过程
# 但由于界面不是标准html,各种数据用js处理过了
# 完全自动化会很麻烦,不值得
# 所以请手动填入数据
# Cookie用于验证身份, data用于post方法获取课程列表, data_ent用于进入课程, url_finished用于发送课程已完成指令

# 打开chrome,随便你用什么手段,查到以下三个cookie,填下去
cookies = dict()
cookies['acw_tc'] = '2760827e1577107a78390a4a6e179efe9ca1a755f0ac900c7ba987aa3ada6f'
cookies['Hm_lvt_a371a0af679e5ae55fe240040f35942e'] = '1577231303'
cookies['Hm_lpvt_a371a0af679e5ae55fe240040f35942e'] = '1512313216'

# Chrome打开到登录,在课程列表页面按下F12, 右上方选择Network,勾选上方的Preserve log
# 然后进入课程页面
# 在抓到的文件中选择listCourse.do?timestamp=xxx这个文件,xxx表示一串数字
# 选择Header,滚动到最下方,找到FromData,按下view source,复制到下面
data = 'userProjectId=52d7asdf-606a-4271-b5ae-54asdf70e87b&chooseType=3&tenantCode=362088801&name=&userId=f9asdf5f-268c-48c9-sdff-baeff216e4d9&token=1e1aaaa0-4746-4afc-b401-87fe2a5f4085'

# 同上,F12,随便点击一个课程,找到study.do?timestamp=xxx,复制source
# 将 &courseId=xxxxxxxxxxxxxxx&tent 替换为&courseId=...& 也就是说,用三个点...代替courseId原本的数据
data_ent = 'userProjectId=52dasdf8-606a-4271-b5ae-5460asdfe87b&courseId=...&tenantCode=362asdf01&userId=f9f4715f-268c-48c9-9cdf-basdf216e4d9&token=1e1asdf0-4746-4afc-b401-87feasdf4085'

# 接上步骤,完成刚刚点开的课程,不需要回到课程列表
# 找到finish.do?callback...
# 复制General中的Request URL,
# 复制完后别忘了,把userCourseId中的值替换为...哦
url_finished = 'https://weiban.mycourse.cn/pharos/usercourse/finish.do?callback=jQuery16408069094712341414_1577123412322&userCourseId=...&tenantCode=362088801&_=1571234133627'

#配置结束了,可以开始运行了,建议在cmd下运行,这样可以看到报错






import requests
import time


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
