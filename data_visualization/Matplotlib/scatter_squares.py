import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path

sns.set_style('whitegrid')
# path对象
# path = Path('B:\\Coding\\Python\\Projects\\data_visualization\\1.png')

# 几个点
# x_values = [1, 2, 3, 4, 5]
# y_values = [1, 4, 9, 16, 25]

x_values = range(1, 1001)
y_values = [x ** 2 for x in x_values]

fig, ax = plt.subplots()
# 绘制单个点
# ax.scatter(2, 4, s=200)
# 绘制多个点
# ax.scatter(x_values, y_values, color='red', s=10)
# ax.scatter(x_values, y_values, color=(0,0.8,0) , s=10)
ax.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, s=10)

# 设置样式
ax.set_title("Square Numbers", fontsize = 24)
ax.set_xlabel("Value", fontsize = 14)
ax.set_ylabel("Square of value", fontsize = 14)
ax.tick_params(labelsize = 14)
ax.axis([0, 1100, 0, 1_100_000])
ax.ticklabel_format(style='plain')

# 获取当前脚本所在的目录
script_directory = os.path.dirname(os.path.abspath(__file__))
# 构建保存图片的绝对路径
image_path = os.path.join(script_directory, 'suqare_plot.png')
# print(image_path)
# plt.show()
# image_path = path
plt.savefig(image_path, bbox_inches='tight')