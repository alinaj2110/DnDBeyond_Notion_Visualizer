from enum import Enum
from core.utils import *
from core.Singleton import *


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
            if shared_data.debug_enabled : await highlight_element(comb_action)
            text = await get_text_content(element=comb_action)
            typ = self.__extract_type(text)
            match typ:
                case C_Actions.ACTION:
                    self.actions = Action(comb_action)
                    await self.actions.parse_contents()
                case C_Actions.BONUS_ACTION:
                    self.bonus_actions = BonusAction(comb_action)
                    await self.bonus_actions.parse_contents()
                case C_Actions.REACTION:
                    self.reactions = Reactions(comb_action)
                    await self.reactions.parse_contents()
                case C_Actions.OTHER:
                    self.others = comb_action

class Section:
    def __init__(self, stats) -> None:
        self.stats_element = stats
        self.basic_activatable = None
        self.activatables = {}
    
    async def parse_activatables(self, activatable_elements):
        '''
        activatable
        |- ct-feature-snippet__heading
        |- ct-feature-snippet__content
            |- ddbc-snippet  ddbc-snippet--parsed
        '''
        for activatable in activatable_elements:
            if shared_data.debug_enabled : await highlight_element(activatable)
            feature_name = str(await get_text_content(await activatable.querySelector(".ct-feature-snippet__heading"))).strip()
            feature_description = await get_text_content(await activatable.querySelector(".ct-feature-snippet__content .ddbc-snippet.ddbc-snippet--parsed"))
            self.activatables[feature_name] = feature_description
    
    async def parse_contents(self):
        '''
        basic
        |- ct-actions-list__basic-heading
        |- ct-actions-list__basic-list
        '''
        basic = await self.stats_element.querySelector(".ct-actions-list__content .ct-actions-list__basic")
        if shared_data.debug_enabled : await highlight_element(basic)
        self.basic_activatable = await get_text_content(await basic.querySelector(".ct-actions-list__basic-list"))
        activatables = await self.stats_element.querySelectorAll(".ct-actions-list__content .ct-actions-list__activatable")
        await self.parse_activatables(activatables) 
    
    def add_other_content(self):
        pass

class Action(Section):
    '''
    ct-actions-list
    |-ct-actions-list__heading
        |-ct-actions__attacks-heading  -- for action and attack #
    |-ct-actions-list__content
        |- ddbc-attack-table
            |-ddbc-attack-table__row-header
            |ddbc-attack-table__content
                |-ddbc-combat-attack__name
        |-ct-actions-list__basic
        |-ct-actions-list__activatable [list]
            |-ct-feature-snippet
    '''
    pass
    

class BonusAction(Section):
    '''
    ct-actions-list
    |-ct-actions-list__heading
        |-ct-actions__attacks-heading 
    |-ct-actions-list__content
        |-ct-actions-list__basic
        |-ct-actions-list__activatable [list]
            |-ct-feature-snippet
    '''
    pass


class Reactions(Section):
    '''
    ct-actions-list
    |-ct-actions-list__heading
        |-ct-actions__attacks-heading 
    |-ct-actions-list__content
        |-ct-actions-list__basic
        |-ct-actions-list__activatable [list]
            |-ct-feature-snippet
    '''
    pass


class Spells:
    def __init__(self, spellblock) -> None:
        self.spellblock = spellblock

        
'''
Others:
ct-actions-list
    |-ct-actions-list__heading
        |-ct-actions__attacks-heading 
    |-ct-actions-list__content
        |-ct-actions-list__basic
        |-ct-actions-list__activatable [list]
            |-ct-feature-snippet

'''