from Map import  *

class Action:
    def __init__(self):
        pass

class Move(Action):
    AP=4
    def __init__(self,*args):
        if(len(args)>1):
            self.Dest_Position=Position(args[0],args[1])
        else:
            self.Dest_Position=args[0]

class Rest(Action):
    AP=0
    def __init__(self):
        pass

class Attack(Action):
    AP=6
    def __init__(self,target_character,skill):
        self.Target=target_character
        self.Skill=skill



