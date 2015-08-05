import w3replay
import os

# list players of all "Legion TD" games from REPLAY_PATH folder
players = []
for file_name in os.listdir(w3replay.REPLAY_PATH):
    players.append(
    	w3replay.filter_game_name(
    		w3replay.get_decompressed_block(file_name),
    		"Legion TD"))
for game in players:
	if game:
		print(game)
