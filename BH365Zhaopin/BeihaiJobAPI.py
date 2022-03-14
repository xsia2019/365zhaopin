# 查询北海365招聘网上的职位信息
# https://www.365zhaopin.com/
# author: kinofgl
# -*- coding: utf-8 -*-

import random
import re
import time
import requests
from bs4 import BeautifulSoup
from fake_user_agent.main import user_agent


class BeiHaiJobAPI(object):
    def __init__(self):
        self.headers = {'User-Agent': user_agent()}  # 取得ua
        self.url = 'https://www.365zhaopin.com/index.php?do=search&p='
        self.homepage = 'https://www.365zhaopin.com/'

    #  根据url取得网页htm内容
    def get_html(self, url):
        # 尝试3次获取网页
        num = 0
        while True:
            try:
                response = requests.get(url, headers=self.headers, timeout=30)
                return response.text
            except:
                num += 1
                print('第 %s 次获取网页内容失败，重新获取...' % num)
                # 尝试3次不成功则放弃
                if num < 3:
                    time.sleep(random.randint(1, 10))  # 随机休眠1-10秒
                    continue
                else:
                    break

    #  获取页数
    def get_page_num(self):
        try:
            html = self.get_html(self.url + str(1))
            soup = BeautifulSoup(html, 'lxml')
            page_num = soup.select('div.clearfix.mt20.msg-column.f14 > div > span')[0].get_text().strip()[2:5]
            return int(page_num)
        except Exception as e:
            print(e)
            return '获取页数失败'

    # 获取所有职位链接
    def get_job_url(self):
        job_url = []
        try:
            # 获取页数
            page_num = self.get_page_num()
            # 遍历页数
            for page in range(1, page_num + 1):
                url = self.url + str(page)
                html = self.get_html(url)
                # 获取职位链接
                soup = BeautifulSoup(html, 'lxml')
                job_items = soup.select('div.w1024.f-yehei > div.main-ul > ul > li')

                for job in job_items:
                    url = self.homepage + job.find('div', class_='panl1').find('a')['href']
                    job_url.append(url)

            return job_url
        except Exception as e:
            print(e)
            return '获取链接失败'

    #  解析网页内容
    def get_job_info(self, response):
        job_info = []
        try:
            soup = BeautifulSoup(response, 'lxml')
            # 取得当前页面所有的职位信息
            job_items = soup.select('div.w1024.f-yehei > div.main-ul > ul > li')
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
                # 详情链接
                url = self.homepage + job_item.find('div', class_='panl1').find('a')['href']

                # 处理工资
                if re.search(r'（底薪([\d]{4,6}[-]?){1,2}', salary):
                    salary = re.search(r'（底薪([\d]{4,6}[-]?){1,2}', salary).group()[3:]
                elif re.search(r'面议', salary):
                    salary = 0
                elif re.search(r'￥([\d]{2,6}[-]?){1,2}', salary):
                    salary = re.search(r'￥([\d]{2,6}[-]?){1,2}', salary).group()[1:]
                else:
                    salary = salary

                if salary == 0:
                    salary = '0'
                elif '-' in salary:
                    salary = salary.split('-')
                    salary = salary[0]
                else:
                    salary = re.search(r'\d{2,6}', salary).group().strip()

                list = [title, salary, company, date, url]
                job_info.append(list)
            return job_info

        except Exception as e:
            print(e)
            return '解析错误'

    #  获取职位信息
    def get_job_now(self, salary):
        job_list = []
        page_num = self.get_page_num()
        for i in range(1, page_num + 1):
            # 开始抓取
            html = self.get_html(self.url + str(i))
            job_info = self.get_job_info(html)
            # 如果不是今天的信息，中止抓取
            if job_info[0][3] != '今天':
                break

            for item in job_info:
                if int(item[1]) >= salary and \
                        re.search(r'(助理)|(副总)|(行政)|(主管)', item[0]) and \
                        item[3] == '今天':
                    job_list.append(item)
                    pass
                else:
                    continue
        # 处理职位信息
        job_message = ''
        # 发送消息
        for job in job_list:
            job_title = job[0][:4] + ', '
            job_salary = job[1][:5] + ', '
            job_company = job[2][:4] + ', '
            job_date = job[3][:2] + ', '
            job_url = '[详情](' + job[4] + ')'

            job_message += job_title + job_salary + job_company + job_date + job_url + '  \n  '

        return job_list, job_message

    #  取得所有职位信息
    def get_job_all(self):
        job_list = []
        page_num = self.get_page_num()
        for i in range(1, page_num + 1):
            # 开始抓取
            print('开始抓取 %s ' % self.url + str(i))
            html = self.get_html(self.url + str(i))

            job_info = self.get_job_info(html)
            for job in job_info:
                job_list.append(job)

        return job_list