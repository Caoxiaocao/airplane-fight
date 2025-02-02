import sys
import pygame
import random
from bullet import BossBullet, Bullet
from enemy import NormalEnemy, FastEnemy, HeavyEnemy, BossEnemy
from player import Player
from rewards2 import apply_reward, show_reward_screen, draw_text

# 初始化 Pygame
pygame.init()

# 游戏窗口设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("飞机大战")

# 颜色常量
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)  # 弹窗背景颜色
GREEN = (0, 255, 0)  # 血条颜色

# 帧率控制
clock = pygame.time.Clock()
FPS = 60

# 加载音效
pygame.mixer.init()  # 初始化音频模块
shoot_sound = pygame.mixer.Sound("Sound Effects Shooting sounds 001/SHOOT008.mp3")  # 发射音效
hit_sound = pygame.mixer.Sound("Sound Effects Shooting sounds 001/SHOOT005.mp3")  # 击落音效
# 创建音效通道
shoot_channel = pygame.mixer.Channel(0)  # 发射音效通道
hit_channel = pygame.mixer.Channel(1)  # 击落音效通道

# 初始化字体
font_path = "SIMKAI.TTF"  # 替换为你的中文字体文件路径
font = pygame.font.Font(font_path, 36)
font_18 = pygame.font.Font(font_path, 18)

# 敌机生命增强参数
ENEMY_HEALTH_INCREASE = 1.5  # 每次增强的生命值倍数
ENEMY_HEALTH_INTERVAL = 10000  # 增强间隔（毫秒）

