# 玩家飞机类
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


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 加载玩家战机贴图
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        # self.image = pygame.Surface((50, 50))
        # self.image.fill(BLUE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80))
        self.speed = 5

        # 射击冷却时间
        self.shoot_delay = 100  # 毫秒
        self.last_shot = 0

    def update(self, *args):
        # 获取键盘输入（WASD 控制）
        keys = pygame.key.get_pressed()

        # 横向移动（A/D 或 左/右方向键）
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # 纵向移动（W/S 或 上/下方向键）
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # 限制移动范围（避免超出屏幕）
        self.rect.clamp_ip(args[1].get_rect())  # 更简洁的边界限制方法

    def draw_health_bar(self, screen, hp, max_hp, font):
        # 血条的位置和大小
        bar_length = 50
        bar_height = 25
        x = self.rect.centerx - bar_length // 2
        y = self.rect.bottom + 5

        # 计算血条的当前长度
        health_percentage = hp / max_hp
        current_bar_length = int(bar_length * health_percentage)

        blood_text = font.render(f"HP:", True, YELLOW)
        screen.blit(blood_text, (10, 10))
        # 绘制血条背景
        pygame.draw.rect(screen, RED, (70, 15, bar_length, bar_height))
        # 绘制当前血条
        pygame.draw.rect(screen, GREEN, (70, 15, current_bar_length, bar_height))