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
    
    async def parse_basic_activatable(self):
        '''
        basic
        |- ct-actions-list__basic-heading
        |- ct-actions-list__basic-list
        '''
        basic = await self.stats_element.querySelector(".ct-actions-list__content .ct-actions-list__basic .ct-actions-list__basic-list")
        if shared_data.debug_enabled : await highlight_element(basic)
        self.basic_activatable = await get_text_content(basic)

    async def parse_activatables(self):
        '''
        activatable
        |- ct-feature-snippet__heading
        |- ct-feature-snippet__content
            |- ddbc-snippet  ddbc-snippet--parsed
        '''
        activatable_elements = await self.stats_element.querySelectorAll(".ct-actions-list__content .ct-actions-list__activatable")
        for activatable in activatable_elements:
            if shared_data.debug_enabled : await highlight_element(activatable)
            feature_name = str(await get_text_content(await activatable.querySelector(".ct-feature-snippet__heading"))).strip()
            feature_description = await get_text_content(await activatable.querySelector(".ct-feature-snippet__content .ddbc-snippet.ddbc-snippet--parsed"))
            self.activatables[feature_name] = feature_description

    async def parse_contents(self):        
        await self.parse_basic_activatable()
        await self.parse_activatables() 
    
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
    async def parse_attack_table(self):
        '''
        ddbc-attack-table
        |-
            |- ddbc-combat-attack--item ddbc-combat-item-attack--melee ddbc-combat-attack
            |- ddbc-combat-attack--item ddbc-combat-item-attack--ranged ddbc-combat-attack
                |- ddbc-combat-attack__label 
        '''
        attack_table = await self.stats_element.querySelector(".ddbc-attack-table")
        self.melee_weapons = await attack_table.querySelectorAll(".ddbc-combat-item-attack--melee .ddbc-combat-attack__label")
        self.ranged_weapons = await attack_table.querySelectorAll(".ddbc-combat-item-attack--ranged .ddbc-combat-attack__label")

        self.melee_weapons = [await get_text_content(x) for x in self.melee_weapons]
        self.ranged_weapons = [await get_text_content(x) for x in self.ranged_weapons]
    
    async def parse_contents(self):
        await self.parse_attack_table()     
        await self.parse_basic_activatable()
        await self.parse_activatables() 
    

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