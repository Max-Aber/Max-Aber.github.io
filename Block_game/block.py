"""
This file contains the Block class, the main data structure used in the game.

This file is part of the Block assignment.
"""
from typing import Optional
import random
import math
from renderer import COLOR_LIST, TEMPTING_TURQUOISE, BLACK, color_name


HIGHLIGHT_COLOR = TEMPTING_TURQUOISE
FRAME_COLOR = BLACK


class Block:
    """A square block in the Blocky game.

    === Public Variables ===
    position:
        The (x, y) coordinates of the upper left corner of this Block.
        Note that (0, 0) is the top left corner of the window.
    size:
        The height and width of this Block.  Since all blocks are square,
        we needn't represent height and width separately.
    color:
        If this block is not subdivided, <color> stores its color.
        Otherwise, <color> is None and this block's sublocks store their
        individual colors.
    level:
        The level of this block within the overall block structure.
        The outermost block, corresponding to the root of the tree,
        is at level zero.  If a block is at level i, its children are at
        level i+1.
    max_depth:
        The deepest level allowed in the overall block structure.
    highlighted:
        True iff the user has selected this block for action.
    children:
        The blocks into which this block is subdivided.  The children are
        stored in this order: upper-right child, upper-left child,
        lower-left child, lower-right child.
    parent:
        The block that this block is directly within.

    === Representation Invariations ===
    - len(children) == 0 or len(children) == 4
    - If this Block has children,
        - their max_depth is the same as that of this Block,
        - their size is half that of this Block,
        - their level is one greater than that of this Block,
        - their position is determined by the position and size of this Block,
          as defined in the Assignment 2 handout, and
        - this Block's color is None
    - If this Block has no children,
        - its color is not None
    - level <= max_depth
    """

    position: tuple[int, int]
    size: int
    color: Optional[tuple[int, int, int]]
    level: int
    max_depth: int
    highlighted: bool
    children: list['Block']
    parent: Optional['Block']

    def __init__(self, level: int,
                 color: Optional[tuple[int, int, int]] = None,
                 children: Optional[list['Block']] = None) -> None:
        """Initialize this Block to be an unhighlighted root block with
        no parent.

        If <children> is None, give this block no children.  Otherwise
        give it the provided children.  Use the provided level and color,
        and set everything else (x and y coordinates, size,
        and max_depth) to 0.  (All attributes can be updated later, as
        appropriate.)
        """
    
        self.highlighted = False
        self.parent = None  # non highlightes, parentless
        self.level = level
        
        self.position = (0, 0)
        self.size = 0
        self.max_depth = 0
        
        if color is not None:
            self.color = color
        
        if children is None:
            self.children = []
        else:
            self.color = None
            assert len(children) == 4, "Wrong number of children"
            self.children = children
            for child in children:
                
                child.parent = self
                
    
        

    def rectangles_to_draw(self) -> list[tuple[tuple[int, int, int],
                                               tuple[int, int],
                                               tuple[int, int],
                                               int]]:
        """
        Return a list of tuples describing all of the rectangles to be drawn
        in order to render this Block.

        This includes (1) for every undivided Block:
            - one rectangle in the Block's color
            - one rectangle in the FRAME_COLOR to frame it at the same
              dimensions, but with a specified thickness of 3
        and (2) one additional rectangle to frame this Block in the
        HIGHLIGHT_COLOR at a thickness of 5 if this block has been
        selected for action, that is, if its highlighted attribute is True.

        The rectangles are in the format required by method Renderer.draw.
        Each tuple contains:
        - the color of the rectangle
        - the (x, y) coordinates of the top left corner of the rectangle
        - the (height, width) of the rectangle, which for our Blocky game
          will always be the same
        - an int indicating how to render this rectangle. If 0 is specified
          the rectangle will be filled with its color. If > 0 is specified,
          the rectangle will not be filled, but instead will be outlined in
          the FRAME_COLOR, and the value will determine the thickness of
          the outline.

        The order of the rectangles does not matter.

        Returns:
            (list) The list of tuples, as described above.
        """
        rectangles = []
        
        if self.children == []: # if block has no children
            # rectangle to be colored in
            rectangles.append((self.color, self.position, (self.size, self.size), 0))
            
            # rectangle for the outline using the frame color
            rectangles.append((FRAME_COLOR, self.position, (self.size, self.size), 3))
            
            if self.highlighted:    # if highlighted thickness of 5, and highlighted color
                rectangles.append((HIGHLIGHT_COLOR, self.position, (self.size, self.size), 5))
                
        else:   # rectangle has children
            
            for child in self.children: # recursively call rectangles to draw for each child
                rectangles.extend(child.rectangles_to_draw())
            
            if self.highlighted:    # if highlighted add another rectangle with thickness of 5
                rectangles.append((HIGHLIGHT_COLOR, self.position, (self.size, self.size), 5))
                
        return rectangles

    def swap(self, direction: int) -> None:
        """Swap the child Blocks of this Block.

        If <direction> is 1, swap vertically.  If <direction> is 0, swap
        horizontally. If this Block has no children, do nothing.
        
        Parameters:
            direction: (int) The direction to swap (0 or 1)
        """
        if len(self.children) > 0:
            if direction == 1:
                # swap vertically: top and bottom
                self.children[0], self.children[1], self.children[2], self.children[3] = self.children[3], self.children[2], self.children[1], self.children[0]
                self.update_block_locations(self.position,self.size)
            elif direction == 0:
                # swap Horizantally: left and right
                self.children[0], self.children[1], self.children[2], self.children[3] = self.children[1], self.children[0], self.children[3], self.children[2]
                self.update_block_locations(self.position,self.size)
        

    def rotate(self, direction: int) -> None:
        """Rotate this Block and all its descendants.

        If <direction> is 1, rotate clockwise.  If <direction> is 3, rotate
        counterclockwise. If this Block has no children, do nothing.

        Parameters:
            direction: (int) The direction to rotate (1 or 3)
        """
        if len(self.children) > 0:
            if direction == 1:
                # Swap Vertically: clockwise
                self.children[0], self.children[1], self.children[2], self.children[3] = self.children[1], self.children[2], self.children[3], self.children[0]
                self.update_block_locations(self.position,self.size)
            elif direction == 3:
                # Swap Horizantally: counterclockwise
                self.children[1], self.children[2], self.children[3], self.children[0] = self.children[0], self.children[1], self.children[2], self.children[3]
                self.update_block_locations(self.position,self.size)
        

    def smash(self) -> bool:
        """Smash this block.

        If this Block can be smashed, randomly generating four new child
        Blocks for it.  (If it already had child Blocks, discard them.) Ensure
        that the RI's of the Blocks remain satisfied.

        A Block can be smashed iff it is not the top-level Block and it is not
        already at the level of the maximum depth.

        Returns:
            (bool) True if this Block was smashed and False otherwise.
        """
        if self.level != 0 and self.level != self.max_depth:
            # if not top level and not max depth
            if len(self.children) > 0:
                for i in range(4):  # if it already has children randomize them
                    self.children[i] = random_init(self.level, self.max_depth-1) 
                    # create new random children
                self.update_block_locations(self.position,self.size)
                return True
            else:
                for i in range(4):  # if it did not have children already create new random ones
                    self.children.append(random_init(self.level, self.max_depth-1))
                    # create new random children
                self.update_block_locations(self.position,self.size)
                return True
            
        else:   #if not possible return false
            return False
    

    def update_block_locations(self, top_left: tuple[int, int],
                               size: int) -> None:
        """
        Update the position and size of each of the Blocks within this Block.

        Ensure that each is consistent with the position and size of its
        parent Block.

        Parameters:
            top_left: (tuple[int,int]) the (x, y) coordinates of the top left corner of this Block.
            size: (int) The height and width of this Block.
        """
        self.position = top_left    # assign values to the current block
        self.size = size
        
        x, y = top_left
        
        if len(self.children) > 0:
            ch_size = round(size/2) 
            # calculate the size by dividing by 2 because the block is divided 
            # into 4, 2 and 2 H and V
            ch_pos = [
                (x + ch_size, y),  # top right
                (x, y), # top left
                (x, y + ch_size), # bottom left
                (x + ch_size, y + ch_size) # bottom right
            ]
            
            for i, child in enumerate(self.children):
                child.update_block_locations(ch_pos[i], ch_size)
        
        

    def get_selected_block(self, location: tuple[int, int], level: int) -> 'Block':
        """Return the Block within this Block that includes the given location
        and is at the given level. If the level specified is lower than
        the lowest block at the specified location, then return the block
        at the location with the closest level value.

        Parameters:
            location: (tuple[int,int]) The (x, y) coordinates of the location on the window
                whose corresponding block is to be returned.
            level: (int) The level of the desired Block. Note that if a Block
                includes the location (x, y), and that Block is subdivided, then
                one of its four children will contain the location (x, y) also;
                this is why <level> is needed.

        Preconditions:
        - 0 <= level <= max_depth

        Returns:
            (Block) The block at the specified location and level.
        """

        assert 0 <= level <= self.max_depth, f"Invalid Level, level: {level}, max_depth: {self.max_depth}"
        
        # base case: if the block your looking for is the one you are in
        if self.level == level or not self.children:
            return self

        # recursive case: looks at current blocks children blocks for block at given location and level
        for child in self.children:
            if child.position[0] <= location[0] < child.position[0] + child.size and child.position[1] <= location[1] < child.position[1] + child.size:
                selected_block = child.get_selected_block(location, level)
                if selected_block is not None:
                    return selected_block
    
        # If the requested level is lower than the lowest block at the specified location, return the block at the location with the closest level value.
        return self   


    def flatten(self) -> list[list[tuple[int, int, int]]]:
        """Return a two-dimensional list representing this Block as rows
        and columns of unit cells.

        Returns:
            (list[list[tuple[int, int, int]]]) A list of lists L, where,
                for 0 <= i, j < 2^{max_depth - self.level}
                    - L[i] represents column i and
                    - L[i][j] represents the unit cell at column i and row j.
            Each unit cell is represented by 3 ints for the color of the block
            at the cell location[i][j]

            L[0][0] represents the unit cell in the upper left corner of the Block.
        """
        size = 2 ** (self.max_depth - self.level)
        
        if len(self.children) > 0: # if it has children it does not have a color
            tl = self.children[1].flatten()
            tr = self.children[0].flatten() # recurse flatten on children
            bl = self.children[2].flatten()
            br = self.children[3].flatten()
            
            flattened = []
            for i in range(len(tl)):
                new = []
                new.extend(tl[i]) # add all from left column
                new.extend(bl[i])
                flattened.append(new)
                
            for i in range(len(tr)):
                new = []
                new.extend(tr[i]) # add all from right column
                new.extend(br[i])
                flattened.append(new)
                
            return flattened
        else: # if it does not have children
            
            flattened = []
            for i in range(size):
                new = []    # make the list acording to the size
                for j in range(size):
                    new.append(self.color)
                flattened.append(new)
            return flattened
        


