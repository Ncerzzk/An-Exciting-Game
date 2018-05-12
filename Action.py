from Map import  *

class Action:
    def __init__(self):
        pass

    def __str__(self):
        return str(__class__.__name__)

class Move(Action):
    AP=4
    def __init__(self,*args):
        if(len(args)>1):
            self.Dest_Position=Position(args[0],args[1])
        else:
            self.Dest_Position=args[0]

    def __str__(self):
        return str(__class__.__name__)

class Rest(Action):
    AP=0
    def __init__(self):
        pass
    def __str__(self):
        return str(__class__.__name__)

class Attack(Action):
    AP=6
    def __init__(self,target_character,skill):
        self.Target=target_character
        self.Skill=skill
    def __str__(self):
        return str(__class__.__name__)


