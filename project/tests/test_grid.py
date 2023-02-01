import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from grid import *

grid1 = "BBoooRoooooRoooAAooooOOOoooCCCoooooo"
grid2 = "CCoooRoooooRoooAAooooOOooooooooooWWo"
size = 6

def test_coordinates():
    """Test the function coordinates"""

    assert coordinates(grid1, size) != []
    assert coordinates(grid2, size) != []
    assert coordinates(grid1, size) == [(0,0,"B"),(1,0,"B"),(5,0,"R"),(5,1,"R"),(3,2,"A"),(4,2,"A"),(3,3,"O"),(4,3,"O"),(5,3,"O"),(3,4,"C"),(4,4,"C"),(5,4,"C")]
    assert coordinates(grid2, size) == [(0,0,"C"),(1,0,"C"),(5,0,"R"),(5,1,"R"),(3,2,"A"),(4,2,"A"),(3,3,"O"),(4,3,"O"),(3,5,"W"),(4,5,"W")]

def test_pieces():
    """Lists are sorted, thus the list must be in a gramatic order"""
    assert "A" in pieces(grid1, size)
    assert "B" in pieces(grid1, size)
    assert "C" in pieces(grid1, size)
    assert "O" in pieces(grid1, size)
    assert "R" in pieces(grid1, size)
    
    assert "A" in pieces(grid2, size)
    assert "C" in pieces(grid2, size)
    assert "O" in pieces(grid2, size)
    assert "R" in pieces(grid2, size)
    assert "W" in pieces(grid2, size)

def test_piece_coordinates():

    assert piece_coordinates(grid1, size, "A") == [(3,2),(4,2)]
    assert piece_coordinates(grid1, size, "B") == [(0,0),(1,0)]
    assert piece_coordinates(grid1, size, "C") == [(3,4),(4,4),(5,4)]
    assert piece_coordinates(grid1, size, "O") == [(3,3),(4,3),(5,3)]
    assert piece_coordinates(grid1, size, "R") == [(5,0),(5,1)]

    assert piece_coordinates(grid2, size, "A") == [(3,2),(4,2)]
    assert piece_coordinates(grid2, size, "C") == [(0,0),(1,0)]
    assert piece_coordinates(grid2, size, "O") == [(3,3),(4,3)]
    assert piece_coordinates(grid2, size, "R") == [(5,0),(5,1)]
    assert piece_coordinates(grid2, size, "W") == [(3,5),(4,5)]

def test_get():
    cursor1 = (4,3)
    cursor2 = (3,4)

    assert get(grid1, size, cursor1) == "O"
    assert get(grid2, size, cursor1) == "O"
    assert get(grid1, size, cursor2) == "C"
    assert get(grid2, size, cursor2) == "o"

def test_move():
    
    piece1 = "B"
    piece2 = "W"
    piece3 = "R"
    vector1 = (0,1)
    vector2 = (1,0)
    vector3 = (0,-1)
    vector4 = (-1,0)

    assert move(grid1, size, piece1, vector1) == False
    assert move(grid1, size, piece1, vector2) == "oBBooRoooooRoooAAooooOOOoooCCCoooooo"
    assert move(grid1, size, piece1, vector3) == False
    assert move(grid1, size, piece1, vector4) == False #reached the limit of going to the left

    assert move(grid1, size, piece3, vector1) == "BBoooooooooRoooAARoooOOOoooCCCoooooo"
    assert move(grid1, size, piece3, vector2) == False
    assert move(grid1, size, piece3, vector3) == False #reached the limit of going up
    assert move(grid1, size, piece3, vector4) == False

    assert move(grid2, size, piece2, vector1) == False
    assert move(grid2, size, piece2, vector2) == "CCoooRoooooRoooAAooooOOoooooooooooWW"
    assert move(grid2, size, piece2, vector3) == False #reached the limit of going up
    assert move(grid2, size, piece2, vector4) == "CCoooRoooooRoooAAooooOOoooooooooWWoo"
