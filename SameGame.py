# -*- coding: latin-1 -*-
#-----------------------------------------------------------------------------------------------
# Projeto-IA
#	Inteligência Artificial
#	1ª parte do Projecto
#	IST @ 2017/2018 
#
#	Grupo 25
#		83448 - Dorin Gujuman
#		83504 - Manuel José Ribeiro Vidigueira
#-----------------------------------------------------------------------------------------------
#	  /$$$$$$                                     /$$$$$$                                   
#	 /$$__  $$                                   /$$__  $$                                  
#	| $$  \__/  /$$$$$$  /$$$$$$/$$$$   /$$$$$$ | $$  \__/  /$$$$$$  /$$$$$$/$$$$   /$$$$$$ 
#	|  $$$$$$  |____  $$| $$_  $$_  $$ /$$__  $$| $$ /$$$$ |____  $$| $$_  $$_  $$ /$$__  $$
#	 \____  $$  /$$$$$$$| $$ \ $$ \ $$| $$$$$$$$| $$|_  $$  /$$$$$$$| $$ \ $$ \ $$| $$$$$$$$
#	 /$$  \ $$ /$$__  $$| $$ | $$ | $$| $$_____/| $$  \ $$ /$$__  $$| $$ | $$ | $$| $$_____/
#	|  $$$$$$/|  $$$$$$$| $$ | $$ | $$|  $$$$$$$|  $$$$$$/|  $$$$$$$| $$ | $$ | $$|  $$$$$$$
#	 \______/  \_______/|__/ |__/ |__/ \_______/ \______/  \_______/|__/ |__/ |__/ \_______/
#-----------------------------------------------------------------------------------------------
from utils import *
from search import *
#from termcolor import *
#TEMP

test = [[1,2,2,3,3],[2,2,2,1,3],[1,2,2,2,2],[1,1,1,1,1]]
b1 = [[0,0,0,0,0],[0,2,3,3,0],[1,2,1,3,0],[2,2,2,2,0]] 
large = [[1,3,2,1,2,1,2,2,1,2,2,1,1,3,1],[1,3,3,2,1,2,2,2,3,1,2,1,2,3,1],[1,1,1,2,3,2,3,3,2,2,3,1,1,3,1],[1,2,2,2,3,3,3,3,1,2,1,2,1,3,2],[1,3,1,3,2,2,2,2,3,1,1,2,3,2,1],[1,1,2,2,2,1,1,3,2,1,2,3,1,3,1],[3,1,3,2,2,2,3,3,3,1,3,3,2,1,1],[3,2,1,2,1,3,1,2,1,2,3,1,1,3,3],[2,3,1,2,3,3,1,2,3,3,3,2,1,1,1],[2,2,1,1,2,1,2,2,1,1,3,2,2,2,2]]

#	TIPOS

# TAI color
# sem cor = 0
# com cor > 0
def get_no_color():
	return 0
def no_color (c):
	return c==0
def color (c):
	return c > 0

# TAI pos
# Tuplo (l, c)
def make_pos (l, c):
	return (l, c)
def pos_l (pos):
	return pos[0]
def pos_c (pos):
	return pos[1]

#Tipo group
#O tipo group corresponde a uma lista de peças adjacentes com a mesma cor. A sua representação
#interna é uma lista de elementos do tipo pos.

def get_adjacent(board, pos):
	""" retorna uma lista com elementos do tipo pos com elementos adjacentes da mesma cor indicada """
	adj = []
	l, c = pos_l(pos), pos_c(pos)

	for x, y in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
		if 0 <= c + x < board_width(board) and 0 <= l + y < board_height(board):
			test_pos = make_pos(l+y, c+x)
			if board_get_color(board, pos) == board_get_color(board, test_pos):
				adj.append(test_pos)
	return adj

def board_get_group(board, pos):
	stack = set([pos])
	group = set()

	while len(stack) > 0:
		curr = stack.pop()
		for adjacent in get_adjacent(board, curr):
			if adjacent not in group:
				stack.add(adjacent)
		group.add(curr)

	return list(group)

def board_find_groups(board):
	"""devolve uma lista com os grupos de peças que se podem encontrar no tabuleiro, 
	sendo um grupo de peças uma lista com uma ou mais peças."""

	groups = []
	visited = set()

	for c in range(board_width(board)):
		for l in range(board_height(board)):
			curr = make_pos(l, c)
			if curr not in visited:
				curr_group = board_get_group(board, curr)
				groups.append(curr_group)
				for pos in curr_group:
					visited.add(pos)
	return groups


def board_remove_group(board, group):
	"""remove  o  grupo  do  tabuleiro fazendo
	a  compactação  vertical  e  horizontal  das  peças."""
	new_board = [list(x) for x in board] #copy the board
	for pos in group:
		board_del_color(new_board, pos)

	new_board = list(map(list, zip(*new_board))) #this transposes the matrix
	for row in new_board:
		row.sort(key=lambda x: x != 0) #this pushes all zeroes to left

	new_board.sort(key=lambda x: x.count(0) == board_height(board)) 

	new_board = list(map(list, zip(*new_board)))
	return new_board

	#primeiro transpomos para compactar verticalmente

#Tipo board
#O tipo tabuleiro representa o tabuleiro de um jogo de Same Game. A representação interna de um
#jogo de Same Game é uma lista de listas, em que as sublistas correspondem às linhas do tabuleiro do
#jogo. Uma sublista tem uma representação do conteúdo da linha. O conteúdo de uma posição é
#representado pelo tipo color. O canto superior esquerdo corresponde à posição (0,0). O canto
#inferior direito corresponde à posição (<nºlinhas>-1,<nºcolunas>-1).

def board_width(board):
	return len(board[0])
def board_height(board):
	return len(board)
def board_get_color(board, pos):
	return board[pos_l(pos)][pos_c(pos)]
def board_del_color(board, pos):
	board[pos_l(pos)][pos_c(pos)] = 0
def board_print(board):
	print_table(board, sep=' ')
"""
def board_print_board(board):
	colors=["grey", "red", "green","yellow", "blue", "magenta", "cyan"]
	colors2 = ["on_grey", "on_red", "on_green","on_yellow", "on_blue", "on_magenta", "on_cyan"]
	numbers = "  "
	for i in range(board_width(board)):
		numbers += str(i).rjust(2)
	print(numbers)
	a = 0
	for line in board:
		print(str(a).rjust(2), end="")
		a += 1
		for i in line:
			cprint("  ", colors[int(i)],colors2[int(i)], end="")
		print("")
"""
class sg_state:
	def __init__(self, init_board):
		self.board = init_board
		self.current_groups = board_find_groups(init_board)

	def __lt__(self, other):
		return len(self.board) < len(other.board)

	def remove_group(self, group):
		return sg_state(board_remove_group(self.board, group))

	def get_actions(self):
		return [group for group in self.current_groups if len(group) > 1]


class same_game(Problem):
	def __init__(self, board):
		Problem.__init__(self, sg_state(board), sg_state([[0 for i in range(board_width(board))] for i in range(board_width(board))]))
	def actions(self, state):
		return state.get_actions()
	def result(self, state, action):
		return state.remove_group(action)
	def h(self, node):
		return 1