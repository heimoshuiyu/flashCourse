# 微伴刷课脚本

## Usage

运行 `main2.py`，根据提示输入 `data`

此处 `data` 是指进入课程列表后，浏览器 `F12` 调试工具中出现的 `listCategory.do` POST 请求中的载荷数据，格式类似 `UserID=abc123&CourseId=1234&tenantCode=666`

## 依赖

- `requests`
- `beautifulsoup4`

## 关于考试答案

来源于 `考试结果` - `作答明细` 中 `reviewPaper.do` 中返回的 json 数据

将该数据保存到 `review.json` 文件中，运行 `get_ans.py`，程序会提取问题和答案的 id 键值对然后保存到 `answer.json` 中