class Game:
    def __init__(self):
        # 加载背景贴图
        self.background = pygame.image.load("assets/background.png").convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # # 加载玩家战机贴图
        # self.player_image = pygame.image.load("assets/player.png").convert_alpha()
        #
        # # 加载敌机贴图
        # self.enemy_normal_image = pygame.image.load("assets/enemy_normal.png").convert_alpha()
        # self.enemy_fast_image = pygame.image.load("assets/enemy_normal.png").convert_alpha()
        # self.enemy_heavy_image = pygame.image.load("assets/enemy_heavy.png").convert_alpha()
        # self.enemy_boss_image = pygame.image.load("assets/enemy_boss.png").convert_alpha()

        self.screen = screen
        self.clock = clock
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.boss_bullets = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.score = 0
        self.boss_score = 0
        self.hp = 50
        self.hp_max = 50

        self.bullet_count = 1  # 子弹数量
        self.bullet_damage = 10  # 子弹伤害
        self.move_speed = 3  # 移动速度
        self.max_health = 30  # 最大生命值
        self.attack_speed = 500  # 攻击间隔（毫秒）
        self.shield = False  # 是否拥有护盾
        self.reward_cost = 50  # 初始兑换奖励需要的分数
        self.change_score = 100 # 出現boss的積分

        self.paused = False
        self.upgrades = []
        self.boss_spawned = False
        self.reward_time = pygame.time.get_ticks()
        self.last_attack_time = pygame.time.get_ticks()
        self.current_enemy_health = 1

        # 敌机生成计时器
        self.ENEMY_SPAWN = pygame.USEREVENT + 1
        pygame.time.set_timer(self.ENEMY_SPAWN, 1000)  # 每1秒生成一个敌机

    def run(self):
        running = True
        while running:
            self.handle_events()
            if not self.paused:
                self.update()
                self.render()
            self.clock.tick(FPS)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # 按 P 键暂停游戏
                    self.paused = not self.paused
                    if self.paused:
                        self.show_pause_screen()
            elif event.type == self.ENEMY_SPAWN:
                self.spawn_enemy()

    def update(self):
        current_time = pygame.time.get_ticks()
        self.handle_shooting(current_time)
        self.handle_collisions()
        self.handle_rewards(current_time)
        self.handle_boss(current_time)
        self.all_sprites.update(self.player, self.screen, current_time - self.last_attack_time)

    def render(self):
        # self.screen.fill(BLACK)
        # self.all_sprites.draw(self.screen)
        # 绘制背景
        self.screen.blit(self.background, (0, 0))
        # 绘制所有精灵
        self.all_sprites.draw(self.screen)

        # 显示敌机血条
        for enemy in self.enemies:
            enemy.draw_health_bar(self.screen)

        # 显示护盾特效
        if self.shield:
            # 计算护盾特效的位置和大小
            shield_radius = max(self.player.rect.width, self.player.rect.height) + 10
            shield_x = self.player.rect.centerx
            shield_y = self.player.rect.centery

            # 绘制闪烁的护盾特效
            alpha = int((pygame.time.get_ticks() % 1000) / 1000 * 255)  # 闪烁效果
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(shield_surface, (0, 255, 255, alpha), (shield_radius, shield_radius), shield_radius, 5)
            self.screen.blit(shield_surface, (shield_x - shield_radius, shield_y - shield_radius))

        self.draw_ui()
        pygame.display.flip()

    def handle_shooting(self, current_time):
        mouse_pressed = pygame.mouse.get_pressed()
        # if mouse_pressed[0] and current_time - self.player.last_shot > self.player.shoot_delay:
        if mouse_pressed[0] and current_time - self.player.last_shot > self.attack_speed:
            # bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
            # bullet_left = Bullet(self.player.rect.centerx - 10, self.player.rect.top)
            # self.all_sprites.add(bullet)
            # self.bullets.add(bullet)
            # self.all_sprites.add(bullet_left)
            # self.bullets.add(bullet_left)
            for i in range(self.bullet_count):
                bullet = Bullet(self.player.rect.centerx - 10 * i, self.player.rect.top, self.bullet_damage)
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)
            self.player.last_shot = current_time
            shoot_channel.play(shoot_sound)

    def handle_collisions(self):
        # 子弹与敌机的碰撞检测
        for bullet in self.bullets:
            enemy_hit_list = pygame.sprite.spritecollide(bullet, self.enemies, False)
            for enemy in enemy_hit_list:
                bullet.kill()
                if enemy.take_damage(bullet.damage):
                    if isinstance(enemy, FastEnemy) or isinstance(enemy, HeavyEnemy):
                        self.score += 20
                    else:
                        self.score += 10
                    self.boss_score += 10
                    hit_channel.play(hit_sound)

                    # 如果被击败的敌机是 Boss，重置 boss_spawned 状态
                    if isinstance(enemy, BossEnemy):
                        self.boss_spawned = False
                        self.boss_score = 0
                        self.show_reward()  # 调用奖励系统

        # Boss 子弹与玩家的碰撞检测
        for bullet in self.boss_bullets:
            if pygame.sprite.collide_rect(bullet, self.player):
                bullet.kill()
                if self.shield:  # 如果玩家有护盾，减免伤害并消耗护盾
                    self.shield = False
                    print("护盾生效，抵消一次伤害！")
                else:
                    self.hp -= 10  # 玩家掉血
                    if self.hp <= 0:
                        self.game_over()

        # 玩家与敌机的碰撞检测
        if pygame.sprite.spritecollide(self.player, self.enemies, True):
            if self.shield:  # 如果玩家有护盾，减免伤害并消耗护盾
                self.shield = False
                print("护盾生效，抵消一次伤害！")
            else:
                self.hp -= 10
                if self.hp <= 0:
                    self.game_over()

    def handle_rewards(self, current_time):
        # if current_time - self.reward_time >= 10000:
        #     reward = show_reward_screen(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, GRAY, BLACK, font)
        #     self.hp, self.score = apply_reward(reward, self.upgrades, self.hp, self.score)
        #     self.current_enemy_health += ENEMY_HEALTH_INCREASE
        #     for enemy in self.enemies:
        #         enemy.health += ENEMY_HEALTH_INCREASE
        #         enemy.max_health += ENEMY_HEALTH_INCREASE
        #     self.reward_time = current_time
        pass

    def show_reward(self):
        """显示奖励选择界面并应用奖励"""
        # reward_type  = show_reward_screen(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, GRAY, BLACK, font)
        # self.hp, self.score = apply_reward(reward_type , self.upgrades, self.hp, self.score)
        #
        # # 根据奖励类型更新玩家属性
        # if reward_type == "bullet_count":
        #     self.bullet_count += 1
        # elif reward_type == "bullet_damage":
        #     self.bullet_damage += 10
        # elif reward_type == "move_speed":
        #     self.move_speed += 1
        #     self.player.speed = self.move_speed
        # elif reward_type == "max_health":
        #     self.hp_max += 10
        #     self.hp = self.hp_max
        # elif reward_type == "attack_speed":
        #     self.attack_speed = max(100, self.attack_speed - 100)  # 攻击间隔不低于 100ms
        # elif reward_type == "shield":
        #     self.shield = True

        reward_type = show_reward_screen(SCREEN_WIDTH, SCREEN_HEIGHT, self.screen, GRAY, BLACK, font, self.score,
                                         self.reward_cost)
        if reward_type:
            # 扣除分数
            self.score -= self.reward_cost
            self.reward_cost += 50  # 下一次兑换需要的分数增加 50

            # # 根据奖励类型更新玩家属性
            if reward_type == "bullet_count":
                self.bullet_count += 1
            elif reward_type == "bullet_damage":
                self.bullet_damage += 10
            elif reward_type == "move_speed":
                self.move_speed += 1
                self.player.speed = self.move_speed
            elif reward_type == "max_health":
                self.hp_max += 10
                self.hp = self.hp_max
            elif reward_type == "attack_speed":
                self.attack_speed = max(100, self.attack_speed - 100)  # 攻击间隔不低于 100ms
            elif reward_type == "shield":
                self.shield = True

            # 应用奖励
            self.hp, self.score = apply_reward(reward_type, self.upgrades, self.hp, self.score)

            # 增强敌机生命值
            self.current_enemy_health *= ENEMY_HEALTH_INCREASE
            self.change_score *= ENEMY_HEALTH_INCREASE
            # for enemy in self.enemies:
            #     enemy.health *= ENEMY_HEALTH_INCREASE
            #     enemy.max_health *= ENEMY_HEALTH_INCREASE
            #     if isinstance(enemy, BossEnemy):
            #         enemy.attack_delay = max(500, enemy.attack_delay - 500)

            # 重置奖励计时器（如果需要）
            self.reward_time = pygame.time.get_ticks()
        else:
            self.current_enemy_health *= ENEMY_HEALTH_INCREASE
            self.change_score *= ENEMY_HEALTH_INCREASE
            self.reward_time = pygame.time.get_ticks()

    def handle_boss(self, current_time):
        if self.boss_score >= self.change_score and not self.boss_spawned:
            boss_enemy = BossEnemy()
            # 应用敌机生命增强倍数
            boss_enemy.health *= self.current_enemy_health
            boss_enemy.max_health *= self.current_enemy_health
            boss_enemy.attack_delay = max(200, boss_enemy.attack_delay - 500 * self.current_enemy_health)
            print('attack: ', boss_enemy.attack_delay)
            self.all_sprites.add(boss_enemy)
            self.enemies.add(boss_enemy)
            self.boss_spawned = True

        if self.boss_spawned:
            for enemy in self.enemies:
                if isinstance(enemy, BossEnemy):
                    bullet = enemy.update(self.player, self.screen, current_time - self.last_attack_time)
                    if bullet:
                        self.all_sprites.add(bullet)
                        self.boss_bullets.add(bullet)
                        self.last_attack_time = current_time
                        print('生命：', enemy.health, '攻击间隔：', enemy.attack_delay)

    def draw_ui(self):
        # 显示分数
        score_text = font.render(f"SC: {self.score}", True, YELLOW)
        self.screen.blit(score_text, (10, 40))

        # 显示玩家血条
        self.player.draw_health_bar(self.screen, self.hp, self.hp_max, font)

        # 显示已选择的奖励
        for i, upgrade in enumerate(self.upgrades):
            draw_text(f"奖励{i + 1}: {upgrade}", self.screen, YELLOW, font_18, SCREEN_WIDTH - 170, i * 20 + 10)

    def spawn_enemy(self):
        enemy_type = random.choices(["normal", "fast", "heavy"], weights=[70, 20, 10], k=1)[0]
        if enemy_type == "normal":
            enemy = NormalEnemy()
        elif enemy_type == "fast":
            enemy = FastEnemy()
        elif enemy_type == "heavy":
            enemy = HeavyEnemy()

        # 应用敌机生命增强倍数
        enemy.health *= self.current_enemy_health
        enemy.max_health *= self.current_enemy_health

        self.all_sprites.add(enemy)
        self.enemies.add(enemy)

    def game_over(self):
        choice = self.show_game_over_screen()
        if choice == "restart":
            self.__init__()  # 重置游戏状态
        elif choice == "quit":
            pygame.quit()
            sys.exit()

    def show_game_over_screen(self):
        popup_x, popup_y = self.show_window_screen(400, 200)
        draw_text("游戏结束！", self.screen, RED, font, popup_x + 120, popup_y + 30)
        draw_text("R(重玩) | Q(退出)", self.screen, BLACK, font, popup_x + 50, popup_y + 100)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "restart"
                    if event.key == pygame.K_q:
                        return "quit"

    def show_pause_screen(self):
        popup_x, popup_y = self.show_window_screen(400, 200)
        draw_text("游戏暂停!", self.screen, RED, font, popup_x + 120, popup_y + 30)
        draw_text("P(继续)", self.screen, BLACK, font, popup_x + 140, popup_y + 100)
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        return

    def show_window_screen(self, w, h):
        popup_width, popup_height = w, h
        popup_x = (SCREEN_WIDTH - popup_width) // 2
        popup_y = (SCREEN_HEIGHT - popup_height) // 2
        pygame.draw.rect(self.screen, GRAY, (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, BLACK, (popup_x, popup_y, popup_width, popup_height), 2)
        return popup_x, popup_y


# 启动游戏
if __name__ == "__main__":
    game = Game()
    game.run()