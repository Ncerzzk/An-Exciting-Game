from Action import *
from Map import *

class Character:
    Character_Num=0
    def __init__(self,name,hp,mp,skill_list,position,action_list,party_id,move,symbol):
        self.Name=name
        self.HP=hp
        self.MP=mp
        self.Skill_List=skill_list
        if(position.__class__==Position):
            self.Position=position
        elif(position.__class__==list):
            self.Position=Position(position[0],position[1])
        self.Action_List=action_list
        self.Action_Point=10
        self.Party_ID=party_id
        self.MV=move
        self.Symbol=symbol
        Character.Character_Num = Character.Character_Num + 1
        self.ID=Character.Character_Num

    def update_HP(self,h):
        # 更新HP
        self.HP+=h
        if self.HP<0:
            self.HP=0

    def update_MP(self,h):
        self.MP+=h
        if self.MP<0:
            self.MP=0

    def can_use_skill(self,skill):
        if self.MP>skill.Consume:
            return True
        else:
            return False


    def is_alive(self):  #判断是否存活
        if(self.HP>0):
            return True
        else:
            return False

    def distance(self,target_character):
        return self.Position.distance(target_character.Position)

class Skill:
    def __init__(self,name,distance,damage,consume):
        self.Name=name
        self.Distance=distance
        self.Damage=damage
        self.Consume=consume

class Character_Action():

    def __init__(self,character,action_list):
        self.Character=character
        self.Action_List = []
        if not character.is_alive():
            return

        self.AP_Bin=(1<<Move.AP) |(1<<Attack.AP) |(1<<Rest.AP)
        ap=character.Action_Point     # 剩余的行动点数
        for action in action_list:
            if (not self.is_done(action.AP)) and ap>action.AP:
                self.Action_List.append(action)
                ap=ap-action.AP
                self.set_done(action.AP)
    def __iter__(self):
        return iter(self.Action_List)
    def __next__(self):
        return next(self.Action_List)



    def __getitem__(self, item):
        if item>=len(self.Action_List):
            raise IndexError("out of index")
        return self.Action_List[item]


    def is_done(self,ap):   #判断该Action 是否执行过，即每回合只能做一次移动
        if (1<<ap) & self.AP_Bin :
            return False
        else:
            return True

    def set_done(self,ap):
        self.AP_Bin & ~(1<<ap)


def Think(all_list):
    pass





