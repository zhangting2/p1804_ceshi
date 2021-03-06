#-*- coding=utf-8 -*-
import pygame
import time, random

class BasePlane(object):
    def __init__(self, screen, x, y, image_name):
        self.screen = screen
        self.x = x
        self.y = y
         #3.英雄
        self.image = pygame.image.load(image_name)
        # 4. 定义英雄的初始位置
        self.rect = pygame.Rect(self.x, self.y, 102, 126)
        self.bullet_list = [] #保持子弹引用
        self.bullet_remove = [] #保持待删除的子弹
    def display(self):
        self.screen.blit(self.image,self.rect)
        if len(self.bullet_list) > 0:
            for bullet in self.bullet_list:
                bullet.display()
                bullet.move()
                if bullet.judge():
                    self.bullet_remove.append(bullet)
            if len(self.bullet_remove) > 0:
                for i in self.bullet_remove:
                    self.bullet_list.remove(i)
                # self.bullet_remove.clear()
                del self.bullet_remove[:]

class HeroPlane(BasePlane):
    """英雄的创建和展示类"""
    def __init__(self, arg):
        super(HeroPlane, self).__init__( arg, 150, 500, './images/hero1.png')
    

    def fire(self):
        self.bullet_list.append(Bullet(self.screen, self.rect.x, self.rect.y))
        
class EnemyPlane(BasePlane):
    """敌人飞机 创建和展示类"""
    def __init__(self, arg):
        super(EnemyPlane, self).__init__(arg, 0, 0, './images/enemy0.png')
        self.direction = 'right' #保持敌机默认方向

    def move(self):
        if self.direction == 'right':
            self.rect.x += 5
        elif self.direction == 'left':
            self.rect.x -= 5

        if self.rect.x > 480-self.rect.width:
            self.direction = 'left'
        elif self.rect.x < 0:
            self.direction = 'right'

    def fire(self):
        if random.randint(1,100) == 78:
            self.bullet_list.append(EnemyBullet(self.screen, self.rect.x, self.rect.y))
   
class BaseBullet(object):
    """BaseBullet for ClassName"""
    def __init__(self, arg ,x ,y ,image_name):
        self.screen = arg
        self.x = x
        self.y = y
         #3.英雄
        self.image = pygame.image.load(image_name)
    def display(self):
        self.screen.blit(self.image,(self.x, self.y))
        
class Bullet(BaseBullet):
    """docstring for Bullet"""
    def __init__(self, arg ,x ,y):
        BaseBullet.__init__(self, arg, x+40, y+20, './images/bullet.png')
   
    def move(self):
        self.y -= 4
    def judge(self):
        if self.y < 0:
            return True
        else:
            return False
        
class EnemyBullet(BaseBullet):
    """docstring for Bullet"""
    def __init__(self, arg ,x ,y):
        BaseBullet.__init__(self, arg, x+25, y+40, './images/bullet1.png')
   
    def move(self):
        self.y += 4
    def judge(self):
        if self.y > 600:
            return True
        else:
            return False


def key_control(hero):
    '''键盘的监听控制方法'''
    move_step = 5
    move_x, move_y = 0, 0
    # =====事件监听
    for event in pygame.event.get():
        # 判断用户是否点击了关闭按钮
        if event.type == pygame.QUIT:
            print("退出游戏...")
            pygame.quit()
            # 直接退出系统
            exit()
        elif event.type == pygame.KEYDOWN:
            #键盘有按下？
            if event.key == pygame.K_LEFT:
                #按下的是左方向键的话，把x坐标减一
                move_x = -move_step
            elif event.key == pygame.K_RIGHT:
                #右方向键则加一
                move_x = move_step
            elif event.key == pygame.K_UP:
                #类似了
                move_y = -move_step
            elif event.key == pygame.K_DOWN:
                move_y = move_step
            elif event.key == pygame.K_SPACE:
                hero.fire()
        elif event.type == pygame.KEYUP:
            #如果用户放开了键盘，图就不要动了
            move_x = 0
            move_y = 0

        #计算出新的坐标
        hero.rect.x += move_x
        hero.rect.y += move_y

def main():# 主方法 调用 类和方法
    #1.窗口
    screen = pygame.display.set_mode((480,600),0,32)
    #2.背景
    background = pygame.image.load('./images/background.png')
    #3.英雄
    hero = HeroPlane(screen)
    # 4.1. 创建游戏时钟对象
    clock = pygame.time.Clock()

    # 5创建一个敌人飞机
    enemy = EnemyPlane(screen)

    while True:
        screen.blit(background,(0,0))
        hero.display()
        enemy.display()
        enemy.move() #让敌机移动
        enemy.fire()
        # 设置屏幕刷新帧率
        clock.tick(60)
        if hero.rect.y <= 0:
            hero.rect.y = 500
        key_control(hero)
        pygame.display.update()
   
if __name__ == '__main__':
    main()
