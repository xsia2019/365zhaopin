import pandas as pd


df = pd.read_csv('job_info.csv', )

# 输入重复的前10个职位
print(df.iloc[:, 0].value_counts().head(10))
