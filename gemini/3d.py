# -*- coding: utf-8 -*-
"""
功能描述：
本脚本使用 Pygame 和 PyOpenGL 库在 Windows 环境下创建一个 3D 渲染窗口。
它旨在展示一个动态、炫酷且视觉上引人入胜的 3D 场景，
包含一个旋转的几何体（立方体）和一个围绕它流动的复杂粒子系统。
粒子具有变化的颜色和生命周期，并通过混合模式产生发光效果，
试图营造一种宇宙能量或星云般的震撼视觉体验。
相机围绕场景中心缓慢旋转，以增强 3D 感和动态性。
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
import time # 使用 time 模块获取时间用于动画

# --- 配置参数 ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PARTICLE_COUNT = 3000  # 粒子数量
PARTICLE_LIFE_MAX = 2.0  # 粒子最大生命周期（秒）
PARTICLE_SPEED = 0.8    # 粒子基础速度
ROTATION_SPEED_CUBE = 30 # 中心立方体旋转速度 (度/秒)
ROTATION_SPEED_CAMERA = 10 # 相机旋转速度 (度/秒)

# --- 粒子类 ---
class Particle:
    def __init__(self):
        self.reset()

    def reset(self):
        """重置粒子状态"""
        self.x, self.y, self.z = 0.0, 0.0, 0.0 # 从中心产生
        # 随机初始速度方向 (球状散开)
        theta = random.uniform(0, 2 * math.pi)
        phi = math.acos(random.uniform(-1, 1))
        speed_multiplier = random.uniform(0.5, 1.5)
        self.vx = PARTICLE_SPEED * speed_multiplier * math.sin(phi) * math.cos(theta)
        self.vy = PARTICLE_SPEED * speed_multiplier * math.sin(phi) * math.sin(theta)
        self.vz = PARTICLE_SPEED * speed_multiplier * math.cos(phi)

        # 随机生命周期和颜色
        self.life = random.uniform(PARTICLE_LIFE_MAX * 0.1, PARTICLE_LIFE_MAX)
        self.initial_life = self.life

        # 颜色 (例如：从蓝到紫/红的变化)
        self.r = random.uniform(0.2, 0.6) # 偏冷色调
        self.g = random.uniform(0.1, 0.4)
        self.b = random.uniform(0.7, 1.0)
        self.a = 1.0 # 初始 Alpha

    def update(self, dt):
        """更新粒子状态"""
        self.life -= dt
        if self.life <= 0:
            self.reset() # 生命结束则重置

        # 更新位置
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.z += self.vz * dt

        # 更新 Alpha (淡出效果)
        self.a = max(0.0, self.life / self.initial_life)

    def draw(self):
        """绘制粒子"""
        # 颜色随时间变化（可选，可以增加更多变化）
        # life_ratio = self.life / self.initial_life
        # r = self.r * life_ratio + (1-life_ratio) * 0.8 # 临近消失时变红
        # g = self.g * life_ratio
        # b = self.b * life_ratio

        # 使用生命周期调整 Alpha 来实现淡出
        glColor4f(self.r, self.g, self.b, self.a)
        glVertex3f(self.x, self.y, self.z)

# --- 绘制立方体函数 ---
def draw_cube():
    """绘制一个彩色的旋转立方体"""
    vertices = (
        ( 1, -1, -1), ( 1,  1, -1), (-1,  1, -1), (-1, -1, -1),
        ( 1, -1,  1), ( 1,  1,  1), (-1, -1,  1), (-1,  1,  1)
    )
    edges = (
        (0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 7), (7, 6),
        (6, 4), (0, 4), (1, 5), (2, 7), (3, 6)
    )
    surfaces = (
        (0, 1, 2, 3), (3, 2, 7, 6), (6, 7, 5, 4),
        (4, 5, 1, 0), (1, 5, 7, 2), (4, 0, 3, 6)
    )
    colors = (
        (1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 1, 0),
        (1, 0, 1), (0, 1, 1), (0.5, 0.5, 0.5), (1, 0.5, 0)
    )

    # 使用面绘制 (带基础光照)
    glBegin(GL_QUADS)
    for i, surface in enumerate(surfaces):
        # 为每个面设置一种颜色（或者可以为每个顶点设置颜色以获得平滑过渡）
        glColor3fv(colors[i % len(colors)])
        # 计算法线 (简单方式：取前三个顶点计算叉积) - 对光照很重要
        v1 = [vertices[surface[1]][j] - vertices[surface[0]][j] for j in range(3)]
        v2 = [vertices[surface[2]][j] - vertices[surface[0]][j] for j in range(3)]
        normal = [v1[1]*v2[2] - v1[2]*v2[1], v1[2]*v2[0] - v1[0]*v2[2], v1[0]*v2[1] - v1[1]*v2[0]]
        # 标准化法线向量
        norm = math.sqrt(sum(n*n for n in normal))
        if norm > 0:
            normal = [n / norm for n in normal]
        glNormal3fv(normal)

        for vertex_index in surface:
            glVertex3fv(vertices[vertex_index])
    glEnd()

    # 绘制边框（可选，增加清晰度）
    # glColor3f(0.8, 0.8, 0.8) # 边框颜色
    # glBegin(GL_LINES)
    # for edge in edges:
    #     for vertex_index in edge:
    #         glVertex3fv(vertices[vertex_index])
    # glEnd()


# --- 初始化函数 ---
def init_gl(width, height):
    """初始化 OpenGL 设置"""
    glEnable(GL_DEPTH_TEST) # 启用深度测试，确保物体前后关系正确
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (width / height), 0.1, 100.0) # 设置透视投影
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0) # 设置初始相机位置和朝向

    # 启用光照 (使立方体看起来更立体)
    glEnable(GL_LIGHTING)       # 启用光照总开关
    glEnable(GL_LIGHT0)         # 启用 0 号光源
    glEnable(GL_COLOR_MATERIAL) # 允许使用 glColor 来指定材质颜色
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE) # 颜色作用于环境光和漫反射

    # 设置光源属性
    light_ambient = [0.3, 0.3, 0.3, 1.0]  # 环境光
    light_diffuse = [0.8, 0.8, 0.8, 1.0]  # 漫反射光
    light_specular = [1.0, 1.0, 1.0, 1.0] # 镜面反射光
    light_position = [5.0, 5.0, 15.0, 1.0] # 光源位置 (w=1表示点光源)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    # 启用混合，用于粒子效果 (实现发光感)
    glEnable(GL_BLEND)
    # 设置混合函数：源颜色 * 源Alpha + 目标颜色 * (1 - 源Alpha)
    # 对于发光效果，通常使用 GL_ONE 作为目标因子 (Additive Blending)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE)
    # 或者使用标准的 Alpha 混合: glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # 设置点的大小
    glPointSize(2.5)

# --- 主函数 ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("炫酷 3D 粒子效果 - PyOpenGL Demo")

    init_gl(SCREEN_WIDTH, SCREEN_HEIGHT)

    # 创建粒子列表
    particles = [Particle() for _ in range(PARTICLE_COUNT)]

    clock = pygame.time.Clock()
    running = True
    last_time = time.time()
    total_time = 0 # 用于控制旋转

    while running:
        # --- 事件处理 ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # --- 计算时间差 ---
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time
        total_time += dt

        # --- 更新状态 ---
        for p in particles:
            p.update(dt)

        # --- 渲染 ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # 清除颜色和深度缓冲区
        glLoadIdentity() # 重置模型视图矩阵

        # 设置相机旋转
        camera_angle = total_time * ROTATION_SPEED_CAMERA
        cam_x = 10 * math.sin(math.radians(camera_angle))
        cam_z = 10 * math.cos(math.radians(camera_angle))
        gluLookAt(cam_x, 2, cam_z, 0, 0, 0, 0, 1, 0) # 相机围绕 Y 轴旋转，并稍微抬高

        # 绘制中心旋转立方体
        glPushMatrix() # 保存当前矩阵状态
        cube_angle_y = total_time * ROTATION_SPEED_CUBE
        cube_angle_x = total_time * ROTATION_SPEED_CUBE * 0.7 # 也可以绕多个轴旋转
        glRotatef(cube_angle_y, 0, 1, 0) # 绕 Y 轴旋转
        glRotatef(cube_angle_x, 1, 0, 0) # 绕 X 轴旋转
        glScalef(0.5, 0.5, 0.5) # 缩小立方体
        glEnable(GL_LIGHTING) # 绘制立方体时光照有效
        glDisable(GL_BLEND)   # 绘制实心物体时通常禁用混合或使用标准混合
        draw_cube()
        glPopMatrix() # 恢复之前的矩阵状态

        # 绘制粒子
        glEnable(GL_BLEND)           # 为粒子启用混合
        glBlendFunc(GL_SRC_ALPHA, GL_ONE) # 使用 Additive Blending 产生发光效果
        glDisable(GL_LIGHTING)       # 粒子通常不受光照影响（除非使用特殊着色器）
        glDepthMask(GL_FALSE)        # 绘制半透明物体时，禁止写入深度缓冲区，避免遮挡问题
        glBegin(GL_POINTS)
        for p in particles:
            p.draw()
        glEnd()
        glDepthMask(GL_TRUE)         # 恢复深度缓冲区写入

        # --- 更新屏幕 ---
        pygame.display.flip() # 交换缓冲区显示画面
        # pygame.time.wait(10) # 可以稍微降低CPU占用率，但会影响帧率平滑度
        clock.tick(60) # 限制帧率不超过 60 FPS

    pygame.quit()

# --- 程序入口 ---
if __name__ == '__main__':
    main()