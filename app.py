#!/usr/bin/env python
import json
import asyncio
import logging
import itertools
import websockets
import secrets

from websockets.asyncio.server import serve
from connect4 import PLAYER1, PLAYER2, Connect4

JOIN = {}


async def watch(websocket, watch_key):

    ...
    connected.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        connected.remove(websocket)
    # 3 cases that will close the connection for a spectator
    # 1. close connection win event
    # 2. close connection spectator closes browser
    # 3. close connection in case of a network failure


async def play(websocket, game, player, connected):
    websocket.restart()

# implement coroutine for 2 connectiong, restart websocket


async def error(websocket, message):
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))


async def join(websocket, join_key):
    # Find the Connect Four game.
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found")
        return

    # Register to receive moves from this game.
    connected.add(websocket)
    try:
        # Temporary - for testing
        await play(websocket, game, PLAYER2, connected)

    finally:
        connected.remove(websocket)


async def start(websocket):
    # Initialize a Connect Four game, the set of WebSocket connections
    # receiving moves from this game, and secret access token.
    game = Connect4()
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    try:
        # Send the secret access token to the browser of the first player,
        # where it'll be used for building a "join" link
        event = {
            "type": "init",
            "join": join_key,
        }
        await websocket.send(json.dumps(event))

        # Temporary - for testing
        await play(websocket, game, PLAYER1, connected)

    finally:
        del JOIN[join_key]


async def handler(websocket):
    # Receive and parse the "init" event from the UI.
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if "join" in event:
        # Second player joins an existing game.
        await join(websocket, event["join"])
    else:
        # First player starts a new game
        await start(websocket)


async def handler(websocket):
    # enable logging
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)
    # Initialize a connect four game.
    game = Connect4()
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    # Receive and parse the "init" event from the UI.
    message = await websocket.recv()
    event = json .loads(message)
    assert event["type"] == "init"

    # First player starts a new game
    await start(websocket)

    try:
        ...
    finally:
        del JOIN[join_key]

    join_key = ...

    # Find the Connect Four game.
    game, connected = JOIN[join_key]

    # Register to receive moves from this game
    connected.add(websocket)
    try:
        ...
    finally:
        connected.remove(websocket)

    # Players take alternate turns, using the same browser.
    # switch this shit out for a simple algo
    turns = itertools.cycle([PLAYER1, PLAYER2])
    player = next(turns)

    async for message in websocket:
        # Parse a "play" event from the UI
        event = json.loads(message)
        assert event["type"] == "play"
        column = event["column"]

        try:
            # Play the move
            row = game.play(player, column)
        except ValueError as exc:
            # Send an "error" event if the move was illegal.
            event = {
                "type": "error",
                "message": str(exc),
            }
            await websocket.send(json.dumps(event))
            continue
        # Send a "play" event to update the UI

        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row,
        }
        await websocket.send(json.dumps(event))
        # If move is winning, send a "win" event.
        if game.winner is not None:
            event = {
                "type": "win",
                "player": game.winner,
            }
            await websocket.send(json.dumps(event))

        # Alternate turns.
        player = next(turns)


async def main():
    async with serve(handler, "", 8001):
        await asyncio.get_running_loop().create_future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
