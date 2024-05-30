"""
This file (part of Blocky) contains the Goal class hierarchy.
"""

from block import Block


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    DO NOT MODIFY THIS CLASS IN ANY WAY!

    Attributes:
        color (tuple[int, int, int]): The target color for this goal, that is
        the color to which this goal applies.
    """
    color: tuple[int, int, int]

    def __init__(self, target_color: tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target color."""
        self.color = target_color

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.

        Parameters:
            board: (Block) The board to get the score for.
        """
        raise NotImplementedError

    def description(self) -> str:
        """ Return a description of this goal. """
        raise NotImplementedError


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    color, anywhere within the Block.
    """
    def _undiscovered_blob_size(self, pos: tuple[int, int],
                                board: list[list[tuple[int, int, int]]],
                                visited: list[list[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target color, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.

        Parameters:
            pos: (tuple[int, int]) Target cell for blob.
            board: (list[list[tuple]]) is the flattened board on which to search for the blob.
            visited: (list[list[int]]) is a parallel structure that, in each cell, contains:
               -1  if this cell has never been visited
                0  if this cell has been visited and discovered
                   not to be of the target color
                1  if this cell has been visited and discovered
                   to be of the target color

        """
        # if out of bounds
        x, y = pos
        if x < 0 or y < 0 or x >= len(board) or y >= len(board):
            return 0
        # if already visited
        if visited[x][y] != -1:
            return 0
        
        # if wrong color
        if board[x][y] != self.color:
            visited[x][y] = 0
            return 0
        
        visited[x][y] = 1
        size = 1 # initialize size and indicate that visited with blob
        
        neighbors = [(-1,0),(1,0),(0,-1),(0,1)]
        for m, n in neighbors:  # recurse with neighbors
            size += self._undiscovered_blob_size((x+m, y+n), board, visited)
            
        return size

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.

        Parameters:
            board: (Block) The board to get the score for.
        """
        flattened = board.flatten()
        
        vis = []
        for i in range(len(flattened)):
            new = []    # make a copy of flattened for visited cells
            for j in range(len(flattened)): 
                new.append(-1)
            vis.append(new)
        
        biggest_blob = 0
        for i in range(len(flattened)):
            for j in range(len(flattened)):
                if vis[i][j] == -1 and flattened[i][j] == self.color:
                    blob_size = self._undiscovered_blob_size((i,j), flattened, vis)
                    if blob_size > biggest_blob:
                        biggest_blob = blob_size
        
        return biggest_blob

        
    def description(self) -> str:
        """ Return a description of this goal. """
        return "Blob: Largest connected blob"

class PerimeterGoal(Goal):
    """A goal to create the largest perimeter of this goal's target
    color, anywhere within the Block."""
    

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.

        Parameters:
            board: (Block) The board to get the score for.
        """
        flattened_board = board.flatten()
        size = len(flattened_board)
        score = 0

        # Top and bottom rows
        for j in range(size):
            if flattened_board[0][j] == self.color:
                score += 1
            if flattened_board[size - 1][j] == self.color:
                score += 1

        # Left and right columns
        for i in range(size): # we are revisiting the corner cells her too
            if flattened_board[i][0] == self.color:
                score += 1
            if flattened_board[i][size - 1] == self.color:
                score += 1

        return score
        
        
        
    def description(self) -> str:
        """ Return a description of this goal. """
        return f"Perimeter: Most touching the outer perimeter"

