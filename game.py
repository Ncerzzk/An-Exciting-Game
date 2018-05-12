from Character import *

import unittest

class Game:
    def __init__(self):
        Warrior_Normal_Attack = Skill("普通攻击", 1, 20,0)
        Magic_Attack = Skill("法术攻击", 2, 40,20)
        Cure = Skill("恢复", 2, -30,30)

        self.Characters=[]
        self.Map=Map(8,8)
        self.Characters.append(Character("战士", 100, 0, [Warrior_Normal_Attack], [0, 0], [Move, Attack, Rest],1,2,"▲",self.Map))

        self.Characters.append(Character("法师", 50, 100, [Magic_Attack], [0, 1], [Move, Attack, Rest],1,1,"✦",self.Map))
        self.Characters.append(Character("圣职者", 50, 100, [Cure], [0, 2], [Move, Attack, Rest],1,1,"✞",self.Map))

        self.Characters.append(Character("战士", 100, 0, [Warrior_Normal_Attack], [7, 7], [Move, Attack, Rest], 2,2,"▲",self.Map))
        self.Characters.append(Character("法师", 50, 100, [Magic_Attack], [7, 6], [Move, Attack, Rest], 2,1,"✦",self.Map))
        self.Characters.append(Character("圣职者", 50, 100, [Cure], [7, 5], [Move, Attack, Rest], 2,1,"✞",self.Map))

        """
        self.Characters.append(
            Character("战士", 100, 0, [Warrior_Normal_Attack], [0, 5], [Move, Attack, Rest], 2, 2, "▲",self.Map))
        self.Characters.append(Character("法师", 50, 100, [Magic_Attack], [4, 1], [Move, Attack, Rest], 2, 1, "✦",self.Map))
        """
        self.Map.update_all(self.Characters)
        while not self.is_game_over():
            result=Think1(self.Characters)
            for c in result:
                self.do(c,c.Actions,1)
            if self.is_game_over():
                break
            result=Think2(self.Characters)
            for c in result:
                self.do(c,c.Actions,2)
            x=input("next:") #暂停
        print("游戏结束")

    def do(self,character,actions,party_id):
        if(character.Party_ID!=party_id):
            print("该角色你无法控制！")
            return None

        # 判断行动点数是否足够
        ap=character.Action_Point
        real_actions=[]
        for action in actions:
            if ap>=action.AP:
                ap-=action.AP
                real_actions.append(action)
            else:
                print("%d 的 %s 由于行动点数不足，无法执行 %s" %(party_id,character.Name,action))

        for times,action in enumerate(real_actions):
            print("队伍 %d 的 %s，动作是%s" %(character.Party_ID,character.Name,str(action)))
            if action.__class__ == Move:
                if character.Position.distance(action.Dest_Position) > character.MV:
                    print("超出移动距离，移动无效")
                    continue  # 超出移动距离，无效
                else:
                    print("移动目标是 x:%d y:%d" % (action.Dest_Position.X,action.Dest_Position.Y))
                    character.Position = action.Dest_Position
                    self.Map.move(character)
            elif action.__class__ == Attack:
                if character.can_use_skill(action.Skill):  # MP 是否足够
                    if character.distance(action.Target) > action.Skill.Distance:
                        print("超出攻击距离，攻击无效")
                        continue  # 超出攻击距离，无效
                    else:

                        action.Target.update_HP(-action.Skill.Damage)
                        character.update_MP(action.Skill.Consume)
                        print("攻击目标是 队伍%d 的 %s,攻击后，目标HP为%d" % (
                        action.Target.Party_ID, action.Target.Name, action.Target.HP))
                        if not action.Target.is_alive():
                            self.Characters.remove(action.Target)
                            self.Map.remove(action.Target)
                            # 还得检测角色是否死亡，如果死亡应该踢出队伍
            elif action.__class__ == Rest:
                if times == 0:  # 判断是否啥都不干直接休息，如果是，恢复
                    character.HP += character.MAX_HP * 0.1
                    character.MP += character.MAX_MP * 0.1
                    print("休息，当前HP为 %d" % character.HP)
                break  # 休息了，直接跳出

            self.Map.display()
        character.Actions.clear()



    def display(self):
        result=[]
        for i in range(0,8):
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


Party_Dic={}
Ocupation_Dic={}

def Init_Dic(cl):
    Party_Dic[1]=[]
    Party_Dic[2]=[]

    Ocupation_Dic["warrior"]=[]
    Ocupation_Dic["caster"]=[]
    Ocupation_Dic["nurse"]=[]
    for i in cl:
        if i.Party_ID==1:
            Party_Dic[1].append(i)
        else:
            Party_Dic[2].append(i)

        if i.Name=="战士":
            Ocupation_Dic["warrior"].append(i)
        elif i.Name=="法师":
            Ocupation_Dic["caster"].append(i)
        elif i.Name=="奶妈":
            Ocupation_Dic["nurse"].append(i)

def Get_Party_Characters(party_id):
    return Party_Dic[party_id]

def Get_Occupation_Characters(occupation):
    return Ocupation_Dic[occupation]

def Get_Character(party_id,occupation):
    return list(set(Party_Dic[party_id]).intersection(set(Ocupation_Dic[occupation])))[0]

def Think1(cl):
    Init_Dic(cl)
    result=[]
    warrior=cl[0]
    warrior.attack(cl[1])
    result.append(warrior)
    return result


def Think2(cl):
    Init_Dic(cl)

    my_characters=Get_Party_Characters(2)
    enemys=Get_Party_Characters(1)

    my_warrior=Get_Character(2,"warrior")
    my_caster=Get_Character(2,"caster")
#    my_nurse=Get_Character(2,"nurse")

    warrior_can_attack_list=[]
    caster_can_attack_list=[]

    enemy_min_hp=100
    enemy_target=None
    for enemy in enemys:
        if enemy.Position.distance(my_warrior.Position) <= 1 :
            warrior_can_attack_list.append(enemy)
        elif enemy.Position.distance(my_caster.Position)<=2 :
            caster_can_attack_list.append(enemy)
        if enemy.HP<=enemy_min_hp:
            enemy_min_hp=enemy.HP
            enemy_target=enemy  #找血最少的那个，干他丫的


    min_distance=100
    if len(warrior_can_attack_list)<1:  #战士无目标
        t_position,min_distance=my_warrior.find_way(enemy_target.Position)
        print(t_position.X,t_position.Y)
        my_warrior.move(t_position.X,t_position.Y)
        if min_distance <=1:
            my_warrior.attack(enemy_target)
    else:
        my_warrior.attack(warrior_can_attack_list[0])

    if len(caster_can_attack_list)<1:
        t_position,min_distance=my_caster.find_way(enemy_target.Position)
        my_caster.move(t_position.X,t_position.Y)
        if min_distance <=2:
            my_caster.attack(enemy_target)
    else:
        my_caster.attack(enemy_target)
        
    result=[]
    result.append(my_warrior)
    result.append(my_caster)
    return result
Game()