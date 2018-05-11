from Character import *

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

        self.Map.update_all(self.Characters)
        while not self.is_game_over():
            self.do(Think1(self.Characters),1)
            self.do(Think2(self.Characters),2)

            self.display()
            x=input("t")

    def do(self,character_actions,party_id):
        for character_action in character_actions:
            character=character_action.Character
            if character.Party_ID!=party_id: # 输出的动作不是自己队伍的角色，即控制了别人的角色，无效
                return None
            for times,action in enumerate( character_action.Action_List):
                if action.__class__==Move:
                    if character.Position.distance(action.Dest_Position)>character.MV:
                        continue #超出移动距离，无效
                    else:
                        character.Position=action.Dest_Position
                        self.Map.move(character)
                elif action.__class__==Attack:
                    if character.can_use_skill(action.Skill): # MP 是否足够
                        if character.distance(action.Target) > action.Skill.Distance:
                            continue #超出攻击距离，无效
                        else:
                            action.Target.update_HP(-action.Skill.Damage)
                            character.update_MP(action.Skill.Consume)
                            if not action.Target.is_alive():
                                self.Characters.remove(action.Target)
                                self.Map.remove(action.Target)
                                # 还得检测角色是否死亡，如果死亡应该踢出队伍

                elif action.__class__==Rest:
                    if times==0: #判断是否啥都不干直接休息，如果是，恢复
                        character.HP+=character.HP*0.1
                        character.MP+= character.MP * 0.1
                    break #休息了，直接跳出
                self.display()

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

def Think1(cl):
    result=[]
    warrior_action=Character_Action(cl[0],[Move(Position(1,1)),Rest])

    result.append(warrior_action)
    return result

Game()