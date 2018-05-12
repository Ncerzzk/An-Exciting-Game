import math

def Think1(character_list):
    warrior = character_list[0]
    magic = character_list[1]
    nurse = character_list[2]

    warrior_enemy = character_list[3]
    magic_enemy = character_list[4]
    nurse_enemy = character_list[5]

    auto_fight(warrior, warrior_enemy, warrior.MV)
    auto_fight(magic, magic_enemy, magic.MV)
    auto_fight(nurse, warrior, nurse.MV)


def judge_parallel(s1, s2):
    if s1.Position.X == s2.Position.X or s2.Position.Y == s2.Position.Y:
        if s1.Position.X == s2.Position.X:
            dis = abs(s1.Position.Y - s2.Position.Y)
            return 'X', dis
        else:
            dis = abs(s1.Position.X - s1.Position.X)
            return 'Y', dis
    else:
        return False

def can_fight(myself, target, skill):
    if myself.Position.X == target.Position.X:
        if abs(myself.Position.Y - target.Position.Y) <= skill.Distance:
            return True
        else:
            return False
    elif myself.Position.Y == target.Position.Y:
        if abs(myself.Position.X - target.Position.X) <= skill.Distance:
            return True
        else:
            return False
    else:
        return False

def auto_fight(myself, target, step_dis):

    if judge_parallel(myself, target):
        toward, dis = judge_parallel(myself, target)

        if toward == 'X':
            if can_fight(myself, target, myself.Skill_List[0]):
                myself.attack(target)
            else:
                if myself.Position.X > target.Position.X:
                    myself.move(myself.Position.X - min(dis-1, step_dis), myself.Position.Y)
                else:
                    myself.move(myself.Position.X - min(dis-1, step_dis), myself.Position.Y)

                if can_fight(myself, target, myself.Skill_List[0]):
                    myself.attack(target)

        if toward == 'Y':

            if can_fight(myself, target, myself.Skill_List[0]):
                myself.attack(target)
            else:
                if myself.Position.Y > target.Position.Y:
                    myself.move(myself.Position.X, myself.Position.Y - min(dis - 1, step_dis))
                else:
                    myself.move(myself.Position.X, myself.Position.Y - min(dis - 1, step_dis))

                if can_fight(myself, target, myself.Skill_List[0]):
                    myself.attack(target)

    else: # 在Y轴上对齐
        if myself.Position.Y < target.Position.Y:
            dis = abs(myself.Position.Y - target.Position.Y)
            myself.move(myself.Position.X, myself.Position.Y + min(step_dis, dis))
        else:
            dis = abs(myself.Position.Y - target.Position.Y)
            myself.move(myself.Position.X, myself.Position.Y - min(step_dis, dis))