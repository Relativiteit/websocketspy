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

        # tempoerary - for testing
        print(f"first player started game", id(game))
        async for message in websocket:
            print(f"first player sent", message)

    finally:
        del JOIN[join_key]


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
