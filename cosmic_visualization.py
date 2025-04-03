"""
宇宙场景渲染程序 - Cosmic Visualization
使用VPython (GlowScript)创建的交互式3D宇宙场景
包含恒星、行星、星云、黑洞等天体，并模拟基础物理效果
"""

import vpython as vp
import math
import random
import numpy as np
from vpython import vec

# 全局设置
SCALE_FACTOR = 1e9  # 比例因子，用于缩放真实天体距离
G = 6.67430e-11  # 万有引力常数
AU = 149.6e9  # 天文单位(m)
MAX_RENDER_DISTANCE = 50 * AU  # 最大渲染距离（50天文单位）
RUNNING = True  # 模拟运行状态

# 场景设置
scene = vp.canvas(title="宇宙场景渲染", width=1200, height=800, center=vp.vector(0, 0, 0))
scene.range = 5 * AU / SCALE_FACTOR
scene.forward = vp.vec(0, -1, -2)
scene.fov = math.pi/6
scene.background = vp.color.black

# 增加说明文本
instructions = vp.label(pos=vp.vec(0, 0, 0), 
                       text="控制：WASD移动，鼠标拖动调整视角，空格键暂停/继续",
                       xoffset=0, yoffset=-scene.height/2 + 30, 
                       color=vp.color.white,
                       height=15,
                       box=False)

# 创建星空背景
def create_starry_background(n_stars=2000, radius=100*AU/SCALE_FACTOR):
    """创建星空背景"""
    stars = []
    for i in range(n_stars):
        theta = random.uniform(0, math.pi)
        phi = random.uniform(0, 2 * math.pi)
        r = radius
        x = r * math.sin(theta) * math.cos(phi)
        y = r * math.sin(theta) * math.sin(phi)
        z = r * math.cos(theta)
        
        brightness = random.uniform(0.3, 1.0)
        color = vp.vec(brightness, brightness, brightness*random.uniform(0.8, 1.0))
        
        star = vp.sphere(pos=vp.vec(x, y, z), 
                        radius=random.uniform(0.01, 0.05)*AU/SCALE_FACTOR, 
                        color=color,
                        emissive=True)
        stars.append(star)
    return stars

# 创建星云
def create_nebula(pos, size, color):
    """创建星云"""
    nebula_points = []
    num_points = 1000
    
    for i in range(num_points):
        # 生成星云中的随机点
        theta = random.uniform(0, math.pi)
        phi = random.uniform(0, 2 * math.pi)
        r = random.uniform(0, size)
        
        x = pos.x + r * math.sin(theta) * math.cos(phi)
        y = pos.y + r * math.sin(theta) * math.sin(phi)
        z = pos.z + r * math.cos(theta)
        
        opacity = random.uniform(0.1, 0.9)
        point_color = vp.vec(color.x * opacity, color.y * opacity, color.z * opacity)
        
        point = vp.sphere(pos=vp.vec(x, y, z),
                         radius=size/30 * random.uniform(0.1, 0.3),
                         color=point_color,
                         opacity=opacity,
                         emissive=True)
        nebula_points.append(point)
    
    return nebula_points

# 创建小行星带
def create_asteroid_belt(center, inner_radius, outer_radius, num_asteroids=200):
    """创建小行星带"""
    asteroids = []
    
    for i in range(num_asteroids):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(inner_radius, outer_radius)
        
        x = center.x + distance * math.cos(angle)
        y = center.y + random.uniform(-0.1, 0.1) * inner_radius
        z = center.z + distance * math.sin(angle)
        
        size = random.uniform(0.01, 0.05) * AU / SCALE_FACTOR
        color_val = random.uniform(0.6, 0.9)
        
        asteroid = vp.sphere(pos=vp.vec(x, y, z),
                           radius=size,
                           color=vp.vec(color_val, color_val*0.9, color_val*0.7))
        
        asteroids.append({
            'obj': asteroid,
            'angle': angle,
            'distance': distance,
            'speed': math.sqrt(G * 1.989e30 / (distance * SCALE_FACTOR)) * 0.7,  # 轨道速度简化计算
            'y_offset': y - center.y
        })
    
    return asteroids

