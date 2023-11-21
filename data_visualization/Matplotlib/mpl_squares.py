import matplotlib.pyplot as plt
import seaborn as sns


input_value = [1, 2, 3, 4, 5]
squares = [1, 4, 9, 16, 25]
# 此方法已经弃用
# plt.style.use('seaborn')

sns.set_style('whitegrid')

fig, ax = plt.subplots()
# print(fig, ax)
ax.plot(input_value, squares, linewidth = 3)
# ax.plot(squares, linewidth = 3)


# 设置图题，并给坐标轴加上标签
ax.set_title("Square Numbers", fontsize = 24)
ax.set_xlabel("Value", fontsize = 14)
ax.set_ylabel("Square of value", fontsize = 14)
ax.tick_params(labelsize = 14)

plt.show()