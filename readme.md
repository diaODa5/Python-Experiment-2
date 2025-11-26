Alien Invasion

这是一个使用 Pygame 库开发的经典街机风格游戏，玩家操控一艘飞船，射击并摧毁从屏幕上方降落的外星舰队。

#游戏特色

##飞船控制: 玩家可以左右移动飞船并进行射击。

##外星舰队: 外星人以编队形式移动，并在到达屏幕边缘时改变方向并向下移动一层。

##得分和等级: 摧毁外星人可以获得分数，并且随着等级的提升，游戏难度（如速度）会增加。

##生命值系统: 飞船拥有有限的生命 (ships_left)，当被外星人击中或外星人到达屏幕底部时，会损失一次生命。

##高分记录: 游戏会持久化存储最高分到 high_score.txt 文件中。

##道具系统: 游戏过程中会随机生成两种特殊道具（PowerUp）：

💎 Diamond (钻石): 暂时增大子弹的宽度 (bullet_width)，实现更宽的子弹。

🛡️ Shield (护盾): 暂时使飞船进入无敌状态 (is_invulnerable)，免疫外星人碰撞。

##
各文件完成的功能

alien_invasion.py:游戏主文件，包含主循环、事件处理、屏幕更新、创建/更新外星人和子弹等核心逻辑，并管理道具的生成和碰撞计时。

settings.py:游戏配置，包含屏幕尺寸、速度参数、子弹设置、生命限制，以及动态难度调整和道具时间设置。

game_stats.py:管理游戏状态（剩余生命、当前得分、等级）以及最高分的加载和保存。

ship.py:定义飞船类 (Ship)，包含移动逻辑、图像加载以及无敌状态 (is_invulnerable) 的管理。

bullet.py:定义子弹类 (Bullet)，负责子弹的创建、移动和绘制，其宽度受 settings.bullet_width 控制。

alien.py:定义外星人类 (Alien)，负责外星人的图像加载、位置、移动和边缘检测。

powerup.py:定义道具基类 (PowerUp) 及其子类 Diamond 和 Shield，负责道具的图像加载和随机生成。

scoreboard.py:负责在屏幕上显示当前得分、最高分、当前等级和剩余飞船生命值。

button.py:定义按钮类 (Button)，用于绘制游戏开始前的 "Play" 按钮。

如何运行

#安装 Pygame:

#准备资源文件: 确保您有以下图像文件（.bmp 格式），并放置在名为 images 的文件夹中，因为代码中引用了这些路径：

images/ship.bmp

images/alien.bmp

images/diamond.bmp

images/shield.bmp

#运行游戏:

Bash：输入

python alien_invasion.py

#键位控制

右方向键 (K_RIGHT)	飞船向右移动

左方向键 (K_LEFT)	飞船向左移动

空格键 (K_SPACE)	发射子弹

Q (K_q)	退出游戏并保存最高分