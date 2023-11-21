from die import Die
import plotly.express as px

# 创建2个D6

die_1 = Die()
die_2 = Die()

# 投掷几次骰子将结果存在列表中

results = []
for roll_num in range(1000):
    result = die_1.roll() + die_2.roll()
    results.append(result)
    
# print(results)
frequencies = []
max_result = die_1.num_sides + die_2.num_sides
poss_results = range(2, max_result+1)

for value in poss_results:
    frequency = results.count(value)
    frequencies.append(frequency)
    
# print(frequencies)
# 可视化
# 对结果进行可视化
title = "Results of Rolling Two D6 Dice 1,000 Times"
labels = {'x': 'Result', 'y': 'Frequency of Result'}
fig = px.bar(x=poss_results, y=frequencies, title=title, labels=labels)
fig.update_layout(xaxis_dtick=1)
fig.show()