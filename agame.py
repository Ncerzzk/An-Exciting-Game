import pygame
from pygame.locals import *
from sys import exit

from enum import Enum



class Direction(Enum):
    DOWN=0
    LEFT=1
    RIGHT=2
    UP=3
class Actor_State(Enum):
    WAIT=0 # 待机
    STOP=1 # 停止
    WALKING=2 # 移动中

class Menu_Item(Enum):
    MOVE=0
    ATTACK=1
    REST=2

class Position():
    def __init__(self,x,y=None):
        if x.__class__== tuple or x.__class__==list:
            self.X=x[0]
            self.Y=x[1]
        elif y is not None:
            self.X=x
            self.Y=y
        else:
            raise "error argument of Position"
class Piece():
    def __init__(self,x,y):
        self.actor=None
        self.terrain=None #地形
        self.ox=x
        self.oy=y
        self.position=Position(x,y)
        self.canmove=True
        self.mv=0
class Actor():
    def __init__(self,name,surface,map):
        self.name=name
        self.image=pygame.image.load(name+".png").convert_alpha()

        self.subimage=[]
        for j in range(0,4):
            line=[]
            for i in range(0,4):
                line.append(self.image.subsurface(Rect(i*32,j*48,32,48)))
            self.subimage.append(line)
        self.direction=Direction.DOWN
        self.dest_ox=0
        self.dest_oy=0
        self.x=0  # 实际坐标，画图的时候用，左上角为基准
        self.y=0
        self.ox=0 # 格子坐标
        self.oy=0
        self.surface=surface
        self.order=0
        self.animal_count=0
        self.state=Actor_State.WAIT
        self.map=map
        self.move_speed=60 # 单位 像素/s
        # 帧率 40
    def update(self):

        if self.state==Actor_State.WALKING:
            if self.direction == Direction.DOWN:
                self.y += self.move_speed/40
            elif  self.direction == Direction.UP:
                self.y -= self.move_speed/40
            elif self.direction == Direction.RIGHT:
                self.x+=self.move_speed/40
            elif self.direction == Direction.LEFT:
                self.x-=self.move_speed/40
            self.update_oxoy()
            self.check_arrive()
        if self.state==Actor_State.WAIT :
            self.animal_count+=1
            if self.animal_count>10:
                self.order+=1
                self.order %= 4
                self.animal_count=0
        self.surface.blit(self.subimage[self.direction.value][self.order], (self.x, self.y))



    def update_oxoy(self):
        self.ox=int(self.x/32)
        self.oy=int((self.y+16)/32)

    def check_arrive(self):
        if self.direction==Direction.UP:
            if abs(self.dest_oy*32-16-self.y)>3:
                return False
        elif self.direction==Direction.LEFT:
            if abs(self.dest_ox*32-self.x)>3:
                return False
        else:
            if self.ox!=self.dest_ox or self.oy!=self.dest_oy:
                return False

        self.state = Actor_State.WAIT
        self.set_position(self.ox,self.oy) # 校准一下位置，因为位置会有一点误差
        #print("ox:%d oy:%d x；%d y:%d dest_ox:%d dest_oy:%d" % (self.ox, self.oy, self.x, self.y,self.dest_ox,
                                                                  # self.dest_oy))

    def set_position(self,ox,oy):
        self.ox=ox
        self.oy=oy
        self.x = self.ox * 32
        self.y = self.oy * 32 - 16
        self.dest_ox=ox
        self.dest_oy=oy

    def walk(self,direction,distance):
        #print("ox:%d oy:%d x；%d y:%d dest_ox:%d dest_oy:%d" % (self.ox, self.oy, self.x, self.y, self.dest_ox,
                                                              # self.dest_oy))
        self.state=Actor_State.WALKING
        self.direction=direction
        if self.direction==Direction.DOWN:
            self.dest_oy=self.oy+distance
        elif self.direction==Direction.UP:
            self.dest_oy=self.oy-distance
        elif self.direction==Direction.LEFT:
            self.dest_ox=self.ox-distance
        elif self.direction==Direction.RIGHT:
            self.dest_ox=self.ox+distance
        self.map.move_actor(self.dest_ox,self.dest_oy,self.ox,self.oy)

    def walk_down(self,distance):
        self.walk(Direction.DOWN,distance)

    def walk_left(self,distance):
        self.walk(Direction.LEFT,distance)

    def walk_right(self,distance):
        self.walk(Direction.RIGHT,distance)
    def walk_up(self,distance):
        self.walk(Direction.UP,distance)


