# How to run project 

## WebUI 
open several shells, activate the virtual environment with

` source Scripts/Activate` 

Navigate to the directory containing the python and .js files. 

`python -m http.server`

now the server is running with the main board. 

## Server

run the python server with the following commmand. 

`python app.py` 
you won't be able to see if it's running unless you add a print statement or if you are not able to make changes to the server. 

`python -m websockets ws://localhost:8001/`

