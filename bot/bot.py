from sc2.bot_ai import BotAI, Race
from sc2.data import Result
from sc2.ids.unit_typeid import UnitTypeId

import random

class CompetitiveBot(BotAI):
    NAME: str = "Demo Bot"
    """This bot's name"""

    RACE: Race = Race.Protoss
    """This bot's Starcraft 2 race.
    Options are:
        Race.Terran
        Race.Zerg
        Race.Protoss
        Race.Random
    """
    def __init__(self):
        super().__init__()
        self.occupied_positions = []
       
    async def on_start(self):
        """
        This code runs once at the start of the game
        Do things here before the game starts
        """
        print("Game started")
        self.starting_nexus = self.townhalls.first  # store the starting nexus
        self.probe = self.workers.random
       


    async def on_step(self, iteration):
        if iteration == 0:
            await self.chat_send("(probe)(pylon)(cannon)(cannon)(gg)")

        if not self.townhalls:
            # Attack with all workers if we don't have any nexuses left, attack-move on enemy spawn (doesn't work on 4 player map) so that probes auto attack on the way
            for worker in self.workers:
                worker.attack(self.enemy_start_locations[0])
            return

        nexus = self.townhalls.random

        # Make probes until we have 16 total
        if self.supply_workers < 16 and nexus.is_idle:
            if self.can_afford(UnitTypeId.PROBE):
                nexus.train(UnitTypeId.PROBE)

        # If we have no pylon, build one near starting nexus
        elif not self.structures(UnitTypeId.PYLON) and self.already_pending(UnitTypeId.PYLON) == 0:
            if self.can_afford(UnitTypeId.PYLON):
                await self.build(UnitTypeId.PYLON, near=nexus)

        # If we have no forge, build one near the pylon that is closest to our starting nexus
        elif not self.structures(UnitTypeId.FORGE):
            pylon_ready = self.structures(UnitTypeId.PYLON).ready
            if pylon_ready:
                if self.can_afford(UnitTypeId.FORGE):
                    await self.build(UnitTypeId.FORGE, near=pylon_ready.closest_to(nexus))

        # If we have less than 2 pylons, build one at the enemy base
        elif self.structures(UnitTypeId.PYLON).amount < 2:
            if self.can_afford(UnitTypeId.PYLON):
                pos = self.enemy_start_locations[0].towards(self.game_info.map_center, random.randrange(8, 15))
                self.probe.build(UnitTypeId.PYLON, pos)

        # If we have no cannons but at least 2 completed pylons, automatically find a placement location and build them near enemy start location
        elif self.structures(UnitTypeId.PHOTONCANNON).amount < 5:
            if self.structures(UnitTypeId.PYLON).ready.amount >= 2 and self.can_afford(UnitTypeId.PHOTONCANNON) and not self.probe.orders:
                pylon = self.structures(UnitTypeId.PYLON).closer_than(20, self.enemy_start_locations[0]).random
                # Create a 6x6 grid of positions around the Pylon
                positions = [pylon.position.to2.offset((x, y)) for x in range(-3, 4) for y in range(-3, 4)]
                positions = [pos for pos in positions if pos not in self.occupied_positions]  # Exclude already occupied positions
                random.shuffle(positions)  # Shuffle the list of positions
        
                # build cannons in available positions
                for pos in positions:
                    if self.can_place(UnitTypeId.PHOTONCANNON, pos):
                        position = pos  # Use the current position in the loop
                        placement = await self.find_placement(UnitTypeId.PHOTONCANNON, near=position, placement_step=1)
                        if placement is not None:  # Check if a placement was found
                            self.occupied_positions.append(placement)  # Add the placement to the list of occupied positions
                            self.probe.build(UnitTypeId.PHOTONCANNON, placement)  # Build the Photon Cannon at the placement
                        
                
        
          

    async def on_end(self, result: Result):
        """
        This code runs once at the end of the game
        Do things here after the game ends
        """
        print("Game ended.")