class Party():
    def __init__(self):
        self.data=[]

    def append(self,actor):
        return self.data.append(actor)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key]=value
class Map():
    def __init__(self,width,height,screen):
        self.map_data=[]
        for y in range(0,height):
            line=[]
            for x in range(0,width):
                line.append(Piece(x,y))
            self.map_data.append(line)

        self.screen=screen
        self.actors=[]
        self.test=[]

    def background_update(self):
        pygame.draw.rect(self.screen, (100, 200, 0), ((0, 0), (640, 480)))
        width=self.screen.get_width()
        height=self.screen.get_height()

        for i in range(0,width,32):
            pygame.draw.line(self.screen, (0, 0, 0), (i, 0), (i, height))
        for i in range(0,height,32):
            pygame.draw.line(self.screen,(0,0,0),(0,i),(width,i))

    def add_actor(self,actor,ox,oy):
        self.actors.append(actor)
        self.map_data[oy][ox].actor=actor
        self.map_data[oy][ox].canmove=False
        actor.set_position(ox,oy)

    def move_actor(self,dest_ox,dest_oy,ox,oy):
        self.map_data[dest_oy][dest_ox].actor=self.map_data[oy][ox].actor
        self.map_data[oy][ox].actor = None
        self.map_data[oy][ox].canmove=True

    def get_actor(self,ox,oy):
        return self.map_data[oy][ox].actor

    def can_move(self,ox,oy):
        return self.map_data[oy][ox].canmove

    def get_move_list(self,ox,oy,move):
        start_point=self.map_data[oy][ox]
        start_point.mv=move
        wait_to_extend=[]
        extended=[]

        path=[]
        wait_to_extend.append(start_point)

        off_x={Direction.DOWN:0,Direction.LEFT:-1,Direction.RIGHT:1,Direction.UP:0}
        off_y={Direction.DOWN:1,Direction.LEFT:0,Direction.RIGHT:0,Direction.UP:-1}
        while len(wait_to_extend)>0:
            extending_point=wait_to_extend.pop(0) # 不能从末尾弹出，因为必须保证搜寻是从一条路径上找的
            print("从待拓展区取出一个点，坐标为 %d %d" %(extending_point.ox,extending_point.oy))
            extended.append(extending_point)
            for direction in Direction:
                # 往四个方向开始拓展

                temp_ox=extending_point.ox+off_x[direction]
                temp_oy=extending_point.oy+off_y[direction]
                temp=self.map_data[temp_oy][temp_ox]
                temp.mv=extending_point.mv-1
                print("现在开始拓展"+str(direction)+" %d %d 行动力还剩：%d" %(temp.ox,temp.oy,temp.mv))
                ## 检测该点是否正常
                if  temp.mv<0:
                    print("行动力不足，跳出")
                    continue

                if temp not in extended:
                    wait_to_extend.append(temp)
                else:
                    print("该点已拓展过，跳出")
                    continue
        self.test=extended
        for i in self.test:
            print(i.ox,i.oy)

    def sprite_update(self):
        for actor in self.actors:
            actor.update()
        for i in self.test:
            pygame.draw.rect(self.screen,(0,255,255),(i.ox*32,i.oy*32,32,32))
        '''
        for i in self.map_data:
            for j in i:
                if j.actor is not None:
                    self.draw_actor(j.x,j.y,j.actor)
                    '''


    def draw_actor(self,x,y,actor):
        self.screen.blit(actor.subimage[0][0], (x*32, y*32-16))
