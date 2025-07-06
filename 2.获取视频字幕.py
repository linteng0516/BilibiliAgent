import requests
import time
import json

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

headers = config['headers']
output_dir = config['output_dir']
keyword = config['keyword']
get_cid_url = config['get_cid_url']
get_subtitle_url = config['get_subtitle_url']

bvid_list, aid_list = [], []
with open(output_dir + keyword + ".txt", "r") as f:
    for line in f:
        bvid, aid = line.strip().split()
        bvid_list.append(bvid)
        aid_list.append(int(aid))

for bvid, aid in zip(bvid_list, aid_list):
    cid_back = requests.get(f"{get_cid_url}?bvid={bvid}", headers=headers)
    if cid_back.status_code != 200:
        print(f'获取分P列表失败: {bvid}, 状态码: {cid_back.status_code}')
        continue
    cid_json = json.loads(cid_back.content)

    for item in cid_json['data']:
        cid = item['cid']
        part_title = item['part']
        if len(cid_json['data']) > 1:
            output_path = f"{output_dir}/{keyword}/{bvid}_P{part_title}.txt"
        else:
            output_path = f"{output_dir}/{keyword}/{bvid}.txt"
        # 设置请求参数
        params = {
            'aid': aid,
            'cid': cid,
            'isGaiaAvoided': 'false',
            'web_location': '1315873',
            'w_rid': '364cdf378b75ef6a0cee77484ce29dbb',
            'wts': int(time.time()),
        }
        wbi_resp = requests.get(get_subtitle_url, params=params, headers=headers)

        if wbi_resp.status_code != 200:
            print(f'获取字幕链接失败, 状态码: {wbi_resp.status_code}')
            continue
        if "subtitle" not in wbi_resp.json()['data'].keys():
            print(f'视频无字幕')
            continue
        subtitle_links = wbi_resp.json()['data']["subtitle"]['subtitles']
        if not subtitle_links:
            print(f'视频无字幕')
            continue
        else:
            # 下载字幕
            subtitle_url = "https:" + subtitle_links[0]['subtitle_url']
            subtitle_resp = requests.get(subtitle_url, headers=headers)

            if subtitle_resp.status_code == 200:
                # 解析JSON格式的字幕数据
                subtitle_data = json.loads(subtitle_resp.text)
                # 提取所有字幕内容
                subtitles = [item['content'] for item in subtitle_data['body']]
                with open(output_path, 'w', encoding='utf-8') as f:
                    for subtitle in subtitles:
                        f.write(f'{subtitle}\n')
                print(f'下载字幕: {output_path}')
            else:
                print(f'下载字幕失败: {output_path}, 状态码: {subtitle_resp.status_code}')
        time.sleep(1)
