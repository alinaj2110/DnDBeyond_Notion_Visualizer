from enum import Enum


class C_Actions(Enum):
    ACTION = "action"
    BONUS_ACTION = "bonus action"
    REACTION = "reaction"
    OTHER = "other"

class AllActions:
    def __init__(self, combat_stats_element, spellblock = None) -> None:
        self.combat_stats_element = combat_stats_element
        action_stats, bonus_stats, react_stats, others = self.__extract_all_stat_elements(combat_stats_element)
        self.actions = Action(action_stats)
        self.bonus_actions = BonusAction(bonus_stats)
        self.reactions = Reactions(react_stats)
        self.spells = Spells(spellblock)

    def __extract_type(self, title:str) -> C_Actions:
        for e in C_Actions:
            if title.lower().startswith(e.value):
                return e
        raise KeyError("No action type found")
    
    def __extract_all_stat_elements(self, stat_element):
        return ("action","bonus","reaction","others")


class Action:
    def __init__(self, stats) -> None:
        pass
    

class BonusAction:
    def __init__(self, stats) -> None:
        pass

class Reactions:
    def __init__(self, stats) -> None:
        pass

class Spells:
    def __init__(self, spellblock) -> None:
        self.spellblock = spellblock

        
