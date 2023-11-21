from pathlib import Path
import csv
import matplotlib.pyplot as plt
import seaborn as sns 
from datetime import datetime

path_1 = Path('Projects/data_visualization/Datahandle/data/sitka_weather_2021_simple.csv')
path_2 = Path('Projects/data_visualization/Datahandle/data/death_valley_2021_simple.csv')

lines_1 = path_1.read_text().splitlines()
lines_2 = path_2.read_text().splitlines()

reader_1 = csv.reader(lines_1)
reader_2 = csv.reader(lines_2)
header_row_1 = next(reader_1)
header_row_2 = next(reader_2)

dates_1, highs_1, lows_1 = [], [], []
dates_2, highs_2, lows_2 = [], [], []

for row_1 in reader_1:
    date_1 = datetime.strptime(row_1[2], '%Y-%m-%d')
    try:
        high_1 = int(row_1[4])
        low_1 = int(row_1[5])
    except ValueError:
        print(f"missing value at {date_1}")
    else:
        dates_1.append(date_1)
        highs_1.append(high_1)
        lows_1.append(low_1)

for row_2 in reader_2:
    date_2 = datetime.strptime(row_2[2], '%Y-%m-%d')
    try:
        high_2 = int(row_2[3])
        low_2 = int(row_2[4])
    except ValueError:
        print(f"missing value at {date_2}")
    else:
        dates_2.append(date_2)
        highs_2.append(high_2)
        lows_2.append(low_2)
        
fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
ax1.plot(dates_1, lows_1, color='blue', alpha=0.5)
ax1.plot(dates_1, highs_1, color='red', alpha=0.5)
ax1.fill_between(dates_1, lows_1, highs_1, facecolor='green', alpha=0.1)

ax2.plot(dates_2, lows_2, color='blue', alpha=0.5)
ax2.plot(dates_2, highs_2, color='red', alpha=0.5)
ax2.fill_between(dates_2, lows_2, highs_2, facecolor='green', alpha=0.1)

ax1.set_title('Daily High and Low Temperatures, 2021\nSitka, AK', fontsize=15)
ax1.set_xlabel('', fontsize=13)
fig.autofmt_xdate()
ax1.set_ylabel('Temperature (F)', fontsize=13)
ax1.tick_params(labelsize=10)

ax2.set_title('Daily High and Low Temperatures, 2021\nDeath Valley, CA', fontsize=15)
ax2.set_xlabel('', fontsize=13)
fig.autofmt_xdate()
ax2.tick_params(labelsize=10)
plt.show()