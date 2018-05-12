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
        self.Matrix=[[0]*width for i in range(0,height)]
        self.Dic={}

    def search(self,position,distance):
        result=[]
        for cid in self.Dic:
            if(self.Dic[cid].distance(position)<=distance):
                result.append(cid)
        return result

    def find_way(self,pa,pb,mv):
        x_start=0 if pa.X-mv<0 else pa.X-mv
        x_end=self.Width if pa.X+mv>self.Width else pa.X+mv
        y_start=0 if pa.Y-mv<0 else pa.Y-mv
        y_end=self.Height if pa.Y+mv>self.Height else pa.Y+mv
        min_distance=1000

        for x in range(x_start,x_end+1):
            for y in range(y_start,y_end+1):
                temp_p=Position(x,y)
                temp_distance=temp_p.distance(pb)
                if temp_p.distance(pa)>mv:
                    continue
                if temp_distance<min_distance and temp_distance>0:
                    min_distance=temp_distance
                    result=temp_p
        return result,min_distance

    def __getitem__(self, item):   # item 是一个Position对象
        return self.Matrix[item.Y][item.X]

    def __setitem__(self, key, value):

        self.Matrix[key.Y][key.X]=value

    def remove(self,character):
        self.Dic.pop(character.ID)
        self.update(character.Position,0)

    def update(self,position,n):
        self[position]=n

    def update_all(self,characters):
        for i in characters:
            self.Matrix[i.Position.Y][i.Position.X]=i.ID
            self.Dic[i.ID]=i.Position

    def move(self,character):
        self.update(character.Position,character.ID)
        self.update(self.Dic[character.ID],0)
        self.Dic[character.ID]=character.Position

    def display(self):
        for line in self.Matrix:
            print(line)

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

