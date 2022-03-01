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
    ua = user_agent('chrome')
    headers = {'User-Agent': ua}
    while True:
        try:
            # 获取网页的HTML
            html = requests.get(url, headers=headers, timeout=30).text
            # 返回HTML
            return html, url
            break
        except:
            print('网络错误，正在重新请求')
            # 设置随机的请求时间
            time.sleep(random.randint(1, 3))
            continue


# 1.4 解析职位详情里面的信息
def get_job_info(html):
    while True:
        try:
            # 解析HTML
            soup = BeautifulSoup(html, 'lxml')
            # 获取职位信息
            job_name = str(soup.select('span.f44.c-grey-33.j-jobname')[0].text.strip())
            # 获取职位薪资
            job_salary = str(soup.select('div.c-red.f22')[0].text.strip())
            # 处理职位薪资
            if '-' in job_salary:
                job_salary = job_salary.split('-')
                job_salary_low = int(job_salary[0][1:])
                job_salary_high = int(job_salary[1])
            else:
                job_salary_low = int(job_salary[1:])
                job_salary_high = int(job_salary[1:])
            # 职位信息列表
            info_list = [job_name, job_salary_low, job_salary_high]
            return info_list
            break
        except:
            print("get_job_info fails")
            time.sleep(random.randint(1, 3))
            continue


# 1.5 保存职位信息到csv文件
def save_csv(filepath, list):
    df = pd.DataFrame(list)
    # 创建一个csv文件
    df.to_csv(filepath, index=False, header=False, mode='a')


# 1.1 职位链接csv文件
job_link_csv = 'job_link.csv'
# 1.2 职位信息csv文件
job_info_csv = 'job_info.csv'

# 1.3 取得日期截
basename = time.strftime("%Y%m%d", time.localtime())
# 1.4 csv文件添加日期和时间
job_link_csv = job_link_csv[:-4] + '_' + basename + '.csv'
job_info_csv = job_info_csv[:-4] + '_' + basename + '.csv'

i = 0
# 职位信息列表
job_info_list = []
# 3.读取csv文件取得职位信息链接
with open(job_link_csv) as f:
    reader = csv.reader(f)
    for row in reader:
        # 获取职位详情链接
        job_link = row[0]
        # 获取HTML
        html = get_html_text(job_link)[0]
        # 获取职位信息
        job_info = get_job_info(html)
        # 添加职位信息到列表
        job_info_list.append(job_info)

        i += 1
        print('获取第%d条职位信息：' % i, job_info)
        print('职位信息链接：', row)
        # 每隔10秒换一个链接
        # time.sleep(random.randint(1, 10))
        if i % 10 == 0:
            # 保存职位信息到csv文件
            save_csv(job_info_csv, job_info_list)