def random_init(level: int, max_depth: int) -> 'Block':
    """Return a randomly-generated Block with level <level> and subdivided
    to a maximum depth of <max_depth>.

    Throughout the generated Block, set appropriate values for all attributes
    except position and size.  They can be set by the client, using method
    update_block_locations.

    Precondition:
        level <= max_depth

    Parameters:
        level: (int) Level for the generated block
        max_depth: (int) The maximum depth to subdivide the block.

    Returns:
        (Block): The randomly generated Block.
    """
    assert level <= max_depth, "Invalid Level"
    
    # if not at max depth and random says to, create children with recursion and create block
    if level != max_depth and random.random() < math.exp(-0.25 * level): 
        children = [random_init(level + 1, max_depth) for _ in range(4)]
        bl =  Block(level, None, children)
        bl.max_depth = max_depth
        bl.update_block_locations((0,0),750)
        return bl
    else:   # else just create block without children with random color
        color = random.choice(COLOR_LIST)
        bl = Block(level, color, None)
        bl.max_depth = max_depth
        bl.update_block_locations((0,0),750)
        return bl
    


def attributes_str(b: Block, verbose: bool) -> str:
    """Return a str that is a concise representation of the attributes of <b>.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Note: These are attributes that every Block has.

    Parameters:
        b: (Block) The Block to generate the string for.
        verbose: (bool) Flag to indicate whether additional info is included
            in the string.

    Returns:
        String representation of b's attributes.
    """
    answer = f'pos={b.position}, size={b.size}, level={b.level}, '
    if verbose:
        answer += f'highlighted={b.highlighted}, max_depth={b.max_depth}'
    return answer


def print_block(b: Block, verbose: bool = False) -> None:
    """Print a text representation of Block <b>.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Precondition: b is not None.

    Parameters:
        b: (Block) The Block to print.
        verbose: (bool) Flag to indicate whether additional info is included
            in the printout.

    """
    print_block_indented(b, 0, verbose)


def print_block_indented(b: Block, indent: int, verbose: bool) -> None:
    """Print a text representation of Block <b>, indented <indent> steps.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Precondition: b is not None.

    Parameters:
        b: (Block) The Block to print.
        indent: (int) The indentation level (i.e. number of steps)
        verbose: (bool) Flag to indicate whether additional info is included
            in the printout.
    """
    if len(b.children) == 0:
        # b a leaf.  Print its color and other attributes
        print(f'{"  " * indent}{color_name(b.color)}: ' +
              f'{attributes_str(b, verbose)}')
    else:
        # b is not a leaf, so it doesn't have a color.  Print its
        # other attributes.  Then print its children.
        print(f'{"  " * indent}{attributes_str(b, verbose)}')
        for child in b.children:
            print_block_indented(child, indent + 1, verbose)


if __name__ == '__main__':
    print("File ran")