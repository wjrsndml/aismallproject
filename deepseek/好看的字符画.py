#我的环境是Windows，请你使用 Python编写一个gui界面，其中运行动态 ASCII 艺术程序，要求是这个ASCII艺术程序是你能想象到的最炫酷，最漂亮，最震撼的画面



import tkinter as tk
import random
import math
import time
from itertools import cycle



class AsciiArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("炫酷动态ASCII艺术")
        self.root.geometry("1000x600")
        
        # 设置黑色背景
        self.root.configure(bg='black')
        
        # 创建文本显示区域
        self.canvas = tk.Text(root, bg='black', fg='white', font=('Courier New', 8), 
                             insertbackground='white', borderwidth=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 初始化艺术参数
        self.width = 120
        self.height = 30
        self.stars = []
        self.galaxy_angle = 0
        self.ship_pos = [self.width//2, self.height//2]
        self.ship_direction = 0
        self.ship_speed = 0.5
        self.particles = []
        self.colors = cycle(['#FF0000', '#FF7F00', '#FFFF00', '#00FF00', 
                            '#0000FF', '#4B0082', '#8B00FF', '#FFFFFF'])
        
        # 初始化星星
        self.initialize_stars(200)
        
        # 开始动画循环
        self.animate()
        
        # 绑定键盘事件
        self.root.bind('<Left>', lambda e: self.change_ship_direction(-15))
        self.root.bind('<Right>', lambda e: self.change_ship_direction(15))
        self.root.bind('<Up>', lambda e: self.change_ship_speed(0.1))
        self.root.bind('<Down>', lambda e: self.change_ship_speed(-0.1))
        
    def initialize_stars(self, count):
        for _ in range(count):
            star = {
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'speed': random.uniform(0.02, 0.2),
                'brightness': random.uniform(0.3, 1.0),
                'phase': random.uniform(0, 2*math.pi)
            }
            self.stars.append(star)
    
    def change_ship_direction(self, delta):
        self.ship_direction += delta
    
    def change_ship_speed(self, delta):
        self.ship_speed += delta
        self.ship_speed = max(0, min(2, self.ship_speed))
    
    def add_particle(self, x, y, dx, dy, life):
        self.particles.append({
            'x': x,
            'y': y,
            'dx': dx,
            'dy': dy,
            'life': life,
            'max_life': life,
            'char': random.choice(['*', '+', '.', '·', '°'])
        })
    
    def update_particles(self):
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
    
    def animate(self):
        start_time = time.time()
        
        # 清空画布
        self.canvas.delete('1.0', tk.END)
        
        # 创建空白帧
        frame = [[' ' for _ in range(self.width)] for _ in range(self.height)]
        
        # 更新星星
        for star in self.stars:
            star['x'] -= star['speed']
            if star['x'] < 0:
                star['x'] = self.width
                star['y'] = random.randint(0, self.height)
            
            # 星星闪烁效果
            brightness = star['brightness'] * (0.7 + 0.3 * math.sin(time.time() * 3 + star['phase']))
            x, y = int(star['x']), int(star['y'])
            if 0 <= x < self.width and 0 <= y < self.height:
                if brightness > 0.8:
                    frame[y][x] = '●'
                elif brightness > 0.6:
                    frame[y][x] = '○'
                elif brightness > 0.3:
                    frame[y][x] = '·'
                else:
                    frame[y][x] = ' '
        
        # 绘制旋转星系
        self.galaxy_angle += 0.02
        galaxy_center_x = self.width * 0.3
        galaxy_center_y = self.height * 0.5
        for i in range(100):
            angle = self.galaxy_angle + i * 0.2
            radius = 5 + i * 0.15
            x = int(galaxy_center_x + radius * math.cos(angle))
            y = int(galaxy_center_y + radius * math.sin(angle) * 0.4)
            if 0 <= x < self.width and 0 <= y < self.height:
                frame[y][x] = '#'
        
        # 更新飞船位置
        self.ship_direction %= 360
        rad = math.radians(self.ship_direction)
        self.ship_pos[0] += math.cos(rad) * self.ship_speed
        self.ship_pos[1] -= math.sin(rad) * self.ship_speed
        
        # 边界检查
        self.ship_pos[0] = max(0, min(self.width-1, self.ship_pos[0]))
        self.ship_pos[1] = max(0, min(self.height-1, self.ship_pos[1]))
        
        # 添加尾迹粒子
        if random.random() < 0.7 and self.ship_speed > 0:
            self.add_particle(
                self.ship_pos[0] - math.cos(rad) * 2,
                self.ship_pos[1] + math.sin(rad) * 2,
                -math.cos(rad) * 0.2 + random.uniform(-0.1, 0.1),
                math.sin(rad) * 0.2 + random.uniform(-0.1, 0.1),
                random.randint(10, 20)
            )
        
        # 更新粒子
        self.update_particles()
        
        # 绘制粒子
        for particle in self.particles:
            x, y = int(particle['x']), int(particle['y'])
            if 0 <= x < self.width and 0 <= y < self.height:
                alpha = particle['life'] / particle['max_life']
                if alpha > 0.7:
                    frame[y][x] = particle['char']
                elif alpha > 0.4:
                    frame[y][x] = '·'
                elif alpha > 0.1:
                    frame[y][x] = ' '
        
        # 绘制飞船
        ship_x, ship_y = int(self.ship_pos[0]), int(self.ship_pos[1])
        if 0 <= ship_x < self.width and 0 <= ship_y < self.height:
            # 简单的飞船图形，方向敏感
            frame[ship_y][ship_x] = '▲'
            if 0 <= ship_x-1 < self.width:
                frame[ship_y][ship_x-1] = '<'
            if 0 <= ship_x+1 < self.width:
                frame[ship_y][ship_x+1] = '>'
        
        # 绘制行星
        planet_x = int(self.width * 0.7)
        planet_y = int(self.height * 0.5)
        planet_radius = 8
        for dy in range(-planet_radius, planet_radius+1):
            for dx in range(-planet_radius, planet_radius+1):
                if dx*dx + dy*dy <= planet_radius*planet_radius:
                    x = planet_x + dx
                    y = planet_y + dy
                    if 0 <= x < self.width and 0 <= y < self.height:
                        # 简单的行星纹理
                        if abs(dx) == planet_radius or abs(dy) == planet_radius:
                            frame[y][x] = 'O'
                        elif dx*dx + dy*dy > (planet_radius-2)*(planet_radius-2):
                            frame[y][x] = random.choice(['=', '~'])
                        else:
                            frame[y][x] = random.choice(['+', '.'])
        
        # 将帧转换为文本
        frame_text = '\n'.join([''.join(row) for row in frame])
        
        # 应用颜色
        next_color = next(self.colors)
        self.canvas.tag_configure("color", foreground=next_color)
        self.canvas.insert(tk.END, frame_text)
        
        # 为特定元素着色
        for y in range(self.height):
            for x in range(self.width):
                char = frame[y][x]
                if char in ['●', '○', '·']:  # 星星
                    self.canvas.tag_add("color", f"{y+1}.{x}", f"{y+1}.{x+1}")
        
        # 计算FPS
        elapsed = time.time() - start_time
        fps = 1 / elapsed if elapsed > 0 else 0
        self.root.title(f"炫酷动态ASCII艺术 - FPS: {fps:.1f}")
        
        # 安排下一次更新
        self.root.after(50, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = AsciiArtApp(root)
    root.mainloop()