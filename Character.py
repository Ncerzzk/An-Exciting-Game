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
            self.position=Position(position[0],position[1])
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
        self.Action_List=[]

        if not character.is_alive():
            self.Action_List=[]

        self.AP_Bin=(1<<Move.AP) |(1<<Attack.AP) |(1<<Rest.AP)
        ap=character.Action_Point     # 剩余的行动点数
        for action in action_list:
            if (not self.is_done(action.AP)) and ap>action.AP:
                self.Action_List.append(action)
                ap=ap-action.AP
                self.set_done(action.AP)


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
    result=[]
    warrior_action=Character_Action(a,[Move(4,5),Attack(b),Rest])

    result.append(warrior_action)
    return result

class Game:
    def __init__(self):
        Warrior_Normal_Attack = Skill("普通攻击", 1, 20,0)
        Magic_Attack = Skill("法术攻击", 2, 40,20)
        Cure = Skill("恢复", 2, -30,30)

        self.Characters=[]
        self.Map=Map(8,8);
        self.Characters.append(Character("战士", 100, 0, [Warrior_Normal_Attack], [0, 0], [Move, Attack, Rest],1,2,"▲"))
        self.Characters.append(Character("法师", 50, 100, [Magic_Attack], [0, 1], [Move, Attack, Rest],1,1,"✦"))
        self.Characters.append(Character("圣职者", 50, 100, [Cure], [0, 2], [Move, Attack, Rest],1,1,"✞"))

        self.Characters.append(Character("战士", 100, 0, [Warrior_Normal_Attack], [7, 7], [Move, Attack, Rest], 2,2,"▲"))
        self.Characters.append(Character("法师", 50, 100, [Magic_Attack], [7, 6], [Move, Attack, Rest], 2,1,"✦"))
        self.Characters.append(Character("圣职者", 50, 100, [Cure], [7, 5], [Move, Attack, Rest], 2,1,"✞"))

        while not self.is_game_over():
            Think1(self.Characters)
            Think2(self.Characters)

            self.display()

    def do(self,character_actions):
        character=character_actions.Character
        for times,action in character_actions:
            if action.__class__==Move:
                if character.position.distance(action.Dest_Position)>character.MV:
                    continue #超出移动距离，无效
                else:
                    character.Position=action.Dest_Position
                    self.Map.update(character_actions.Character)
            elif action.__class__==Attack:
                if character.distance(action.Target) > action.Skill.Distance:
                    continue #超出攻击距离，无效
                else:
                    action.Target.HP-=action.Skill.Damage #更新HP 这里最好调用类里的方法
                    character.MP-=action.Skill.Consume #更新MP 同理
                    # 还得检测角色是否死亡，如果死亡应该踢出队伍

            elif action.__class__==Rest:
                if times==0: #判断是否啥都不干直接休息，如果是，恢复
                    character.HP+=character.HP*0.1
                    character.MP+= character.MP * 0.1
                break #休息了，直接跳出


    def display(self):
        result=[]
        for i in range(0,9):
            result.append(' '*8)
        for character in self.Characters:
            result[character.Position.Y][character.Position.X]=character.Symbol
        for i in result:
            print(i)

    def is_game_over(self):
        if len(self.Characters)<=3:
            temp_party_id=None
            for i in self.Characters:
                if not temp_party_id:
                    temp_party_id=i.Party_ID
                else:
                    if temp_party_id != i.Party_ID:
                        break
            else:
                return True
        return False



