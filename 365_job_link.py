# 用于获得所有的职位链接

import requests
from bs4 import BeautifulSoup
from fake_user_agent.main import user_agent
import time
import random
import pandas as pd
import csv


# 1.1 解析链接返回的HTML
def get_html_text(url):
    # 生成一个user_agent
    ua = user_agent()
    headers = {'User-Agent': ua}
    while True:
        try:
            # 设置随机的请求时间
            time.sleep(random.randint(1, 3))
            # 获取网页的HTML
            html = requests.get(url, headers=headers, timeout=30).text
            # 打印成功的链接
            print('获取HTML成功：', url)
            # 返回HTML
            return html, url
            break
        except:
            print('网络错误，正在重新请求', url)
            continue


# 1.2 解析HTML得到职位详情链接
def get_job_link(html):
    soup = BeautifulSoup(html, 'lxml')
    # 获取所有的职位详情链接
    job_links = soup.select('ul > li > div.panl1 > h3 > a')

    # 创建一个空列表，用于存放所有的职位链接
    job_link_list = []
    for i in range(len(job_links)):
        link = 'https://www.365zhaopin.com/' + job_links[i].get('href')
        job_link_list.append(link)

    return job_link_list


# 1.5 保存职位信息到csv文件
def save_csv(filepath, list):
    df = pd.DataFrame(list)
    # 创建一个csv文件
    df.to_csv(filepath, index=False, header=False, mode='a')


# 1.6 获取页数
def get_page_num(html):
    while True:
        try:
            soup = BeautifulSoup(html, 'lxml')
            # 获取页数
            page_num = soup.select('span.ml20')[0].get_text()
            # 处理页数
            page_num = int(page_num[2:5])
            return page_num
            break
        except:
            continue


# 0. 起始页链接
url = 'https://www.365zhaopin.com/index.php?do=search&p='

# 1. csv文件
csv_file = 'job_link.csv'

# 取得日期截
basename = time.strftime("%Y%m%d", time.localtime())
csv_file = csv_file[:-4] + '_' + basename + '.csv'

# 取得总页数
html = get_html_text(url + '1')[0]
page_num = get_page_num(html)
print('总页数：', page_num)

for i in range(page_num):
    success_url = []
    job_link_all = []
    # 随机暂停一段时间
    # 生成一个随机数
    random_num = random.randint(1, 10)
    time.sleep(random_num)

    # 得到页面链接
    page_url = url + str(i + 1)
    # 解析页面链接
    html, got_url = get_html_text(page_url)
    # 解析页面链接得到职位详情链接
    job_link_list = get_job_link(html)
    # 循环职位详情链接
    success_url.append(got_url)
    job_link_all.extend(job_link_list)

    # 保存到csv文件
    save_csv(csv_file, job_link_all)
    save_csv('success_url.csv', success_url)

