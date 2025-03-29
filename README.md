# Spotify Automation
This is the first draft of a tool to automate curating a library of music on Spotify.

## Setup
To use the Spotify Web API, you need to provide a client_id and a client_secret, for which you need to have a Spotify Application. You can create te Application by following the steps described in [the Spotipy documentation](https://spotipy.readthedocs.io/en/2.25.1/). Or, if you know me, ask me if I'm willing to share mine with you :)

If you create your own Spotify application, make sure to add http://127.0.0.1:8080 as a redirect URI in your app's settings. This is needed for authorization.

Go to source/shell_scripts/set_variables.sh and insert your client_id and client_secret. Run set_variables.sh each time you run any API calls from a new environment to ensure authorization.

To test if authorization works, you can run

``python3 source/executables/get_track_metadata.py 180OrhCzFdX7Pyhri6AerI``

to request the metadata of "California King". It should print the metadata to the terminal.