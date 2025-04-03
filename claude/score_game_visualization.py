import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'SimSun', 'Arial Unicode MS']  # 优先使用的中文字体列表
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置参数（可以修改）
initial_score_diff_requirement = 15000  # 初始分差需求
decay_rate_per_hour = 0.01  # 每小时衰减率（占初始总数的百分比）
hourly_score = 1000  # 每小时得分
simulation_hours = 123  # 模拟总时间（小时）

# 创建时间数组
time = np.arange(0, simulation_hours + 1)

# 计算分差需求随时间的衰减
def calculate_requirement(t):
    # 24小时后开始衰减
    if t <= 24:
        return initial_score_diff_requirement
    else:
        hours_after_24 = t - 24
        return initial_score_diff_requirement *(1-hours_after_24*decay_rate_per_hour)

# 计算得分情况
def calculate_score_diff(t):
    score_diff = 0
    for i in range(int(t)):
        # 前6小时，A阵营得分
        if i < 6:
            score_diff += hourly_score
        # 接下来6小时，B阵营得分
        elif (i-6) % 24 < 12:
            score_diff -= hourly_score
        # 接下来6小时，A阵营得分
        elif (i-6) % 24 >= 12:
            score_diff += hourly_score
        else:
            score_diff -= hourly_score
    return score_diff

# 计算每个时间点的分差需求和实际分差
requirement_positive = np.array([calculate_requirement(t) for t in time])
requirement_negative = -requirement_positive

# 计算分差，但如果进入获胜区域则停止
score_diff = []
victory_time = None
for t in time:
    current_score = calculate_score_diff(t)
    score_diff.append(current_score)
    
    # 检查是否进入获胜区域
    current_req_positive = calculate_requirement(t)
    current_req_negative = -current_req_positive
    
    if current_score >= current_req_positive or current_score <= current_req_negative:
        victory_time = t
        break

# 如果找到了获胜时间，就截断数组
if victory_time is not None:
    victory_index = int(victory_time)
    time = time[:victory_index+1]
    requirement_positive = requirement_positive[:victory_index+1]
    requirement_negative = requirement_negative[:victory_index+1]
    score_diff = np.array(score_diff)  # 只包含到获胜时间的分数

# 创建图表
plt.figure(figsize=(12, 8))

# 绘制分差需求曲线
plt.plot(time, requirement_positive, 'r--', label='分差需求 (A帮获胜)')
plt.plot(time, requirement_negative, 'b--', label='分差需求 (B帮获胜)')

# 绘制实际分差曲线
plt.plot(time, score_diff, 'g-', label='实际分差')

# 填充获胜区域
plt.fill_between(time, requirement_positive, initial_score_diff_requirement+1000, alpha=0.2, color='red')
plt.fill_between(time, requirement_negative, -initial_score_diff_requirement-1000, alpha=0.2, color='blue')

# 如果有获胜，标记获胜点
if victory_time is not None:
    victory_score = score_diff[-1]
    if victory_score >= requirement_positive[-1]:
        plt.scatter([victory_time], [victory_score], color='red', s=100, zorder=5)
        plt.annotate('A帮获胜!', 
                     xy=(victory_time, victory_score),
                     xytext=(victory_time-10, victory_score+1000),
                     arrowprops=dict(facecolor='red', shrink=0.05))
    else:
        plt.scatter([victory_time], [victory_score], color='blue', s=100, zorder=5)
        plt.annotate('B帮获胜!', 
                     xy=(victory_time, victory_score),
                     xytext=(victory_time-10, victory_score-1000),
                     arrowprops=dict(facecolor='blue', shrink=0.05))

# 添加水平零线
plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)

# 添加标签和图例
plt.xlabel('时间（小时）')
plt.ylabel('分差')
plt.title('RW模拟')
plt.legend()
plt.grid(True, alpha=0.3)

# 设置x轴范围到获胜接触点
if victory_time is not None:
    plt.xlim(0, victory_time * 1.05)  # 留一点额外空间以便标注
else:
    plt.xlim(0, simulation_hours)

# 设置y轴范围，使图表更加合理
plt_min_y = min(np.min(score_diff), np.min(requirement_negative)) * 1.1
plt_max_y = max(np.max(score_diff), np.max(requirement_positive)) * 1.1
plt.ylim(plt_min_y, plt_max_y)

# 显示图表
plt.tight_layout()
plt.savefig('score_game_visualization.png')
plt.show() 