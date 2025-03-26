#我的环境是Windows，请你使用 Python编写一个gui界面，其中运行动态 ASCII 艺术程序，要求是这个ASCII艺术程序是你能想象到的最丑陋，最难看，最无聊的画面
import tkinter as tk
import random
import time
from itertools import cycle

class UglyAsciiArt:
    def __init__(self, root):
        self.root = root
        self.root.title("世界上最丑陋的ASCII艺术")
        
        # 设置窗口大小和背景色
        self.root.geometry("800x600")
        self.root.configure(bg="black")
        
        # 创建ASCII显示区域
        self.ascii_label = tk.Label(
            self.root, 
            text="", 
            font=("Courier", 8), 
            fg="lime", 
            bg="black",
            justify=tk.LEFT
        )
        self.ascii_label.pack(expand=True, fill=tk.BOTH)
        
        # 丑陋的颜色循环
        self.colors = cycle([
            "red", "green", "blue", "yellow", "magenta", "cyan",
            "pink", "orange", "purple", "brown", "lime", "teal"
        ])
        
        # 丑陋的图案
        self.patterns = [
            self.generate_random_pattern,
            self.generate_ugly_face,
            self.generate_boring_lines,
            self.generate_pointless_animation,
            self.generate_meaningless_noise
        ]
        
        # 开始动画
        self.update_ascii_art()
    
    def generate_random_pattern(self, step):
        """生成随机字符的无意义图案"""
        rows = []
        for i in range(30):
            row = "".join(random.choice("@#$%&*+=-~^;:,.") for _ in range(80))
            rows.append(row)
        return "\n".join(rows)
    
    def generate_ugly_face(self, step):
        """生成一个丑陋的脸"""
        face = [
            "  .-~~~-.__  .-~~~-.__  .-~~~-.__  ",
            " /         ~~~         ~~~         \ ",
            "|   O    O    O    O    O    O    O |",
            " \      .-~~~-.      .-~~~-.      / ",
            "  ~-.__/       \____/       \__.-~  ",
            "      \       /    \       /       ",
            "       ~-.___/      \___.-~         ",
            "              ~~~~~~                "
        ]
        
        # 随机扭曲脸部
        if step % 3 == 0:
            face[2] = face[2].replace("O", random.choice(["@", "#", "$", "%"]))
        if step % 4 == 0:
            face.insert(4, " " * random.randint(10, 30) + "BURP!" + " " * random.randint(10, 30))
        
        return "\n".join(face * 3)
    
    def generate_boring_lines(self, step):
        """生成无聊的线条图案"""
        lines = []
        for i in range(30):
            char = random.choice(["-", "=", "_", "~"])
            length = random.randint(40, 80)
            lines.append(char * length)
        return "\n".join(lines)
    
    def generate_pointless_animation(self, step):
        """毫无意义的动画"""
        anim = []
        size = 30
        for y in range(size):
            row = []
            for x in range(80):
                val = (x * y + step) % 256
                if val < 50:
                    row.append(".")
                elif val < 100:
                    row.append(",")
                elif val < 150:
                    row.append(":")
                elif val < 200:
                    row.append(";")
                else:
                    row.append("#")
            anim.append("".join(row))
        return "\n".join(anim)
    
    def generate_meaningless_noise(self, step):
        """纯粹的视觉噪声"""
        noise = []
        for _ in range(30):
            row = "".join(chr(random.randint(33, 126)) for _ in range(80))
            noise.append(row)
        return "\n".join(noise)
    
    def update_ascii_art(self):
        """更新ASCII艺术"""
        step = int(time.time() * 2)  # 用于动画的时间步长
        
        # 随机选择图案
        pattern_func = random.choice(self.patterns)
        ascii_art = pattern_func(step)
        
        # 随机改变颜色
        if step % 5 == 0:
            fg_color = next(self.colors)
            bg_color = next(self.colors)
            self.ascii_label.config(fg=fg_color, bg=bg_color)
        
        # 随机改变字体大小
        if step % 7 == 0:
            font_size = random.randint(6, 12)
            self.ascii_label.config(font=("Courier", font_size))
        
        # 更新文本
        self.ascii_label.config(text=ascii_art)
        
        # 随机安排下一次更新
        delay = random.randint(50, 300)
        self.root.after(delay, self.update_ascii_art)

if __name__ == "__main__":
    root = tk.Tk()
    app = UglyAsciiArt(root)
    root.mainloop()