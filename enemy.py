# 普通敌机
import random

import pygame

from bullet import BossBullet

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


class NormalEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/enemy_normal.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH-20), -20))
        self.speed = 3
        self.health = 20
        self.max_health = 20

    def update(self, *args):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False

    def draw_health_bar(self, screen):
        bar_length = 40
        bar_height = 5
        x = self.rect.centerx - bar_length // 2
        y = self.rect.top - 10
        health_percentage = self.health / self.max_health
        current_bar_length = int(bar_length * health_percentage)
        # pygame.draw.rect(screen, GRAY, (x, y, bar_length, bar_height))
        pygame.draw.rect(screen, RED, (x, y, current_bar_length, bar_height))


# 快速敌机
class FastEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/enemy_normal.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        # self.image = pygame.Surface((30, 30))
        # self.image.fill(RED)
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH-20), -20))
        self.speed = 5  # 速度更快
        self.health = 10  # 生命值较低
        self.max_health = 10

    def update(self, player=None, screen=None, c_time=None):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False

    def draw_health_bar(self, screen):
        bar_length = 30
        bar_height = 5
        x = self.rect.centerx - bar_length // 2
        y = self.rect.top - 10
        health_percentage = self.health / self.max_health
        current_bar_length = int(bar_length * health_percentage)
        # pygame.draw.rect(screen, GRAY, (x, y, bar_length, bar_height))
        pygame.draw.rect(screen, RED, (x, y, current_bar_length, bar_height))


# 重型敌机
class HeavyEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/enemy_heavy.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        # self.image = pygame.Surface((60, 60))
        # self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH-20), -20))
        self.speed = 1  # 速度较慢
        self.health = 40  # 生命值较高
        self.max_health = 40

    def update(self, player=None, screen=None, c_time=None):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False

    def draw_health_bar(self, screen):
        bar_length = 60
        bar_height = 5
        x = self.rect.centerx - bar_length // 2
        y = self.rect.top - 10
        health_percentage = self.health / self.max_health
        current_bar_length = int(bar_length * health_percentage)
        # pygame.draw.rect(screen, GRAY, (x, y, bar_length, bar_height))
        pygame.draw.rect(screen, RED, (x, y, current_bar_length, bar_height))



# BOSS敌机
class BossEnemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/enemy_boss.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (750, 100))
        # self.image = pygame.Surface((750, 100))
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, -50))
        self.speed = 1
        self.health = 300
        self.max_health = 300
        # self.last_attack = pygame.time.get_ticks()  # 上次攻击时间
        self.last_attack = 0
        self.attack_delay = 2000  # 攻击冷却时间（2秒）

    def update(self, player=None, screen=None, c_time=None):
        # self.rect.y += self.speed
        self.rect.y = 40
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

        # 检查是否可以攻击
        if c_time > self.attack_delay:
            bullet = self.attack(player)  # 调用攻击方法
            if bullet:  # 如果生成了子弹
                return bullet  # 返回生成的子弹对象

    def attack(self, player):
        """BOSS 敌机攻击"""
        if player:  # 如果玩家存在
            bullet = BossBullet(self.rect.centerx, self.rect.bottom, player.rect.centerx, player.rect.centery)
            return bullet  # 返回生成的子弹对象

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False

    def draw_health_bar(self, screen):
        bar_length = 300
        bar_height = 20
        x = self.rect.centerx - bar_length // 2
        y = self.rect.top - 30
        health_percentage = self.health / self.max_health
        current_bar_length = int(bar_length * health_percentage)
        # pygame.draw.rect(screen, GRAY, (x, y, bar_length, bar_height))
        pygame.draw.rect(screen, RED, (x, y, current_bar_length, bar_height))