# 创建黑洞
def create_black_hole(pos, mass, radius):
    """创建黑洞"""
    # 黑洞核心
    black_hole = vp.sphere(pos=pos,
                         radius=radius,
                         color=vp.color.black,
                         emissive=False,
                         shininess=0)
    
    # 黑洞吸积盘
    accretion_disk = []
    disk_radius = radius * 5
    disk_thickness = radius * 0.5
    num_rings = 20
    
    for i in range(num_rings):
        r = radius * 2 + (disk_radius - radius * 2) * i / num_rings
        ring = vp.ring(pos=pos,
                     axis=vp.vec(0, 1, 0),
                     radius=r,
                     thickness=disk_thickness / num_rings,
                     color=vp.vec(1, 0.5 - i/num_rings/2, 0.1),
                     opacity=0.7 - i/num_rings*0.5,
                     emissive=True)
        accretion_disk.append({'ring': ring, 'speed': math.sqrt(G * mass / (r * SCALE_FACTOR)) * 0.01, 'angle': 0})
    
    # 黑洞附近的粒子
    particles = []
    num_particles = 50
    for i in range(num_particles):
        dist = random.uniform(radius * 5, radius * 15)
        angle = random.uniform(0, 2 * math.pi)
        height = random.uniform(-disk_thickness, disk_thickness)
        
        x = pos.x + dist * math.cos(angle)
        y = pos.y + height
        z = pos.z + dist * math.sin(angle)
        
        particle = vp.sphere(pos=vp.vec(x, y, z),
                           radius=radius * 0.05,
                           color=vp.vec(1, 0.3, 0.1),
                           emissive=True)
        
        particles.append({
            'particle': particle,
            'distance': dist,
            'angle': angle,
            'height': height,
            'speed': math.sqrt(G * mass / (dist * SCALE_FACTOR)) * 0.05
        })
    
    return {
        'core': black_hole,
        'accretion_disk': accretion_disk,
        'particles': particles,
        'mass': mass
    }

# 创建脉冲星
def create_pulsar(pos, radius):
    """创建脉冲星"""
    # 脉冲星核心
    pulsar_core = vp.sphere(pos=pos,
                          radius=radius,
                          color=vp.color.white,
                          emissive=True)
    
    # 脉冲星光束
    beam1 = vp.cone(pos=pos, 
                  axis=vp.vec(0, radius*10, 0),
                  radius=radius*2,
                  color=vp.color.cyan,
                  opacity=0.6,
                  emissive=True)
    
    beam2 = vp.cone(pos=pos,
                  axis=vp.vec(0, -radius*10, 0),
                  radius=radius*2,
                  color=vp.color.cyan,
                  opacity=0.6,
                  emissive=True)
    
    return {
        'core': pulsar_core,
        'beam1': beam1,
        'beam2': beam2,
        'angle': 0,
        'rotation_speed': 0.1,  # 旋转速度
        'pulse_timer': 0,
        'pulse_period': 30  # 脉冲周期（帧数）
    }

# 创建恒星
def create_star(pos, radius, color=vp.color.yellow):
    """创建恒星"""
    # 恒星核心
    star = vp.sphere(pos=pos,
                   radius=radius,
                   color=color,
                   emissive=True)
    
    # 恒星日冕
    corona_radius = radius * 1.5
    corona = vp.local_light(pos=pos,
                          color=color,
                          visible=True)
    
    # 恒星日冕粒子
    corona_particles = []
    num_particles = 100
    
    for i in range(num_particles):
        theta = random.uniform(0, math.pi)
        phi = random.uniform(0, 2 * math.pi)
        r = random.uniform(radius * 1.05, corona_radius)
        
        x = pos.x + r * math.sin(theta) * math.cos(phi)
        y = pos.y + r * math.sin(theta) * math.sin(phi)
        z = pos.z + r * math.cos(theta)
        
        particle = vp.sphere(pos=vp.vec(x, y, z),
                           radius=radius * 0.05,
                           color=color,
                           opacity=random.uniform(0.3, 0.7),
                           emissive=True)
        
        corona_particles.append({
            'particle': particle,
            'distance': r - radius,
            'theta': theta,
            'phi': phi,
            'speed_theta': random.uniform(-0.01, 0.01),
            'speed_phi': random.uniform(-0.01, 0.01),
            'lifetime': random.uniform(50, 200),
            'age': 0
        })
    
    return {
        'core': star,
        'corona': corona,
        'particles': corona_particles,
        'radius': radius
    }

