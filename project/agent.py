from grid import *
import math
import heapq

class Agent:
    def __init__(self, grid: str):
        self.grid = grid
        self.grid_size = int(math.sqrt(len(self.grid)))
        self.pieces = pieces(self.grid, self.grid_size)


    def next_states(self, grid: str):
        """Get all possible next states of a given grid"""
        directions = [(0,1), (0,-1), (1,0), (-1,0)]
        states = []
        for piece in self.pieces:
            for direction in directions:
                new_grid = move(grid, self.grid_size, piece, direction)
                if new_grid:
                    states.append((new_grid, piece))
        return states


    def get_path(self, node: tuple):
        """Recieves a node and returns the path to the root node"""
        if node[1] == None:
            return [node[0]]
        path = self.get_path(node[1])
        path += [node[0]]
        return(path)


    def is_solved(self, grid: str):
        """Check if a given grid is solved"""

        if self.blocking_pieces(grid) == 0:
            return True
        return False




    def blocking_pieces(self, grid: str):
        """Count the number of pieces blocking the player car"""

        for line in range(self.grid_size):
            for col in range(self.grid_size-1, 0, -1):
                index = line*self.grid_size + col
                if grid[index] == PLAYER_CAR:
                    player_line = grid[index+1:(line+1)*self.grid_size]
                    return len(player_line) - player_line.count(EMPTY_TILE)
                

    def heuristic(self, grid: str, diff_piece: bool):
        """Returns the heuristic value of a given grid"""
        heuristic = 0

        # Heuristic 1: Piece moved is different from the previous one
        heuristic += diff_piece

        # Find player's line
        for line in range(self.grid_size):
            for col in range(self.grid_size-1, 0, -1):
                index = line*self.grid_size + col
                if grid[index] == PLAYER_CAR:
                    player_line = grid[index+1:(line+1)*self.grid_size]

                    # Heuristic 2: Distance of player car to exit
                    heuristic += len(player_line)

                    # Heuristic 3: Number of blocking pieces
                    heuristic += len(player_line) - player_line.count(EMPTY_TILE)

                    return heuristic


    def solve(self):
        """Solve the puzzle"""

        # Current grid as parent node
        # Node = (state, parent, cost, heuristic, piece)
        root = (self.grid, None, 0, self.heuristic(self.grid, 0), None)
        open_nodes = []
        heapq.heappush(open_nodes, (root[2] + root[3], root[0]))
        all_nodes = {root[0]: root}
        # self.count_nodes = 0

        # While there are still nodes to explore
        while open_nodes:
            node_grid = heapq.heappop(open_nodes)[1]
            node = all_nodes[node_grid]

            # If the grid is solved, return the path
            if self.is_solved(node_grid):
                path = self.get_path(node)
                return path + self.get_final_states(path[-1])

            # self.count_nodes += 1

            # Expand node
            for state in self.next_states(node_grid):
                new_grid = state[0]
                new_piece = state[1]
                

                # Prune nodes that have already been explored
                if new_grid not in self.get_path(node):

                    # If piece is different, add 2 to cost, else add 1
                    diff_piece = node[4]!=new_piece
                    cost = node[2] + 1 + diff_piece 

                    heuristic = self.heuristic(new_grid, diff_piece)
                    new_node = (new_grid, node, cost, heuristic, new_piece)

                    # Graph search algorithm
                    if new_grid in all_nodes:
                        if cost < all_nodes[new_grid][2]:
                            all_nodes[new_grid] = new_node
                    else:
                        all_nodes[new_grid] = new_node

                        # A* algorithm (priority queue)
                        heapq.heappush(open_nodes, (all_nodes[new_grid][2] + all_nodes[new_grid][3], new_grid))

        return None


    def get_final_states(self, grid: str):
        """Get grid positions after player car's path is cleared"""
        states = []
        while True:
            grid = move(grid, self.grid_size, PLAYER_CAR, (1,0))
            if grid:
                states.append(grid)
            else:
                return states


def get_coordinates(old_grid: str, new_grid: str, cursor: tuple):
    """Returns start and end coordinates of the changed piece closest to the cursor"""

    size = int(math.sqrt(len(old_grid)))
    changed_positions = [None, None]
    piece = ''

    # Find changed positions
    for line in range(size):
        for column in range(size):
            if old_grid[size*line + column] != new_grid[size*line + column]:
                if old_grid[size*line + column] == EMPTY_TILE:
                    changed_positions[0] = (line, column)
                else:
                    changed_positions[1] = (line, column)
                    piece = old_grid[size*line + column]


    # Get movement direction
    movement = (changed_positions[0][1] - changed_positions[1][1], changed_positions[0][0] - changed_positions[1][0])

    # Normalize movement direction
    if movement[0] != 0:
        movement = (movement[0]//abs(movement[0]), movement[1])
    if movement[1] != 0:
        movement = (movement[0], movement[1]//abs(movement[1]))

    # Get piece's coordinates closest to cursor
    closest_coordinates = closest_position(old_grid, size, piece, cursor)

    # Get start and end coordinates
    start_coordinates = (closest_coordinates[0], closest_coordinates[1])
    end_coordinates = (closest_coordinates[0] + movement[0], closest_coordinates[1] + movement[1])


    return start_coordinates, end_coordinates


def get_keys_to_next_state(old_grid: str, new_grid: str, cursor: tuple, first_move: bool):
    """Returns an array of keypresses to
    move the cursor from the current grid to the next"""

    # Get target coordinates
    start, end = get_coordinates(old_grid, new_grid, cursor)
    keys = []
    is_moving = []

    # Calculate keypresses between target coordinates
    cursor_start = get_keys(cursor, start)
    start_end = get_keys(start, end)

    if cursor_start:
        if not first_move:
            keys.append(' ')
            is_moving.append(False)

        keys.extend(cursor_start)
        [is_moving.append(False) for _ in range(len(cursor_start))]
    
        keys.append(' ')
        is_moving.append(False)
    else:
        if first_move:
            keys.append(' ')
            is_moving.append(False)


    keys.extend(start_end)
    [is_moving.append(True) for _ in range(len(start_end))]


    return keys, is_moving

 
def get_keys (ini: tuple, fin: tuple):
    """Recieves initial and final cursor coordinates and 
    returns an array of keypresses to move the cursor from ini to fin"""
    lateral = ['d']*(fin[0]-ini[0]) if (ini[0]<fin[0]) else ['a']*(ini[0]-fin[0])
    vertical = ['s']*(fin[1]-ini[1]) if (ini[1]<fin[1]) else ['w']*(ini[1]-fin[1])
    return lateral + vertical


def closest_position(grid: str, size, piece, cursor: tuple):
    # Get piece's coordinates
    _piece_coordinates = piece_coordinates(grid, size, piece)

    # Find piece's coordinates closest to cursor
    closest_coordinates = _piece_coordinates[0]
    for coordinates in _piece_coordinates:
        if manhattan_distance(coordinates, cursor) < manhattan_distance(closest_coordinates, cursor):
            closest_coordinates = coordinates

    return closest_coordinates


def manhattan_distance(ini: tuple, fin: tuple):
    """Manhattan distance between two coordinates"""
    return abs(ini[0] - fin[0]) + abs(ini[1] - fin[1])

        