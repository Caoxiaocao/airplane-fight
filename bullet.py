import pygame

# 游戏窗口设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 颜色常量
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)  # 弹窗背景颜色
GREEN = (0, 255, 0)  # 血条颜色


# 子弹类
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, damage):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -8
        self.damage = damage  # 子弹伤害值

    def update(self, player=None, screen=None, c_time=None):
        self.rect.y += self.speed
        if self.rect.bottom < 0:  # 飞出屏幕后删除
            self.kill()

# BOSS 子弹类
class BossBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.target_x = target_x  # 目标位置（玩家位置）
        self.target_y = target_y
        # 计算子弹的方向
        self.direction = pygame.math.Vector2(target_x - x, target_y - y).normalize()

    def update(self, player=None, screen=None, c_time=None):
        # 根据方向移动子弹
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed
        # 如果子弹飞出屏幕，则销毁
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or \
           self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()