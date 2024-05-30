"""
This file contains the Game class, which is the main class for the Blocky
game.

At the bottom of the file, there are some function that you can call to try
playing the game in several different configurations.
"""

import random
from block import Block, random_init
from goal import BlobGoal, PerimeterGoal
from player import Player, HumanPlayer
from renderer import Renderer, COLOR_LIST, color_name, BOARD_WIDTH


class Game:
    """A game of Blocky.

    Public Attributes:
        board (Block):
            The Blocky board on which this game will be played.
        renderer (Renderer):
            The object that is capable of drawing our Blocky board on the screen,
            and tracking user interactions with the Blocky board.
        players (list[Player]):
            The entities that are playing this game.

    Representation Invariants:
        1. len(players) >= 1
    """

    board: Block
    renderer: Renderer
    players: list[Player]

    def __init__(self, max_depth: int, num_pla: int) -> None:
        """Initialize this game.

        Precondition:
            2 <= max_depth <= 5
        """
        assert 2 <= max_depth and max_depth <= 5, "Invalid Max depth"
        
        #initialize render
        self.renderer = Renderer(num_pla)
        self.board = random_init(0, max_depth)  #create board and update locations
        self.board.update_block_locations((0,0), 750)
        
        # player creation:
        self.players = []
        player_colors = COLOR_LIST[:]
        random.shuffle(player_colors)
        
        for i in range(num_pla):
            goal_idx = random.randrange(0,2) # creates human players with random goal
            g = BlobGoal(player_colors[i]) if goal_idx == 1 else PerimeterGoal(player_colors[i])
            pla = HumanPlayer(self.renderer, i+1, g)
            self.players.append(pla)
        
        self.renderer.draw(self.board)

        return None


    def run_game(self, num_turns: int) -> None:
        """Run the game for the number of turns specified.

        Each player gets <num_turns> turns. The first player in self.players
        goes first.  Before each move, print to the console whose turn it is
        and what the turn number is.  After each move, print the current score
        of the player who just moved.

        When the game is over, print who won to the console.

        Parameters:
            num_turns: (int) The number of turns to run the game for.

        """
        assert num_turns >= 0, "Number of turns must be non-negative"

        max_turn = num_turns * len(self.players)
        self.renderer.display_turn_info(self.board, self.players, 0, max_turn, 0)

        # Index within self.players of the current player.
        index = 0
        for turn in range(max_turn):
            player = self.players[index]
            print(f'Player {player.id}, turn {turn}')
            if self.players[index].make_move(self.board) == 1:
                break
            else:
                print(f'Player {player.id} CURRENT SCORE: ' +
                      f'{player.goal.score(self.board)}')
                index = (index + 1) % len(self.players)
                self.renderer.display_turn_info(self.board, self.players,
                                                turn+1, max_turn, index)

        # Determine and report the winner.
        max_score = 0
        winning_player = 0
        for i in range(len(self.players)):
            score = self.players[i].goal.score(self.board)
            print(f'Player {i} : {score}')
            if score > max_score:
                max_score = score
                winning_player = i
        print(f'WINNER is Player {winning_player+1}!')
        print('Players had these goals:')   # anounce winner and final standings
        for player in self.players:
            print(f'Player {player.id} ' +
                  f'goal = \n\t{player.goal.description()}: ' +
                  f'{color_name(player.goal.color)}')

        self.renderer.display_winner(winning_player)


def multiplayer_game(num_of_players, turns_per_player) -> None:
    """ Run a game with 2 or more players. """
    game = Game(3, num_of_players)
    game.run_game(turns_per_player)


def solitaire_game(total_turns) -> None:
    """ Run a game with one human player. """
    game = Game(4, 1)
    game.run_game(total_turns) 
    
def main():
    print("Hello welcome to the BLOCK game!")
    print("--------------------------------")
    turns = int(input("How many turns for each player? (5-30) "))
    while turns not in range(5, 31):
        print("Invalid amount")
        turns = int(input("How many turns for each player? (5-30) "))
    
    multiplayer_or_single = input("Do you want to play single(1) or against another player(2)? ")
    while multiplayer_or_single not in ['1','2']:
        print("Invalid input")
        multiplayer_or_single = input("Do you want to play single(1) or against another player(2)? ")
        
    if multiplayer_or_single == '2':
        players = int(input("How many players? (2-4) "))
        while players not in range(2, 5):
            print("Invalid amount")
            players = int(input("How many players? (2-4) "))
            
        multiplayer_game(players, turns)
        
    elif multiplayer_or_single == '1':
        solitaire_game(turns)
        
    

if __name__ == '__main__':
    main()