# 创建行星
def create_planet(pos, radius, texture_type, orbit_radius, orbit_speed, parent_pos=vp.vec(0,0,0)):
    """创建行星"""
    if texture_type == "rocky":
        # 岩石行星
        color = vp.vec(random.uniform(0.5, 0.8), random.uniform(0.5, 0.7), random.uniform(0.3, 0.6))
    else:
        # 气态行星
        color = vp.vec(random.uniform(0.6, 0.9), random.uniform(0.6, 0.9), random.uniform(0.7, 1.0))
    
    planet = vp.sphere(pos=pos,
                     radius=radius,
                     color=color,
                     shininess=0.3)
    
    # 为气态行星添加条纹
    if texture_type == "gas":
        stripes = []
        num_stripes = random.randint(3, 7)
        
        for i in range(num_stripes):
            y_pos = pos.y - radius + 2 * radius * i / (num_stripes - 1)
            stripe_color = vp.vec(color.x * 0.8, color.y * 0.8, color.z * 0.8)
            
            stripe = vp.ring(pos=vp.vec(pos.x, y_pos, pos.z),
                           axis=vp.vec(0, 1, 0),
                           radius=radius * math.cos(math.asin((y_pos - pos.y) / radius)) if abs(y_pos - pos.y) < radius else 0,
                           thickness=radius / 10,
                           color=stripe_color)
            stripes.append(stripe)
    else:
        stripes = []
    
    # 添加行星轨道
    orbit = vp.ring(pos=parent_pos,
                  axis=vp.vec(0, 1, 0),
                  radius=orbit_radius,
                  thickness=radius / 20,
                  color=vp.color.white,
                  opacity=0.2)
    
    return {
        'planet': planet,
        'stripes': stripes,
        'orbit': orbit,
        'orbit_radius': orbit_radius,
        'orbit_angle': random.uniform(0, 2 * math.pi),
        'orbit_speed': orbit_speed,
        'parent_pos': parent_pos,
        'type': texture_type,
        'radius': radius
    }

# 创建行星系统
def create_solar_system():
    """创建一个包含恒星和行星的行星系统"""
    # 中央恒星
    star_radius = 0.5 * AU / SCALE_FACTOR
    sun = create_star(vp.vec(0, 0, 0), star_radius, vp.color.yellow)
    
    # 行星系统
    planets = []
    
    # 类地行星（岩石行星）
    for i in range(4):
        orbit_radius = (0.4 + i * 0.3) * AU / SCALE_FACTOR
        planet_radius = (0.03 + i * 0.01) * AU / SCALE_FACTOR
        
        # 轨道速度通过开普勒定律计算
        orbit_speed = math.sqrt(G * 1.989e30 / (orbit_radius * SCALE_FACTOR * 1.5))
        
        planet = create_planet(
            pos=vp.vec(orbit_radius, 0, 0),  # 初始位置
            radius=planet_radius,
            texture_type="rocky",
            orbit_radius=orbit_radius,
            orbit_speed=orbit_speed
        )
        planets.append(planet)
    
    # 小行星带
    asteroids = create_asteroid_belt(
        center=vp.vec(0, 0, 0),
        inner_radius=2.2 * AU / SCALE_FACTOR,
        outer_radius=3.2 * AU / SCALE_FACTOR
    )
    
    # 气态巨行星
    for i in range(4):
        orbit_radius = (5.0 + i * 4) * AU / SCALE_FACTOR
        planet_radius = (0.11 + i * 0.03) * AU / SCALE_FACTOR
        
        # 轨道速度通过开普勒定律计算
        orbit_speed = math.sqrt(G * 1.989e30 / (orbit_radius * SCALE_FACTOR * 2.0))
        
        planet = create_planet(
            pos=vp.vec(orbit_radius, 0, 0),  # 初始位置
            radius=planet_radius,
            texture_type="gas",
            orbit_radius=orbit_radius,
            orbit_speed=orbit_speed
        )
        planets.append(planet)
    
    return sun, planets, asteroids

