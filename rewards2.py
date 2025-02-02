import random
import sys

import pygame
from pygame.locals import *

# 颜色常量
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)  # 弹窗背景颜色
GREEN = (0, 255, 0)  # 血条颜色

# 奖励池
REWARD_POOL = [
    {"name": "子弹数量", "type": "bullet_count", "description": "+  1", "score": 100},
    {"name": "子弹伤害", "type": "bullet_damage", "description": "+ 10", "score": 100},
    {"name": "移动速度", "type": "move_speed", "description": "+  1", "score": 50},
    {"name": "生命值", "type": "max_health", "description": "+ 10", "score": 50},
    {"name": "攻击频率", "type": "attack_speed", "description": "-100", "score": 100},
    {"name": "护盾", "type": "shield", "description": "+  1", "score": 50}
]

def show_reward_screen(screen_width, screen_height, screen, bg_color, text_color, font, score, reward_cost):
    """显示奖励选择界面"""
    # 随机选择 3 项奖励
    rewards = random.sample(REWARD_POOL, 3)
    selected_index = 0
    running = True

    while running:
        # screen.fill(bg_color)
        pygame.draw.rect(screen, GRAY, (screen_width // 2 - 210, 50, 400, 50))
        draw_text(f"选择奖励(消耗{reward_cost}SC)", screen, text_color, font, screen_width // 2 - 170, 60)
        pygame.draw.rect(screen, GRAY, (screen_width // 2 - 110, 400, 200, 50))
        draw_text(f"放弃奖励", screen, text_color, font, screen_width // 2 - 80, 410)
        if selected_index == 4:
            pygame.draw.rect(screen, (0, 255, 0), (screen_width // 2 - 110, 400, 200, 50), 3)

        # 绘制奖励选项
        for i, reward in enumerate(rewards):
            # 绘制矩形框
            # rect_x = screen_width // 2 - 150
            # rect_y = 150 + i * 120
            rect_x = screen_width / 5 * (i + 1)
            rect_y = screen_height // 2 - 150
            rect_width = 150
            rect_height = 243

            # 判断分数是否足够兑换
            if score >= reward_cost:
                color = (0, 255, 0) if i == selected_index else (128, 128, 128)  # 选中高亮
            else:
                color = (255, 0, 0) if i == selected_index else (64, 64, 64)  # 分数不足时禁用

            pygame.draw.rect(screen, GRAY, (rect_x, rect_y, rect_width, rect_height))
            pygame.draw.rect(screen, color, (rect_x, rect_y, rect_width, rect_height), 3)

            # 绘制奖励名称和描述
            draw_text(reward["name"], screen, text_color, font, rect_x + 10, rect_y + 60)
            draw_text(reward["description"], screen, text_color, font, rect_x + 40, rect_y + 100)
            # rect = pygame.Rect(rect_x + 10, rect_y + 20, rect_width - 20, rect_height - 40)
            # draw_wrapped_text(reward["name"], screen, text_color, font, rect)
            # rect.y += 50  # 调整描述文本的位置
            # draw_wrapped_text(reward["description"], screen, text_color, font, rect)

        pygame.display.flip()

        # 处理键盘事件
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == K_a:
                    selected_index = (selected_index - 1) % len(rewards)
                elif event.key == K_RIGHT or event.key == K_d:
                    selected_index = (selected_index + 1) % len(rewards)
                elif event.key == K_DOWN or event.key == K_s:
                    # pygame.draw.rect(screen, (0, 255, 0), (screen_width // 2 - 110, 400, 200, 50), 3)
                    selected_index = 4
                elif event.key == K_UP or event.key == K_w:
                    selected_index = 1
                elif event.key == K_RETURN or event.key == K_SPACE:
                    if score >= reward_cost and selected_index != 4:  # 检查分数是否足够
                        return rewards[selected_index]["type"]
                    if selected_index == 4:
                        return []
                if event.key == K_1:
                    selected_index = 0
                elif event.key == K_2:
                    selected_index = 1
                elif event.key == K_3:
                    selected_index = 2
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()

def draw_wrapped_text(text, screen, color, font, rect, line_spacing=10):
    """绘制自动换行的文本"""
    words = text.split(' ')
    space_width, _ = font.size(' ')
    x, y = rect.topleft
    max_width = rect.width
    max_height = rect.height

    lines = []
    current_line = []
    current_width = 0

    # 将文本拆分为多行
    for word in words:
        word_width, word_height = font.size(word)
        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width + space_width
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
            current_width = word_width + space_width
    if current_line:
        lines.append(' '.join(current_line))

    # 绘制每一行文本
    y_offset = 0
    for line in lines:
        line_surface = font.render(line, True, color)
        line_rect = line_surface.get_rect()
        line_rect.topleft = (x, y + y_offset)
        screen.blit(line_surface, line_rect)
        y_offset += line_rect.height + line_spacing

def apply_reward(reward_type, upgrades, hp, score):
    """应用奖励"""
    if reward_type == "bullet_count":
        upgrades.append("子弹数量+1")
        return hp, score
    elif reward_type == "bullet_damage":
        upgrades.append("子弹伤害+10")
        return hp, score
    elif reward_type == "move_speed":
        upgrades.append("移动速度+1")
        return hp, score
    elif reward_type == "max_health":
        upgrades.append("最大生命值+10")
        return hp + 10, score
    elif reward_type == "attack_speed":
        upgrades.append("攻击速度+1")
        return hp, score
    elif reward_type == "shield":
        upgrades.append("获得护盾")
        return hp, score
    return hp, score

def draw_text(text, screen, color, font, x, y):
    """绘制文本"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)