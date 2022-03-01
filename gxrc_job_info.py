# 查询www.gxrc.com的工作信息
# -*- coding: utf-8 -*-
import random
import re
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from fake_user_agent.main import user_agent


# 1 获取网页内容
def get_html(url):
    num = 0
    while True:
        try:
            ua = user_agent()
            headers = {'User-Agent': ua}
            response = requests.get(url, headers=headers, timeout=30)
            return response.text
        except:
            num += 1
            print('第 %s 次获取网页内容失败，重新获取...' % num)
            # 尝试3次不成功则放弃
            if num > 3:
                time.sleep(random.randint(1, 10))  # 随机休眠1-10秒
                continue
            else:
                break


# 2 解析网页内容
def get_job_info(response):
    job_info = []
    try:
        soup = BeautifulSoup(response, 'lxml')
        # job_list = soup.find_all('div', class_='rlOne')
        job_items = soup.find_all('ul', class_='posDetailUL clearfix')
        for job_item in job_items:
            job_name = job_item.find('li', class_='w1').find('a').get_text()
            job_company = job_item.find('li', class_='w2').find('a').get_text()
            job_salary = job_item.find('li', class_='w3').get_text()
            job_location = job_item.find('li', class_='w4').get_text()
            job_time = job_item.find('li', class_='w5').get_text()
            # 处理工资
            job_salary = re.search(r'([\d]{4,6}[-]?){1,2}', job_salary).group()

            if '-' in job_salary:
                job_salary = job_salary.split('-')
                job_salary = job_salary[0]
            elif '面议' in job_salary:
                job_salary = 0
            list = [job_name, job_company, job_salary, job_location, job_time]
            job_info.append(list)
        return job_info

    except Exception as e:
        print(e)
        pass


# 3 保存职位信息到csv文件
def save_csv(filepath, list):
    df = pd.DataFrame(list)
    # 创建一个csv文件
    df.to_csv(filepath, index=False, header=False, mode='a')


# 起始链接
start_page = 'https://s.gxrc.com/sCareer?postype=5470&page='
# 存放职位信息的文件路径
gxrc_file = 'gxrc_job_info.csv'

for page_num in range(500):
    # 接收职位信息列表
    gxrc_job_info = []
    try:
        page = start_page + str(page_num + 1)
        # 随机停止获得网页内容
        time.sleep(random.randint(10, 20))
        html = get_html(page)
        # 处理网页内容
        job_info_list = get_job_info(html)

        for job_info in job_info_list:
            # 取得薪水
            job_salary = job_info[2]
            if int(job_salary) > 10000 and '北海' in job_info[3]:
                print(job_info)
                print(page)
                gxrc_job_info.append(job_info)
                save_csv(gxrc_file, gxrc_job_info)
            else:
                pass

    except Exception as e:
        print(e)
        continue
