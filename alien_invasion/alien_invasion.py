import sys
import pygame
from time import sleep

from setting import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    """ 管理游戏资源和行为的类 """
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        # 全屏
        """ self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height """
    
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        
        self.clock = pygame.time.Clock()
        # self.screen = pygame.display.set_mode((1200,800))
        # self.bg_color = (230,230,230)
        pygame.display.set_caption("Alien Invasion")
        # 创建一个用于存储游戏统计信息的示例
        self.stats = GameStats(self)
        self.sb = ScoreBoard(self)
        self.ship = Ship(self)
        # 游戏启动后处于活动状态
        self.game_active = False
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
        # 创建 Play 按钮
        self.play_button = Button(self, "Play")
        
    def run_game(self):
        """ 开始游戏的主循环 """
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullet()
                self._update_aliens()
            # 每次循环时都重绘屏幕
            self._update_screen()
            self.clock.tick(60)
    
    def _check_events(self):
        """ 响应按键和鼠标事件 """
        # 监听键盘和鼠标事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_key_down_events(event)
            elif event.type == pygame.KEYUP:
                self._check_key_up_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
                
    def _check_play_button(self, mouse_pos):
        """ 在玩家单击Play按钮时开始新游戏 """
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            """ 重置游戏的统计信息 """
            # 还原游戏设置
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            
            # 清空外星人列表和子弹列表
            self.aliens.empty()
            self.bullets.empty()
            
            # 创建一个新的外星舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            # 隐藏光标
            pygame.mouse.set_visible(False)
    
    def _check_key_down_events(self, event):
        """ 响应按下 """
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船
            # self.ship.rect.x += 1
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        
    def _check_key_up_events(self, event):
        """ 响应抬起 """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
            
    def _fire_bullet(self):
        """ 创建一颗子弹，并将其加入编组 """
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)
            
    def _update_bullet(self):
        """ 更新子弹的位置 """
        self.bullets.update()
        # 删除已消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_bullet_alien_collisions()
        
    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人的碰撞"""
        # 删除发生碰撞的子弹和外星人
        # 检查是否有子弹击中了外星人
        # 如果是，就删除相应的子弹和外星人
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score +=self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        
        if not self.aliens:
            # 删除现有的子弹并创建一个新的舰队
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            # 提高等级
            self.stats.level += 1
            self.sb.prep_level()
    
    def _create_fleet(self):
        """ 创建一个外星舰队 """
        # 创建一个外星人，再不断添加，直到没有空间添加外星人为止
        # 外星人的间距为外星人的宽度和外星人的高度
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 10 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            # 添加一行外星人之后，重置x值并递增y
            current_x = alien_width
            current_y += 2 * alien_height    
    
    def _create_alien(self, x_position, y_position):
        """ 创建一个外星人，并将其加入外星舰队 """
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)
        
    def _update_aliens(self):
        """ 检查是否有外星人位于屏幕边缘,更新外星舰队中所有外星人的位置 """    
        self._check_fleet_edges()
        self.aliens.update()
        # 检测外星人和飞船之间的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print("Ship hit!!!")
            self._ship_hit()
        # 检查是否有外星人到达了屏幕的下边缘
        self._check_aliens_bottom()
    
    def _check_fleet_edges(self):
        """ 在外星人到达边缘时采取相应的措施 """
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """ 将整个舰队下移，并改变它们的方向 """
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
    
    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left > 0:
            # 将 ships_left 减 1
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # 清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            # 创建一个新的外星舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
            # 暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕的下边缘"""    
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # 像飞船被撞到一样进行处理
                self._ship_hit()
                break
    
    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        self.ship.blitme()
        self.aliens.draw(self.screen)
        # 显示得分
        self.sb.show_score()
        # 如果游戏处于非活动状态，就绘制 Play 按钮
        if not self.game_active:
            self.play_button.draw_button()
        # 让最近绘制的屏幕可见 
        pygame.display.flip()

if __name__ == '__main__':
    # 创建游戏示例，并且运行游戏
    ai = AlienInvasion()
    ai.run_game()