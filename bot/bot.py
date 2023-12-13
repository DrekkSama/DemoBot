from sc2.bot_ai import BotAI, Race
from sc2.data import Result
from sc2.ids.unit_typeid import UnitTypeId

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

    async def on_step(self, iteration: int):
        """
        This code runs continually throughout the game
        Populate this function with whatever your bot should do!
        """
        if iteration == 0:
            for worker in self.workers:
                worker.attack(self.enemy_start_locations[0])
                
        nexus_list = self.townhalls(UnitTypeId.NEXUS).ready.idle # get a list of idle nexuses
        for nexus in nexus_list: # loop through all idle nexuses
            if self.can_afford(UnitTypeId.PROBE) and self.workers.amount <= 15: # if we can afford a probe and have less than 15 workers
                nexus.train(UnitTypeId.PROBE) # train a probe
            elif self.workers.amount == 15: # if we have 15 workers
                for worker in self.workers: # loop through all workers
                    worker.attack(self.enemy_start_locations[0]) # attack the enemy start location

    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        print("Game ended.")
