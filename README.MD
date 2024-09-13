# How to run project 

# WebUI 
open several shells, activate the virtual environment with

` source Scripts/Activate` 

Navigate to the directory containing the python and .js files. 

`python -m http.server`

now the server is running with the main board. 

## Transmitting from browser to the server
add "play" events in the browser, addEventListener("click",{{target}} => ....)
figures out what column is clicked, and then this is serialized and sent to the server.

# Server
run the python server with the following commmand. 

`python app.py` 
you won't be able to see if it's running unless you add a print statement or if you are not able to make changes to the server. 

`python -m websockets ws://localhost:8001/`

you get a prompt and have to press enter to enter a message. 

## Transmitting from the server to the browser
Listening to `message` events from the server and deserialize it from JSON.

# Share game state
When you run a single server process you can share a global state. 
Keep track of websocket connection, store both in the same set, use identifiers for the moves of both / all players.


