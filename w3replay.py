import zlib
import re

REPLAY_PATH = "E:\Warcraft III\Replay\Autosaved\Multiplayer"

# word in hex to integer
def word_to_int(text):
	first = ord(text[0])/16
	second = ord(text[0]) % 16
	third = ord(text[1])/16
	fourth = ord(text[1]) % 16
	return first*16 + second + third*16*16*16 + fourth*16*16


def read_header(replay_file):
	return replay_file.read(68)


def read_compressed_size(replay_file):
	return replay_file.read(2)


def read_uncompressed_size(replay_file):
	return replay_file.read(2)


def read_block(replay_file, compressed_size):
	return replay_file.read(word_to_int(compressed_size))


def decompress_block(block):
	decompressor = zlib.decompressobj()
	return decompressor.decompress(block)


def get_decompressed_block(file_name):
	replay_file = open(REPLAY_PATH + "\\" + file_name, "rb")
	header = read_header(replay_file)
	compressed_size = read_compressed_size(replay_file)
	uncompressed_size = read_uncompressed_size(replay_file)
	# 4 bytes of data not used
	replay_file.read(4)
	block = read_block(replay_file, compressed_size)
	return decompress_block(block)

def get_names(block):
	players = []
	# 4 bytes of data not used
	block = block[4:]
	# read host player data
	block = block[1:]
	name_id = ord(block[0]) % 16
	block = block[1:]
	name = ""
	while block[0] != "\x00":
		name += block[0]
		block = block[1:]
	players.append(name)
	block = block[3:]
	# read game name
	game_name = ""
	while block[0] != "\x00":
		game_name += block[0]
		block = block[1:]
	# game settings & map & creator name (dont decode)
	while block[:2] != "\x00\x16":
		block = block[1:]
	# read players data:
	for i in range(14):
		block = block[1:]
		if block[0]  != "\x16":
			break
		block = block[1:]
		name_id = ord(block[0]) % 16
		block = block[1:]
		name = ""
		while block[0] != "\x00":
			name += block[0]
			block = block[1:]
		players.append(name)
		block = block[6:]

	return players


def game_name(block):
	# 4 bytes of data not used
	block = block[4:]
	# read host player data
	block = block[1:]
	name_id = ord(block[0]) % 16
	block = block[1:]
	name = ""
	while block[0] != "\x00":
		name += block[0]
		block = block[1:]
	block = block[3:]
	# read game name
	game_name = ""
	while block[0] != "\x00":
		game_name += block[0]
		block = block[1:]
	return game_name

def filter_game_name(block, reg_exp):
	if re.search(reg_exp, game_name(block)) is not None:
		return get_names(block)
	else:
		return []


