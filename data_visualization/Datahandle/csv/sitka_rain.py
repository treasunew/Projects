from pathlib import Path
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import seaborn as sns

path = Path('Projects/data_visualization/Datahandle/data/death_valley_2021_full.csv')
lines = path.read_text().splitlines()

reader = csv.reader(lines)
header_row = next(reader)
# for index, colum_header in enumerate(header_row):
#     print(index, colum_header)

dates, rainfalls = [], []
for row in reader:
    date = datetime.strptime(row[2], '%Y-%m-%d')
    try:
        rainfall = row[3]
    except ValueError:
        print(f"rainfall missing value at {dates}")
    else:
        dates.append(date)
        rainfalls.append(rainfall)
# print(rainfalls)

sns.set_style('whitegrid')   
fig, ax = plt.subplots()
ax.plot(dates, rainfalls, color='green', alpha=0.5)

ax.set_title('Daily Rainfall, 2021\nDeath Valley, CA', fontsize=16)
ax.set_xlabel('', fontsize=16)
fig.autofmt_xdate()
ax.set_ylabel('Rainfall (ML)', fontsize=16)
ax.tick_params(labelsize=16)

plt.show()