# 创建深空天体
def create_deep_space_objects():
    """创建深空天体（星云、黑洞、脉冲星）"""
    objects = []
    
    # 创建星云
    nebula1 = create_nebula(
        pos=vp.vec(30 * AU / SCALE_FACTOR, 5 * AU / SCALE_FACTOR, -10 * AU / SCALE_FACTOR),
        size=5 * AU / SCALE_FACTOR,
        color=vp.vec(0.2, 0.5, 1.0)  # 蓝色星云
    )
    objects.append({"type": "nebula", "objects": nebula1})
    
    nebula2 = create_nebula(
        pos=vp.vec(-25 * AU / SCALE_FACTOR, -8 * AU / SCALE_FACTOR, 15 * AU / SCALE_FACTOR),
        size=8 * AU / SCALE_FACTOR,
        color=vp.vec(1.0, 0.2, 0.5)  # 红色星云
    )
    objects.append({"type": "nebula", "objects": nebula2})
    
    # 创建黑洞
    black_hole = create_black_hole(
        pos=vp.vec(-15 * AU / SCALE_FACTOR, 0, -20 * AU / SCALE_FACTOR),
        mass=8e30,  # 质量（与太阳质量相当）
        radius=0.8 * AU / SCALE_FACTOR
    )
    objects.append({"type": "black_hole", "object": black_hole})
    
    # 创建脉冲星
    pulsar = create_pulsar(
        pos=vp.vec(20 * AU / SCALE_FACTOR, 3 * AU / SCALE_FACTOR, 25 * AU / SCALE_FACTOR),
        radius=0.2 * AU / SCALE_FACTOR
    )
    objects.append({"type": "pulsar", "object": pulsar})
    
    return objects

# 更新恒星
def update_star(star):
    """更新恒星效果"""
    # 更新日冕粒子
    new_particles = []
    
    for p in star['particles']:
        p['age'] += 1
        
        # 移动粒子
        p['theta'] += p['speed_theta']
        p['phi'] += p['speed_phi']
        
        # 计算新位置
        r = star['radius'] + p['distance']
        x = star['core'].pos.x + r * math.sin(p['theta']) * math.cos(p['phi'])
        y = star['core'].pos.y + r * math.sin(p['theta']) * math.sin(p['phi'])
        z = star['core'].pos.z + r * math.cos(p['theta'])
        
        p['particle'].pos = vp.vec(x, y, z)
        
        # 如果粒子寿命未结束，保留它
        if p['age'] < p['lifetime']:
            new_particles.append(p)
        else:
            p['particle'].visible = False
            del p['particle']
    
    # 补充新粒子
    while len(new_particles) < 100:
        theta = random.uniform(0, math.pi)
        phi = random.uniform(0, 2 * math.pi)
        r = random.uniform(star['radius'] * 1.05, star['radius'] * 1.5)
        
        x = star['core'].pos.x + r * math.sin(theta) * math.cos(phi)
        y = star['core'].pos.y + r * math.sin(theta) * math.sin(phi)
        z = star['core'].pos.z + r * math.cos(theta)
        
        particle = vp.sphere(pos=vp.vec(x, y, z),
                           radius=star['radius'] * 0.05,
                           color=star['core'].color,
                           opacity=random.uniform(0.3, 0.7),
                           emissive=True)
        
        new_particles.append({
            'particle': particle,
            'distance': r - star['radius'],
            'theta': theta,
            'phi': phi,
            'speed_theta': random.uniform(-0.01, 0.01),
            'speed_phi': random.uniform(-0.01, 0.01),
            'lifetime': random.uniform(50, 200),
            'age': 0
        })
    
    star['particles'] = new_particles

# 更新行星位置
def update_planets(planets):
    """更新行星轨道位置"""
    for planet in planets:
        # 更新轨道角度
        planet['orbit_angle'] += planet['orbit_speed']
        
        # 计算新位置（椭圆轨道）
        x = planet['parent_pos'].x + planet['orbit_radius'] * math.cos(planet['orbit_angle'])
        z = planet['parent_pos'].z + planet['orbit_radius'] * math.sin(planet['orbit_angle'])
        
        # 更新行星位置
        planet['planet'].pos = vp.vec(x, planet['parent_pos'].y, z)
        
        # 更新条纹位置（如果是气态行星）
        if planet['type'] == "gas":
            for stripe in planet['stripes']:
                stripe_y_offset = stripe.pos.y - planet['planet'].pos.y
                stripe.pos = vp.vec(x, planet['planet'].pos.y + stripe_y_offset, z)

# 更新小行星带
def update_asteroids(asteroids):
    """更新小行星位置"""
    for asteroid in asteroids:
        # 更新角度
        asteroid['angle'] += asteroid['speed']
        
        # 计算新位置
        x = asteroid['distance'] * math.cos(asteroid['angle'])
        z = asteroid['distance'] * math.sin(asteroid['angle'])
        
        # 更新小行星位置
        asteroid['obj'].pos = vp.vec(x, asteroid['y_offset'], z)

