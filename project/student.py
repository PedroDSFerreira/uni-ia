"""STUDENT EXPERIMENTS."""
"""
game -> GAME_SPEED
game -> CRAZY_STEP
server -> timeout
"""
import asyncio
import getpass
import json
import os
from time import time
from agent import *
import websockets


FPS = 10 # Game speed

async def agent_loop(server_address="localhost:8000", agent_name="student"):
    """Example client loop."""
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        # Inicialization
        agent = Agent('oooooooooooooooooooooooooooooooooooo')
        missed_messages = 0
        states = []
        
        while True:
            try:
                # Consume missed messages 
                for _ in range(missed_messages):
                    await websocket.recv()

                # Get server info
                response = json.loads(
                    await websocket.recv()
                )
                start_time = time()
                
                x, y = response.get('cursor')
                cursor = (x, y)
                _, grid, _ = response.get('grid').split(' ')
                

                # Check if grid changed
                # (crazy car or new level)
                if grid != agent.grid: 
                    agent = Agent(grid)
                    states = agent.solve()
                    keys = []

                    # Remove current state from states
                    states.pop(0)
                    first_move = True
                    is_selected = False



                if not keys:
                    # Get next state
                    next_state = states.pop(0)
                    keys, is_selected = get_keys_to_next_state(agent.grid, next_state, cursor, first_move)
                    first_move = False
                key = keys.pop(0)
                flag = is_selected.pop(0)

                if flag:
                    agent = Agent(next_state)

                # Calculate missed messages to consume
                end_time = time()
                missed_messages = int((end_time - start_time) * FPS)

                # Send keypresses
                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )

                

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return



# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
