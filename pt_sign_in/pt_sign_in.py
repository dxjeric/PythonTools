# -*- coding:utf-8 -*-
# Time:2021/10/16 16:45
# Author:Chiser
# github:  https://github.com/aLuvletter/pt_res.git

import datetime, re, time, requests, json, logging
from urllib import parse
from threading import Timer

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'


def get_page(item: json, sign_in_result: dict):
    try:
        try:
            if item['referer']:
                headers = {
                    'user-agent': user_agent,
                    'referer': item['referer'],
                    'cookie': item['cookie']
                }
        except:
            headers = {'user-agent': user_agent, 'cookie': item['cookie']}

        if 'action' in item.keys():
            data = {'action': 'sign_in'}
            response = requests.post(item['url'], headers=headers, data=data)
        elif 'data' in item.keys():
            data = {item['data']}
            response = requests.post(item['url'], headers=headers, data=data)
        else:
            response = requests.get(item['url'], headers=headers)
        if response.status_code == 200:
            response = response.text
            if '签到成功' in response or '恭喜您' in response:
                sign_in_result[item['site']] = True
            elif '重复刷新' in response or '重复' in response or '簽到過' in response or '已经打卡' or '签到过' in response:
                sign_in_result[item['site']] = True
            elif '首页' or '首頁' in response:
                sign_in_result[item['site']] = True
        else:
            sign_in_result[item['site']] = False
    except:
        sign_in_result[item['site']] = False


def send_notify(sign_in_result: dict):
    # urlcode编码
    ok_site = '%3Ccenter%3E%3Cb%3E%3Cfont%20color%3D%22%234CAF50%22%3E'
    err_site = '%3Ccenter%3E%3Cb%3E%3Cfont%20color%3D%22%23BF360C%22%3E'
    res_ok = '%5B%E7%AD%BE%E5%88%B0%E6%88%90%E5%8A%9F%5D%3C%2Ffont%3E%3C%2Fb%3E%3C%2Fcenter%3E%3Cbr%3E'
    res_err = '%5B%E7%BD%91%E7%AB%99%E6%97%A0%E6%B3%95%E8%AE%BF%E9%97%AE%5D%3C%2Ffont%3E%3C%2Fb%3E%3C%2Fcenter%3E%3Cbr%3E'

    logging.debug("sign_in_result: {}".format(sign_in_result))
    send_txt = []
    for k, v in sign_in_result.items():
        if v:
            site = ok_site + k + " " + res_ok
            send_txt.append(site)
        else:
            site = err_site + k + " " + res_err
            send_txt.append(site)

    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    headers = {
        'user_agent': user_agent,
        'Content-type': 'application/x-www-form-urlencoded'
    }
    now_time = '%3Ccenter%3E%3Cb%3E%3Cfont%20color%3D%22%2355a7e3%22%3E' + parse.unquote(
        time) + '%3C%2Ffont%3E%3C%2Fb%3E%3C%2Fcenter%3E%3Cbr%3E'
    send_str = ''.join(send_txt)
    # IYUU39484Tc2791a1718e1e8ca5351030616ef6e9252c62016
    # IYUU44612T563365f270ffcdca79d26d1083fcd14d3d29c58a
    api = 'http://iyuu.cn/IYUU44612T563365f270ffcdca79d26d1083fcd14d3d29c58a.send'
    sen_url = api + '?text=PT%E7%AD%BE%E5%88%B0%E5%8A%A9%E6%89%8B&desp=' + now_time + send_str
    requests.get(sen_url, headers=headers)


def process_sign_in(all_sign, first_sign):
    json_data = open('site.json', encoding='utf-8')
    json_data = json.load(json_data)
    total_count = 0
    sign_in_result = {}

    for item in json_data:
        if "skip" in item and item["skip"]:
            continue

        total_count += 1
        site = item["site"]
        if site not in all_sign:
            get_page(item, sign_in_result)

    sign_ok_count = 0
    for k, v in sign_in_result.items():
        if v:
            all_sign.append(k)
            sign_ok_count += 1

    if sign_ok_count > 0 or first_sign:
        send_notify(sign_in_result)

    logging.debug("total_count: {}, sites: {}".format(total_count,
                                                      len(all_sign)))
    return len(all_sign) == total_count


def timer_sign_in():
    all_sign = []
    first_sign = True
    while not process_sign_in(all_sign, first_sign):
        first_sign = False
        logging.debug("wait sign in next: {}".format(60))
        time.sleep(60)

    return True


def day_run():
    while timer_sign_in():
        now_time = time.time()
        today_zero = (now_time - (now_time - time.timezone) % 86400)
        sleep_time = today_zero + 86400 - now_time + 60
        logging.debug("sleep_time: {}".format(sleep_time))
        time.sleep(sleep_time)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] [%(levelname)s] %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S',  #注意月份和天数不要搞乱了，这里的格式化符与time模块相同
        filename=r"./sign_in.log")
    day_run()