# 更新黑洞
def update_black_hole(black_hole):
    """更新黑洞效果"""
    # 更新吸积盘
    for ring in black_hole['accretion_disk']:
        ring['angle'] += ring['speed']
        ring['ring'].rotate(angle=ring['speed'], axis=vp.vec(0, 1, 0), origin=black_hole['core'].pos)
    
    # 更新粒子
    for particle in black_hole['particles']:
        # 模拟粒子被吸入黑洞
        particle['angle'] += particle['speed']
        particle['distance'] -= particle['speed'] * 10  # 逐渐向黑洞移动
        
        # 计算新位置
        x = black_hole['core'].pos.x + particle['distance'] * math.cos(particle['angle'])
        y = black_hole['core'].pos.y + particle['height']
        z = black_hole['core'].pos.z + particle['distance'] * math.sin(particle['angle'])
        
        # 更新粒子位置
        particle['particle'].pos = vp.vec(x, y, z)
        
        # 如果粒子太接近黑洞，重置它
        if particle['distance'] < black_hole['core'].radius * 1.5:
            particle['distance'] = random.uniform(black_hole['core'].radius * 5, black_hole['core'].radius * 15)
            particle['angle'] = random.uniform(0, 2 * math.pi)
            particle['height'] = random.uniform(-black_hole['core'].radius, black_hole['core'].radius) * 0.5

# 更新脉冲星
def update_pulsar(pulsar):
    """更新脉冲星效果"""
    # 更新旋转角度
    pulsar['angle'] += pulsar['rotation_speed']
    
    # 旋转光束
    new_axis1 = vp.vec(math.sin(pulsar['angle']), math.cos(pulsar['angle']), 0) * pulsar['beam1'].axis.mag
    new_axis2 = vp.vec(-math.sin(pulsar['angle']), -math.cos(pulsar['angle']), 0) * pulsar['beam2'].axis.mag
    
    pulsar['beam1'].axis = new_axis1
    pulsar['beam2'].axis = new_axis2
    
    # 更新脉冲计时器
    pulsar['pulse_timer'] += 1
    if pulsar['pulse_timer'] >= pulsar['pulse_period']:
        pulsar['pulse_timer'] = 0
        
        # 脉冲效果 - 光束亮度变化
        brightness = 0.5 + 0.5 * math.sin(pulsar['pulse_timer'] / pulsar['pulse_period'] * math.pi)
        color = vp.vec(brightness, brightness, 1) * brightness
        
        pulsar['beam1'].color = color
        pulsar['beam2'].color = color
        pulsar['core'].color = vp.vec(brightness, brightness, brightness)

# 键盘和鼠标交互
def handle_keydown(evt):
    """处理键盘按下事件"""
    global RUNNING
    
    # WASD控制摄像机移动
    move_speed = 0.5 * AU / SCALE_FACTOR
    
    if evt.key == 'w':
        scene.camera.pos += scene.camera.axis * move_speed
    elif evt.key == 's':
        scene.camera.pos -= scene.camera.axis * move_speed
    elif evt.key == 'a':
        # 左移 - 计算垂直于摄像机轴和上方向的向量
        right = vp.cross(scene.camera.axis, scene.up)
        scene.camera.pos -= vp.norm(right) * move_speed
    elif evt.key == 'd':
        # 右移
        right = vp.cross(scene.camera.axis, scene.up)
        scene.camera.pos += vp.norm(right) * move_speed
    elif evt.key == ' ':
        # 空格键暂停/恢复
        RUNNING = not RUNNING

# 注册键盘事件处理函数
scene.bind('keydown', handle_keydown)

# 创建场景
stars = create_starry_background(3000)
sun, planets, asteroids = create_solar_system()
deep_space_objects = create_deep_space_objects()

# 主循环
while True:
    vp.rate(30)  # 限制帧率
    
    if RUNNING:
        # 更新恒星
        update_star(sun)
        
        # 更新行星
        update_planets(planets)
        
        # 更新小行星带
        update_asteroids(asteroids)
        
        # 更新深空天体
        for obj in deep_space_objects:
            if obj["type"] == "black_hole":
                update_black_hole(obj["object"])
            elif obj["type"] == "pulsar":
                update_pulsar(obj["object"])
    
    # 根据摄像机位置优化渲染(LOD)
    for planet in planets:
        distance = vp.mag(planet['planet'].pos - scene.camera.pos)
        # 远距离简化模型
        if distance > 10 * AU / SCALE_FACTOR:
            for stripe in planet['stripes']:
                stripe.visible = False
        else:
            for stripe in planet['stripes']:
                stripe.visible = True 