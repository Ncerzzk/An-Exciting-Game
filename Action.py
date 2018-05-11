class Action:
    def __init__(self):
        pass

class Move(Action):
    AP=4
    def __init__(self,position):
        self.Dest_Position=position

class Rest(Action):
    AP=0
    def __init__(self):
        pass

class Attack(Action):
    AP=6
    def __init__(self,target_character,skill):
        self.Target=target_character
        self.Skill=skill



