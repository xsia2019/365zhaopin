import requests
from bs4 import BeautifulSoup
from fake_user_agent.main import user_agent
import time
import random
import pandas as pd


# 1.1 解析链接返回的HTML
def get_html_text(url):
    # 生成一个user_agent
    ua = user_agent('chrome')
    headers = {'User-Agent': ua}

    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        response.encoding = 'gbk'
        return response.text
    except:
        print("get_html_text fails")
        print('以下链接解析失败：', url)


# 1.3 解析HTML得到职位详情链接
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


# 1.4 解析职位详情里面的信息
def get_job_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    # 职位名称
    job_name = str(soup.select('span.f44.c-grey-33.j-jobname')[0].text)
    # 职位薪资
    job_salary = soup.select('div.c-red.f22')[0].text
    # 处理职位薪资为数字
    if '-' in job_salary:
        job_salary = job_salary.split('-')
        job_salary_low = int(job_salary[0][1:])
        job_salary_high = int(job_salary[1])
    else:
        job_salary_low = int(job_salary[1:])
        job_salary_high = int(job_salary[1:])

    # 职位信息列表
    job_info_list = [job_name, job_salary_low, job_salary_high]

    return job_info_list


# 1.5 保存职位信息到csv文件
def save_csv(list):
    df = pd.DataFrame(list)
    # 创建一个csv文件
    df.to_csv('job_info.csv', index=False, header=False, mode='a')


# 0. 起始页链接
url = 'https://www.365zhaopin.com/job_detail.php?do=info&job_id=224764'

# 解析页面链接
html = get_html_text(url)

# 解析职位详情链接得到职位信息
job_info_list = get_job_info(html)

# 输出职位链接和信息
job_info_list.append(url)

print(job_info_list)

