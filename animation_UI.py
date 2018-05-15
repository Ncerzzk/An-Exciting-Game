import pygame
from pygame.locals import *

from enum import Enum

class Mouse_Item():
    def __init__(self,item,parent_surface,position,h_w=None):
        self.item=item #item 是要显示的surface对象

        self.x=position[0]
        self.y=position[1]
        if h_w: # 若不指定高度和宽度，则使用Item 这个Surface对象的高度和宽度
            self.width=h_w[1]
            self.height=h_w[0]
        else:
            self.width=self.item.get_width()
            self.height=self.item.get_height()
        self.parent_surface=parent_surface
        self.surface=pygame.Surface((self.width,self.height)).convert_alpha()


        self.hover=False

    def hover_display(self):
        pass

    def noram_display(self):
        pass

    def update(self,mouse_x,mouse_y):
        off_x,off_y=self.surface.get_abs_offset()
        rect=Rect(off_x,off_y,self.width,self.height)
        if rect.collidepoint(mouse_x,mouse_y):
            self.hover_display()
            self.hover=True
        else:
            self.noram_display()
            self.hover=False
        self.surface.blit(self.item, (0, 0))
        self.parent_surface.blit(self.surface,(self.x,self.y))

class String_Mouse_Item(Mouse_Item):
    def __init__(self,string,parent_surface,position,font_size=20,font=None,font_color=None,h_w=None):
        self.string=string
        self.font_size = font_size
        if not font:
            self.font=pygame.font.SysFont("fangsong",self.font_size)
        else:
            self.font=font
        if not font_color:
            self.font_color=(0,0,0)
        else:
            self.font_color=font_color
        self.text_surface = self.font.render(self.string, True, self.font_color)
        self.back_normal_color=(255,255,255)
        self.back_hover_color=(150,100,100)
        super(String_Mouse_Item,self).__init__(self.text_surface,parent_surface,position,h_w)

    def hover_display(self):
        self.surface.fill(self.back_hover_color)

    def noram_display(self):
        self.surface.fill(self.back_normal_color)

class Bottom_Menu():
    def __init__(self,name):
        self.display_image_num=5
        self.image=pygame.image.load(name+".png").convert_alpha()
        row_count=int(self.image.get_height()/192)
        column_count=int(self.image.get_width()/192)
        self.subimage=[]
        for j in range(0,row_count):
            for i in range(0,column_count):
                self.subimage.append(self.image.subsurface(Rect(i*192,j*192,192,192)))
        if len(self.subimage)>5:
            self.scroll=True
        else:
            self.scroll=False
class Scroll():
    def __init__(self,h_w,length,parent_surface,mouse_inform):
        self.length=length
        self.parent_surface=parent_surface
        self.width=h_w[0]
        self.height=h_w[1]
        self.surface=pygame.Surface((self.width,self.height))

        self.background_color = (100, 155, 222)
        self.scroll=pygame.Surface((50,30))
        self.scroll.fill(self.background_color)

        self.mouse_inform=mouse_inform
        self.clicked=False # 被点击

        self.display_x=0
        self.display_y=0

        self.type=0
        self.now_result=0

        self.scroll_x=0
        self.scroll_y=0

    def update(self):
        self.surface.fill((255, 255, 255))
        if self.mouse_inform.state==Mouse_State.MOUSE_DOWN:
            if self.clicked==True: # 如果已经被点击了，且此时鼠标按下，那么不管鼠标坐标如何了，直接拉动滚动条
                if self.type==0: # 横
                    self.scroll_y=0
                    sub_x=self.mouse_inform.x-self.display_x
                    percent=sub_x/self.width
                    self.scroll_x=percent*self.width
                else:
                    self.scroll_x=0
                    sub_y=self.mouse_inform.y-self.display_y
                    percent=sub_y/self.height
                    self.scroll_y=percent*self.height
                self.surface.blit(self.scroll, (self.scroll_x, self.scroll_y))
                self.now_result = int(percent * self.length)
            else:
                # 如果是刚按下鼠标，那么检测鼠标是否点到了滚动条上，如果是，将clicked 改变值
                rect=Rect(self.scroll_x,self.scroll_y,self.scroll.get_width(),self.scroll.get_height())
                if rect.collidepoint(self.mouse_inform.x,self.mouse_inform.y):
                    self.clicked=True
                self.surface.blit(self.scroll, (self.now_result / self.length * self.width, 0))
        elif self.mouse_inform.state==Mouse_State.MOUSE_UP:
            if self.clicked:
                self.clicked=False
                if self.type==0:
                    self.scroll_x=self.now_result / self.length * self.width
                    self.scroll_y=0
                else:
                    self.scroll_y=self.now_result / self.length*self.height
                    self.scroll_x=0
            self.surface.blit(self.scroll, (self.scroll_x, self.scroll_y))
        self.parent_surface.blit(self.surface,(self.display_x,self.display_y))






class Mouse_State(Enum):
    MOUSE_DOWN=1
    MOUSE_UP=2
class Mouse_Inform():
    def __init__(self):
        self.state=Mouse_State.MOUSE_UP
        self.x=0
        self.y=0

    def change_state(self,state,x,y):
        self.state=state
        self.x=x
        self.y=y

    def mouse_down(self,x,y):
        self.change_state(Mouse_State.MOUSE_DOWN,x,y)

    def mouse_up(self,x,y):
        self.change_state(Mouse_State.MOUSE_UP,x,y)

    def set_mouse(self,x,y):
        self.x=x
        self.y=y




class Animation_UI():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480), 0, 32)
        # 创建了一个窗口
        pygame.display.set_caption("Animation_GUI")
       # self.menu=Mouse_Item("测试",self.screen,(0,0))
        self.menu=String_Mouse_Item("测试",self.screen,(0,0))
        self.mouse=Mouse_Inform()
        self.scroll=Scroll((640,30),10,self.screen,self.mouse)

    def run(self):
        while True:
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == QUIT:
                    # 接收到退出事件后退出程序
                    exit()
                elif event.type==MOUSEBUTTONDOWN:
                    self.mouse.mouse_down(x,y)
                elif event.type==MOUSEBUTTONUP:
                    self.mouse.mouse_up(x,y)
            self.mouse.set_mouse(x,y)
            self.scroll.update()
            self.menu.update(x,y)
            pygame.display.update()


Animation_UI().run()
