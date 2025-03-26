#我的环境是Windows，请你使用 Python编写一个gui界面，其中运行动态 ASCII 艺术程序，要求是这个ASCII艺术程序是你能想象到的最丑陋，最难看，最无聊的画面
import tkinter as tk
import random
import time

# --- 常量设置 ---
WIDTH = 80  # ASCII 画面的宽度（字符数）
HEIGHT = 25 # ASCII 画面的高度（字符数）
UPDATE_DELAY = 150 # 更新之间的延迟（毫秒），控制变化速度
CHARS_TO_CHANGE_PER_FRAME = 15 # 每帧改变多少个字符，控制“动态”程度

# 定义一个包含丑陋、不和谐或无聊字符的列表
# 大量使用低对比度的标点符号和空格，偶尔加入一些刺眼的符号
# 权重偏向无聊字符，使得整体观感更加单调
UGLY_CHARS = list(".,'`    .,'`    .,'`    #@*?$%^&!~") 

# --- 全局状态 ---
# 使用列表的列表来存储字符网格
char_grid = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]

# --- 功能函数 ---
def initialize_grid():
    """用随机的'丑陋'字符填充初始网格。"""
    for r in range(HEIGHT):
        for c in range(WIDTH):
            char_grid[r][c] = random.choice(UGLY_CHARS)

def update_art():
    """随机更新网格中的一些字符，并刷新显示。"""
    global char_grid

    # 随机改变少量字符
    for _ in range(CHARS_TO_CHANGE_PER_FRAME):
        try:
            # 随机选择一个位置
            r = random.randint(0, HEIGHT - 1)
            c = random.randint(0, WIDTH - 1)
            # 用一个新的随机丑陋字符替换该位置的字符
            char_grid[r][c] = random.choice(UGLY_CHARS)
        except IndexError:
            # 在极少数情况下，如果 HEIGHT 或 WIDTH 为 0，则跳过
            pass

    # 将字符网格转换为用于显示的单字符串（每行用换行符分隔）
    display_string = "\n".join("".join(row) for row in char_grid)

    # 更新 Label 部件的文本内容
    try:
        ascii_label.config(text=display_string)
    except tk.TclError:
        # 如果窗口在更新时被关闭，会引发 TclError，这里简单捕获并退出
        print("窗口已关闭，停止更新。")
        return 

    # 安排下一次更新
    # 使用 root.after 来重复调用自身，避免阻塞 GUI 主循环
    root.after(UPDATE_DELAY, update_art)

# --- GUI 设置 ---
# 创建主窗口
root = tk.Tk()
root.title("最丑陋无聊的ASCII艺术 (Ugliest Boring ASCII Art)")
# 设置一个稍微不那么刺眼的背景色，让前景的“丑陋”更突出
# root.configure(bg='lightgrey') 

# 创建一个 Label 部件来显示 ASCII 艺术
# 使用等宽字体（如 Courier New）确保字符正确对齐
# justify=tk.LEFT 确保多行文本左对齐
# anchor='nw' 使文本在 Label 内从左上角开始显示
ascii_label = tk.Label(
    root, 
    font=("Courier New", 10),  # 选择等宽字体和适中大小
    justify=tk.LEFT,           # 左对齐
    anchor='nw',               # 内容锚定在西北（左上）角
    # 可以取消注释下一行来改变文本和背景色，以增加“丑陋感”
    # fg='darkgreen', bg='beige' 
)
# 将 Label 添加到窗口中，并留出一些边距
ascii_label.pack(padx=10, pady=10)

# --- 初始化并运行主循环 ---
print("正在初始化丑陋无聊的 ASCII 艺术...")
initialize_grid()  # 创建初始的混乱画面
print("开始动态更新...")
update_art()       # 启动更新循环
root.mainloop()    # 运行 Tkinter 事件循环，显示窗口并响应事件