class Cursor():
    def __init__(self,surface):
        self.cursor=pygame.Surface((32,32),flags=SRCALPHA, depth=32).convert_alpha()
        pygame.draw.rect(self.cursor, (255, 255, 255), Rect(0, 0, 30, 30), 2)
        self.surface=surface
        self.mouse_x=0
        self.mouse_y=0
        self.choosed=False
        self.choose_x=0
        self.choose_y=0
        self.choose_cursor=pygame.Surface((32,32),flags=SRCALPHA, depth=32).convert_alpha()

        self.ox=0
        self.oy=0
        pygame.draw.rect(self.choose_cursor, (255, 0, 0), Rect(0, 0, 30, 30), 2)

    def mouse_adjust(self,mouse_x,mouse_y):
        self.ox=int(mouse_x/32)
        self.oy=int(mouse_y/32)
        mouse_x -= mouse_x % 32
        mouse_y -= mouse_y % 32
        self.mouse_x=mouse_x
        self.mouse_y=mouse_y


    def update(self,mouse_x,mouse_y):
        self.mouse_adjust(mouse_x,mouse_y)
        self.surface.blit(self.cursor,(self.mouse_x,self.mouse_y))
        if self.choosed:
            self.surface.blit(self.choose_cursor, (self.choose_x, self.choose_y))

    def choose(self,flag):
        if flag==True:
            self.choosed=True
            self.choose_x=self.mouse_x
            self.choose_y=self.mouse_y
        else:
            self.choosed=False

    def get_ox_oy(self):
        return self.ox,self.oy
class Menu():
    def __init__(self,item_list,parent_surface):
        self.data=item_list
        self.x=0
        self.y=0 # 真实坐标
        self.show=False
        self.font=pygame.font.SysFont("fangsong",25)
        self.text_surfaces=[]

        self.surface=parent_surface
        self.back_surface=pygame.Surface((80,len(self.data)*25))
        self.menu_choose=0

        for i in self.data:
            self.text_surfaces.append(self.font.render(i,True,(0,0,0)))
        #self.menu_cursor=pygame.Surface(80,len(self.data)*25, flags=SRCALPHA, depth=32).convert_alpha()


    def update_background(self):
        self.back_surface.fill((255, 255, 255))
    def display(self,flag,x=0,y=0):
        if flag:
            self.show=True
            self.x=x+30
            self.y=y
        else:
            self.show=False

    def click(self,mouse_x,mouse_y,flag):
        if self.show == False:
            if flag==True:
                self.display(True,mouse_x,mouse_y)
                 # 只有当当前菜单没有显示时，才会检测flag来判断是否显示
        else:
            # 即现在菜单已经显示了
            if self.menu_choose<0 or self.menu_choose >len(self.data)-1: #超出范围
                self.display(False)
            else:
                print(self.menu_choose)





    def update(self,mouse_x,mouse_y):
        if not self.show:
            return
        for i,item in enumerate(self.text_surfaces):
            self.back_surface.blit(item,(0,i*25))
        self.surface.blit(self.back_surface, (self.x, self.y))
        self.update_background()
        self.menu_choose=int((mouse_y-self.y)/25)
        pygame.draw.rect(self.back_surface, (200, 100, 100), (0, self.menu_choose * 25, 78, 25), 2)

class System():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480), 0, 32)
        # 创建了一个窗口
        pygame.display.set_caption("Hello, World!")

        self.font = pygame.font.SysFont("fangsong", 60)
        self.menu = Menu(["移动", "攻击", "休息"],self.screen)
        self.map= Map(int(640 / 32), int(480 / 32), self.screen)

        self.cursor=Cursor(self.screen)

        self.party1=[]
        self.party2=[]
        self.actor_init()
        self.clock=pygame.time.Clock()

    def actor_init(self):
        self.nurse=Actor("nurse",self.screen,self.map)
        self.map.add_actor(self.nurse,5,5)


    def game_run(self):
        while True:
            # 游戏主循环
            self.map.background_update()

            x, y = pygame.mouse.get_pos()
            self.cursor.update(x,y)
            for event in pygame.event.get():
                if event.type == QUIT:
                    # 接收到退出事件后退出程序
                    exit()
                elif event.type == MOUSEBUTTONDOWN:
                    if not self.menu.show:
                        self.cursor.choose(True)
                    ox,oy=self.cursor.get_ox_oy()
                    if self.map.get_actor(ox,oy):
                        self.menu.click(x, y,True)
                        self.map.get_move_list(ox,oy,3)
                    else:
                        self.menu.click(x, y,False)
                    #self.map.actors[0].walk_up(1)

                    #print(self.map.map_data[self.cursor.oy][self.cursor.ox].actor)
            self.clock.tick(40)
            self.menu.update(x,y)

            self.map.sprite_update()

            pygame.display.update()
            # 刷新一下画面

S=System()
S.game_run()