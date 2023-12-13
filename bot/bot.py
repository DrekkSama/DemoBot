from sc2.bot_ai import BotAI, Race
from sc2.data import Result
from sc2.ids.unit_typeid import UnitTypeId
from sc2.ids.ability_id import AbilityId


class CompetitiveBot(BotAI):
    NAME: str = "Zippy"
    """This bot's name"""

    RACE: Race = Race.Protoss
    """This bot's Starcraft 2 race.
    Options are:
        Race.Terran
        Race.Zerg
        Race.Protoss
        Race.Random
    """

    async def on_start(self):
        """
        This code runs once at the start of the game
        Do things here before the game starts
        """
        print("Game started")
        self.starting_nexus = self.townhalls.first  # store the starting nexus


    async def on_step(self, iteration: int):
        """
        This code runs continually throughout the game
        Populate this function with whatever your bot should do!
        """
      
        nexus_list = self.townhalls(UnitTypeId.NEXUS).ready.idle # get a list of idle nexuses
        for nexus in nexus_list: # loop through all idle nexuses
            if nexus.energy >= 50: # if the nexus has enough energy to chrono boost
                abilities = await self.get_available_abilities(nexus) # get the abilities of the nexus
                if AbilityId.EFFECT_CHRONOBOOSTENERGYCOST in abilities: # check if chrono boost ability is available
                    target = self.starting_nexus  # target the starting nexus
                    nexus(AbilityId.EFFECT_CHRONOBOOSTENERGYCOST, target) # chrono boost the nexus
                    print("Chrono Boost in da house - Bzzooom")
                    
            if self.can_afford(UnitTypeId.PROBE) and self.workers.amount <= 15: # if we can afford a probe and have less than 15 workers
                nexus.train(UnitTypeId.PROBE) # train a probe
                print("Trained Probe - Bzzzt")
            elif self.workers.amount == 15: # if we have 15 workers
                for worker in self.workers: # loop through all workers
                    target_area = self.enemy_start_locations[0].position.offset((-4, -4))  # Create a new point 4 units to the left and below the enemy start location
                    worker.attack(target_area)  # Attack the target area
                print("ATTACK! Boop!")
                    
                    

    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        print("Game ended.")
