import math
class Position:
    def __init__(self,x,y):
        self.X=x
        self.Y=y

    def distance(self,pointB):
        result=pow(self.X-pointB.X,2)+pow(self.Y-pointB.Y,2)
        result=math.sqrt(result)
        return result

class Map:
    def __init__(self,width,height):
        self.Width=width
        self.Height=height
        self.Martix=[[0]*width for i in range(0,height)]
        self.Dic={}

    def __getitem__(self, item):   # item 是一个Position对象
        return self.Martix[item.Y][item.X]


    def update_all(self,characters):
        for i in characters:
            self.Martix[i.Position.Y][i.Position.X]=i.ID
            self.Dic[i.ID]=Position

    def update(self,character):
        self[character.Position]=character.ID
        self[self.Dic[character.ID]]=0

    def can_move(self,x=None,y=None,position=None):
        temp_x=0
        temp_y=0
        if not x and not position:
            raise "no argument!"
        elif x:
            temp_x=x
            temp_y=y
        elif position:
            temp_x=position.X
            temp_y=position.Y
        if self.Map[temp_y][temp_x]==0:
            return True
        else:
            return False

