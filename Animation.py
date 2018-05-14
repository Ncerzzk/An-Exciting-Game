import pygame
from pygame.locals import *


class Animation():
    def __init__(self,name,surface,play_list=None):
        self.image=pygame.image.load(name+".png").convert_alpha()
        # 素材规格 192 X 192
        self.line_count=int(self.image.get_height()/192)
        self.column_count=int(self.image.get_width()/192)
        self.subimage=[]
        for i in range(0,self.line_count):
            line=[]
            for j in range(0,self.column_count):
                print(i,j)
                line.append(self.image.subsurface(Rect(j*192,i*192,192,192)))
            self.subimage.append(line)
        self.play_list= play_list if play_list else []

        self.display=False

        self.play_order=0

        self.x=0
        self.y=0

        self.surface=surface

    def show(self,x,y):
        self.display=True
        self.x=x
        self.y=y

    def update(self):
        if not self.display:
            return None
        index=self.play_list[int(self.play_order/2)]
        sub_y=int(index/5)
        sub_x=index%5
        self.surface.blit(self.subimage[sub_y][sub_x],(self.x,self.y))
        self.play_order+=2
        if self.play_order > (len(self.play_list)-1)*2:
            self.play_order=0
            self.display=False


