from enum import Enum
from core.utils import *


class C_Actions(Enum):
    ACTION = "action"
    BONUS_ACTION = "bonus action"
    REACTION = "reaction"
    OTHER = "other"

class AllActions:
    def __init__(self) -> None:
        pass

    def __extract_type(self, content:str) -> C_Actions:
        for e in C_Actions:
            if content.lower().startswith(e.value):
                return e
        raise KeyError("No action type found")
    
    async def extract_all_stat_elements(self, combat_stats_element, spellblock = None):
        self.combat_stats_element = combat_stats_element
        self.spells = Spells(spellblock)

        #Get all the sections of the actions
        combat_action_list = await combat_stats_element.querySelectorAll(".ct-actions-list")
        for comb_action in combat_action_list:
            # if DEBUG_ENABLED: await highlight_element(comb_action, page)
            text = await get_text_content(element=comb_action)
            typ = self.__extract_type(text)
            match typ:
                case C_Actions.ACTION:
                    self.actions = Action(comb_action)
                case C_Actions.BONUS_ACTION:
                    self.bonus_actions = BonusAction(comb_action)
                case C_Actions.REACTION:
                    self.reactions = Reactions(comb_action)
                case C_Actions.OTHER:
                    self.others = comb_action

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

        
