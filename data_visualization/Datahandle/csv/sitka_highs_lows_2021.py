from pathlib import Path
import csv
import os
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# pwd = os.getcwd
# print(pwd)

path = Path('Projects/data_visualization/Datahandle/data/sitka_weather_2021_simple.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)
# for index, column_header in enumerate(header_row):
#     print(index, column_header)

# 提取最高温度
highs, dates, lows = [], [], []
for row in reader:
    current_date = datetime.strptime(row[2], '%Y-%m-%d')
    high = int(row[4])
    low = int(row[5])
    dates.append(current_date)
    highs.append(high)
    lows.append(low)
# print(highs)

# 根据最高温度绘图
sns.set_style('whitegrid')
fig, ax = plt.subplots()
ax.plot(dates, highs, color='red', alpha=0.5)
ax.plot(dates, lows, color='green', alpha=0.5)
ax.fill_between(dates, highs, lows, facecolor='blue', alpha=0.1)

# 格式
ax.set_title('Daily High and Low Temperatures, 2021', fontsize=24)
ax.set_xlabel('', fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel('Temperature (F)', fontsize=16)
ax.tick_params(labelsize=13)
plt.show()