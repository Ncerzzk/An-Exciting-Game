from Action import *
from Map import *

import  unittest

class Character:
    Character_Num=0
    def __init__(self,name,hp,mp,skill_list,position,action_list,party_id,move,symbol,map=None):
        self.Name=name
        self.HP=hp
        self.MP=mp
        self.MAX_HP=hp
        self.MAX_MP=mp
        self.Skill_List=skill_list
        if(position.__class__==Position):
            self.Position=position
        elif(position.__class__==list or position.__class__==tuple):
            self.Position=Position(position[0],position[1])
        self.Action_List=action_list
        self.Action_Point=10
        self.Party_ID=party_id
        self.MV=move
        self.Symbol=symbol
        Character.Character_Num = Character.Character_Num + 1
        self.ID=Character.Character_Num
        self.Actions=Actions()
        self.Map=map

    def move(self,x,y):
        self.Actions.append(Move(x,y))

    def attack(self,target,skill=None):
        if not skill:
            self.Actions.append(Attack(target,self.Skill_List[0]))
        else:
            pass #因为暂时只有一个技能，这里先不实现

    def rest(self):
        self.Actions.append(Rest())

    def find_way(self,pb):
        if pb.__class__==Character:
            return self.Map.find_way(self.Position, pb.Position, self.MV)
        else:
            return self.Map.find_way(self.Position,pb,self.MV)

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
        if self.MP>=skill.Consume:
            return True
        else:
            print("无法使用技能")
            return False


    def is_alive(self):  #判断是否存活
        if self.HP>0 :
            return True
        else:
            print("角色死亡")
            return False

    def distance(self,target_character):
        return self.Position.distance(target_character.Position)

class Skill:
    def __init__(self,name,distance,damage,consume):
        self.Name=name
        self.Distance=distance
        self.Damage=damage
        self.Consume=consume

class Actions():
    def __init__(self,action_list=None):
        if action_list:
            self.Action_List=action_list
        else:
            self.Action_List=[]
    def __iter__(self):

        return iter(self.Action_List)
    def __len__(self):
        return len(self.Action_List)

    def __next__(self):
        return next(self.Action_List)
    def __getitem__(self, item):
        if item>=len(self.Action_List):
            raise IndexError("out of index")
        return self.Action_List[item]

    def append(self,item):
        self.Action_List.append(item)

    def clear(self):
        self.Action_List.clear()

'''
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
    def __len__(self):
        return len(self.Action_List)

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
        self.AP_Bin &= ~(1<<ap)

class Test_Character_Action(unittest.TestCase):
    def test_s(self):
        c=Character("战士", 100, 0, [], [0, 0], [Move, Attack, Rest],1,2,"▲")
        warrior_actions=Character_Action(c,[Move(1,2),Move(1,2)])
        self.assertEqual(len(warrior_actions),1)  ## 测试AP
        self.assertEqual(warrior_actions[0].__class__,Move)  #test_get_item
        for i in warrior_actions:
            self.assertEqual(i.__class__,Move)   # 测试迭代





def Think(all_list):
    pass
'''




