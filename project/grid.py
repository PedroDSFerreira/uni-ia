EMPTY_TILE = "o"
WALL_TILE = "x"
PLAYER_CAR = "A"


def coordinates(grid, size):
    """Representation of ocupied grid positions through tuples x,y,value."""
    _coordinates = []
    for i, pos in enumerate(grid):
        if pos != EMPTY_TILE:
            _coordinates.append((i % size, i // size, pos))
    return _coordinates


def pieces(grid, size):
    """Pieces's chars"""
    return list(set([p for (x, y, p) in coordinates(grid, size) if p ]))


def piece_coordinates(grid, size, piece: str):
    """List coordinates holding a piece."""
    return [(x, y) for (x, y, p) in coordinates(grid, size) if p == piece]


def get(grid, size, cursor: tuple):
    """Return piece at cursor position."""
    if 0 <= cursor[0] < size and 0 <= cursor[1] < size:
        return grid[int(size * cursor[1] + cursor[0])]
    
    
def move(grid, size, piece: str, direction: tuple):
    """Move piece in direction given by a vector."""
    if piece == WALL_TILE:
        return False

    piece_coord = piece_coordinates(grid, size, piece)
    # print(str(_piece) for _piece in piece_coord)

    # Don't move vertical pieces sideways
    if direction[0] != 0 and any([grid[line*size:line*size+size].count(piece) == 1 for line in range(size)]):
        return False
    # Don't move horizontal pieces up-down
    if direction[1] != 0 and any([grid[line*size:line*size+size].count(piece) > 1 for line in range(size)]):
        return False

    def sum(a: tuple, b: tuple):
        return (a[0] + b[0], a[1] + b[1])

    for pos in piece_coord:
        if not get(grid, size, sum(pos, direction)) in [piece, EMPTY_TILE]:
            return False

    new_grid = list(grid)

    for pos in piece_coord:
        new_grid[size * pos[1] + pos[0]] = EMPTY_TILE

    for pos in piece_coord:
        new_pos = sum(pos, direction)
        new_grid[size * new_pos[1] + new_pos[0]] = piece

    return "".join(new_grid)