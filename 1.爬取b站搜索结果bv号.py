import requests
import os
import json
import time
import datetime

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

# 定义搜索关键词和API地址
keyword = config["keyword"]
output_dir = config["output_dir"]
url = config["search_url"]
headers = config["headers"]
time_range = config["time_range"]
page_num = config["max_pages"]

file_path = output_dir + keyword + ".txt"
file_dir = output_dir + keyword
if os.path.isfile(file_path):
    os.remove(file_path)

# 获取筛选时间的时间戳（从若干天前的0点到今天0点）
now = datetime.datetime.now()
# 获取今天零点的时间
zero_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
# 将今天零点的时间转换为时间戳
timestamp_end = int(time.mktime(zero_today.timetuple()))

SeveralDaysAgo = (datetime.datetime.now() - datetime.timedelta(days=time_range))
zero_today1 = SeveralDaysAgo.replace(hour=0, minute=0, second=0, microsecond=0)
# 将若干天之前零点的时间转换为时间戳
timestamp_start = int(time.mktime(zero_today1.timetuple()))

for i in range(page_num):
    # 设置请求参数
    params = {
        "page": i+1,
        "keyword": keyword,
        "pubtime_begin_s": timestamp_start,
        "pubtime_end_s": timestamp_end,
    }
    # 发起GET请求
    response = requests.get(url, params=params, headers=headers)
    # 输出返回结果
    if response.status_code == 200:
        ret = response.json()
        videos = ret['data']['result'][11]['data']

        for j in range(10):
            if j >= len(videos):
                break
            print(videos[j]['title'].replace("<em class=\"keyword\">", '').replace("</em>", ''))
            with open(file_path, "a") as file:
                file.write(videos[j]['bvid'] + ' ' + str(videos[j]['aid']) + '\n')
    else:
        print(f"第{i}页请求失败，状态码: {response.status_code}")
        break
    time.sleep(1)

# 创建存放视频字幕的目录
if not os.path.exists(file_dir):
    os.makedirs(file_dir)
