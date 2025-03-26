#我的环境是Windows，请你使用 Python编写一个gui界面，其中运行动态 ASCII 艺术程序，要求是这个ASCII艺术程序是你能想象到的最炫酷，最漂亮，最震撼的画面

import tkinter as tk
import math
import time
import random

# --- 配置参数 ---
WIDTH = 100         # ASCII 画布宽度 (字符数)
HEIGHT = 50        # ASCII 画布高度 (字符数)
# 不同的字符代表不同的“亮度”或“值”
# 你可以尝试不同的字符集来改变外观
CHAR_GRADIENT = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
# CHAR_GRADIENT = " .:░▒▓█" # 简单的块状渐变
FONT_NAME = "Consolas"  # 在Windows上常用的等宽字体, Courier New 也可以
FONT_SIZE = 10
UPDATE_DELAY_MS = 40  # 更新间隔 (毫秒)，越小越快 (约 25 FPS)
BACKGROUND_COLOR = "black" # 背景色
FOREGROUND_COLOR = "lime green" # 前景色 (ASCII字符颜色)

# --- ASCII 艺术生成函数 ---
def generate_ascii_frame(width, height, t):
    """
    生成一帧 ASCII 艺术。
    使用基于时间和坐标的正弦函数组合来创建类似等离子体的效果。
    """
    lines = []
    for j in range(height):
        line = ""
        y = j / height * 2.0 - 1.0  # 归一化坐标到 [-1, 1]
        for i in range(width):
            x = i / width * 2.0 - 1.0 # 归一化坐标到 [-1, 1]

            # 核心：计算像素值的函数，这里混合了多个随时间变化的模式
            # 1. 基于到中心距离的正弦波
            dist_center = math.sqrt(x*x + y*y)
            v1 = math.sin(dist_center * 10.0 - t * 2.0) # 频率和速度

            # 2. 基于 x, y 坐标和时间的独立正弦波
            v2 = math.sin(x * 5.0 + t * 1.5) # 横向波浪
            v3 = math.sin(y * 6.0 - t * 1.8) # 纵向波浪

            # 3. 对角线/旋转效果
            v4 = math.sin((x + y) * 7.0 + t * 2.2)

            # 组合这些值 (可以尝试不同的组合方式)
            final_value = (v1 + v2 + v3 + v4) / 4.0 # 平均值，范围在 [-1, 1]

            # 将 final_value [-1, 1] 映射到字符渐变的索引 [0, len(CHAR_GRADIENT)-1]
            gradient_index = int(((final_value + 1.0) / 2.0) * (len(CHAR_GRADIENT) - 1))
            # 确保索引在有效范围内
            gradient_index = max(0, min(gradient_index, len(CHAR_GRADIENT) - 1))

            line += CHAR_GRADIENT[gradient_index]
        lines.append(line)
    return "\n".join(lines)

# --- Tkinter 更新函数 ---
start_time = time.time()
def update_frame():
    """
    更新 Tkinter Label 中的 ASCII 艺术。
    """
    # 计算经过的时间，作为动画驱动
    current_t = time.time() - start_time

    # 生成新的 ASCII 帧
    ascii_frame = generate_ascii_frame(WIDTH, HEIGHT, current_t)

    # 更新 Label 的文本
    # 使用 try/except 避免在窗口关闭时更新 Label 出错
    try:
        ascii_label.config(text=ascii_frame)
    except tk.TclError:
        # 窗口可能已经关闭
        return

    # 安排下一次更新
    root.after(UPDATE_DELAY_MS, update_frame)

# --- GUI 设置 ---
root = tk.Tk()
root.title("炫酷动态 ASCII 艺术")
root.configure(bg=BACKGROUND_COLOR)

# 创建一个 Label 来显示 ASCII 艺术
# 使用等宽字体确保字符对齐
# 设置背景色和前景色
ascii_label = tk.Label(
    root,
    font=(FONT_NAME, FONT_SIZE),
    justify=tk.LEFT,       # 左对齐
    anchor="nw",           # 内容在 Label 内也靠左上角
    bg=BACKGROUND_COLOR,
    fg=FOREGROUND_COLOR
)
# 让 Label 填满整个窗口并随窗口缩放（尽管 ASCII 网格大小固定）
ascii_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# --- 启动动画 ---
print("正在启动 ASCII 动画...")
# 首次调用 update_frame 来启动循环
update_frame()

# --- 运行 Tkinter 主事件循环 ---
root.mainloop()

print("程序结束。")