import gamelib
import random
import math
import warnings
from sys import maxsize, exit
import json


class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        # gamelib.debug_write("Random seed: {}".format(seed))

    def on_game_start(self, config):
        """
        Read in config and perform any initial setup here
        """
        # gamelib.debug_write("Configuring your custom algo strategy...")
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0
        # This is a good place to do initial setup
        self.scored_on_locations = []

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        # gamelib.debug_write(
        # "Performing turn {} of your custom algo strategy".format(
        # game_state.turn_number
        # )
        # )
        game_state.suppress_warnings(
            True
        )  # Comment or remove this line to enable warnings.

        self.starter_strategy(game_state)
        # gamelib.debug_write(game_state.contains_stationary_unit([12, 26]))
        game_state.submit_turn()

    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """

    def starter_strategy(self, game_state):
        if game_state.turn_number == 1:
            self.build_turn_1

        self.build_walls_1(game_state)
        self.upgrade_walls_1(game_state)
        self.build_turrets_1(game_state)
        self.build_supports_1(game_state)
        self.upgrade_supports_1(game_state)
        self.build_supports_2(game_state)
        self.upgrade_supports_2(game_state)

        if game_state.get_resource(MP, 1) > 11:
            self.stall_with_interceptors(game_state)
        if game_state.get_resource(MP, 1) > 15:
            self.stall_with_interceptors(game_state)

        if game_state.turn_number % 2 == 1:
            game_state.attempt_spawn(DEMOLISHER, [14, 0], 1)
            game_state.attempt_spawn(SCOUT, [14, 0], 1000)

    def build_turn_1(self, game_state):
        turret_locations = [[25, 12], [3, 11], [6, 11]]
        game_state.attempt_spawn(TURRET, turret_locations)
        wall_locations = [
            [0, 13],
            [27, 13],
            [6, 12],
            [5, 11],
            [1, 12],
            [24, 12],
            [26, 12],
            [2, 11],
            [7, 11],
            [23, 11],
            [25, 11],
            [6, 10],
            [24, 10],
            [7, 9],
            [23, 9],
            [8, 8],
            [22, 8],
            [9, 7],
            [21, 7],
            [10, 6],
            [20, 6],
            [11, 5],
            [19, 5],
            [12, 4],
            [18, 4],
            [13, 3],
            [17, 3],
            [14, 2],
            [16, 2],
            [15, 1],
        ]
        game_state.attempt_spawn(WALL, wall_locations)
        game_state.attempt_upgrade(wall_locations)

    def build_walls_1(self, game_state):
        wall_locations = [
            [0, 13],
            [27, 13],
            [6, 12],
            [5, 11],
            [1, 12],
            [24, 12],
            [26, 12],
            [2, 11],
            [7, 11],
            [23, 11],
            [25, 11],
            [6, 10],
            [24, 10],
            [7, 9],
            [23, 9],
            [8, 8],
            [22, 8],
            [9, 7],
            [21, 7],
            [10, 6],
            [20, 6],
            [11, 5],
            [19, 5],
            [12, 4],
            [18, 4],
            [13, 3],
            [17, 3],
            [14, 2],
            [16, 2],
            [15, 1],
            [25, 13],
        ]
        game_state.attempt_spawn(WALL, wall_locations)

    def upgrade_walls_1(self, game_state):
        wall_upgrade_locations = [
            [27, 13],
            [0, 13],
            [6, 12],
            [24, 12],
            [5, 11],
            [23, 11],
            [25, 13],
        ]
        game_state.attempt_upgrade(wall_upgrade_locations)

    def build_turrets_1(self, game_state):
        turret_locations = [
            [25, 11],
            [2, 12],
            [5, 12],
            [3, 11],
            [6, 11],
            [7, 10],
            [3, 10],
            [24, 11],
            [25, 12],
        ]
        game_state.attempt_spawn(TURRET, turret_locations)

    def build_supports_1(self, game_state):
        support_locations = [
            [4, 9],
            [6, 7],
            [7, 6],
            [8, 5],
            [9, 4],
            [10, 3],
            [11, 2],
            [12, 1],
            [13, 0],
        ]
        game_state.attempt_spawn(SUPPORT, support_locations)

    def upgrade_supports_1(self, game_state):
        support_locations = [
            [4, 9],
            [5, 8],
            [6, 7],
            [7, 6],
            [8, 5],
            [9, 4],
            [10, 3],
            [11, 2],
        ]
        game_state.attempt_upgrade(support_locations)

    def build_supports_2(self, game_state):
        support_locations = [
            [8, 9],
            [9, 8],
            [10, 7],
            [11, 6],
            [12, 5],
            [13, 4],
            [14, 3],
            [15, 2],
        ]
        game_state.attempt_spawn(SUPPORT, support_locations)

    def upgrade_supports_2(self, game_state):
        support_locations = [
            [4, 9],
            [5, 8],
            [6, 7],
            [7, 6],
            [8, 5],
            [9, 4],
            [10, 3],
            [11, 2],
        ]
        game_state.attempt_upgrade(support_locations)

    def stall_with_interceptors(self, game_state):
        game_state.attempt_spawn(INTERCEPTOR, [5, 8], 1)

    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at in json-docs.html in the root of the Starterkit.
        """
        # Let's record at what position we get scored on
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            # When parsing the frame data directly,
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                # gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append(location)
                # gamelib.debug_write(
                # "All locations: {}".format(self.scored_on_locations)
                # )


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
