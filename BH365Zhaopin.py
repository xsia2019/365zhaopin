# 查询北海365招聘网上的职位信息
# https://www.365zhaopin.com/
# author: kinofgl
# -*- coding: utf-8 -*-

import random
import re
import time
import csv
import requests
from bs4 import BeautifulSoup
from fake_user_agent.main import user_agent
from requests import RequestException


class BH365Zhaopin(object):
    def __init__(self):
        self.url = 'https://www.365zhaopin.com/'
        self.headers = {'User-Agent': user_agent()}

    def get_html(self, url):
        while True:
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                return response.text
            except RequestException:
                print('网络错误，请重试')
                time.sleep(random.random() * 3)

    def get_page_num(self, html):
        while True:
            try:
                soup = BeautifulSoup(html, 'lxml')
                page_num = soup.select('span.ml20')[0].get_text()
                return int(page_num[2:5])
            except:
                return None

    def get_job_info(self, html):
        try:
            soup = BeautifulSoup(html, 'lxml')
            job_items = soup.select('div.w1024.f-yehei > div.main-ul > ul > li')
            for job_item in job_items:
                job_info = {}
                job_info['job_name'] = job_item.find('div', class_='panl1').find('a').get_text().strip()
                job_info['job_salary'] = job_item.find('div', class_='panl3 salary-panl3').get_text().strip()
                job_info['job_company'] = job_item.find('div', class_='panl10 mt3').get_text().strip()
                job_info['job_time'] = job_item.find('div', class_='panl5').get_text().strip()
                job_info['job_url'] = job_item.select('div.job-title')[0].a['href']
                yield job_info
        except:
            return None

        # 遍历职位信息
        for job_item in job_items:
            # 职位名称
            title = job_item.find('div', class_='panl1').find('a').get_text().strip()
            # 职位薪水
            salary = job_item.find('div', class_='panl3 salary-panl3').get_text().strip()
            # 公司名称
            company = job_item.find('div', class_='panl10 mt3').get_text().strip()
            # 发布日期
            date = job_item.find('div', class_='panl5').get_text().strip()

            # 处理工资
            if re.search(r'（底薪([\d]{4,6}[-]?){1,2}', salary):
                salary = re.search(r'（底薪([\d]{4,6}[-]?){1,2}', salary).group()[3:]
            elif re.search(r'面议', salary):
                salary = 0
            elif re.search(r'￥([\d]{4,6}[-]?){1,2}', salary):
                salary = re.search(r'￥([\d]{4,6}[-]?){1,2}', salary).group()[1:]
            else:
                salary = salary

            if '-' in salary:
                salary = salary.split('-')
                salary = salary[0]
            else:
                salary = re.search(r'\d{4,5}', salary).group().strip()

            list = [title, salary, company, date]
            job_info.append(list)
        return job_info

    except Exception as e:
        print(e)
        return '解析错误'


# 3 保存职位信息到csv文件
def save_csv(filepath, lists):
    with open(filepath, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(lists)





# 起始链接
start_page = r'https://www.365zhaopin.com/index.php?do=search&p='
# 存放职位信息的文件路径
csv_file = r'C:\Users\Michael\OneDrive\桌面\我的工作区\365job.csv'

# 取得日期截
basename = time.strftime("%Y%m%d", time.localtime())
csv_file = csv_file[:-4] + '_' + basename + '.csv'

# 解析第1页取得总页数
html = get_html(start_page + '1')
page_num = get_page_num(html)
print('总页数：', page_num)

for i in range(page_num):
    # 随机暂停一段时间
    time.sleep(random.randint(1, 10))
    try:
        num = 0
        # 得到页面链接
        page_url = start_page + str(i + 1)
        print('正在爬取第 %s 页' % (i + 1))
        while num < 3:
            job_info_all = []
            # 解析页面链接
            html = get_html(page_url)
            # 解析页面链接得到职位详情链接
            job_info_list = get_job_info(html)
            if len(job_info_list) > 0:
                # 循环职位详情链接
                for item in job_info_list:
                    job_name = item[0]
                    job_salary = int(item[1])
                    if int(item[1]) > 9999 and re.search(r'(助理)|(副总)|(行政)|(主管)', job_name):
                        print(item)
                        job_info_all.append(item)
                    else:
                        pass
                # 跳出while循环
                num = 3
                if len(job_info_all) > 0:
                    save_csv(csv_file, job_info_all)
            else:
                continue
    except:
        continue
