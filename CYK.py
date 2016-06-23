#CYK algorythm
#Implemented by
#Carolina Lange Mello - 229354
#Gunter Hertz - 220491
#Lucas Bertolini Pizzo - 220484
#Natalia Felix Tergolina - 242241

import nltk
import sys
import string

TERMINALS = 0
VARIABLES = 1
INITIAL = 2
RULES = 3

KEY_WORDS 	= ['Terminais', 'Variaveis', 'Inicial', 'Regras']
KEY_CHARS	= [',', ' ', '{']

def get_grammar(f):
	terminals = []
	variables = []
	initial = ''
	rules = {}
	looking_for = ''
	new_key_word = ''
	aux = ''
	skip_line = False

	for line in f:
		for char in line:
			if char in string.ascii_letters:
				new_key_word += char
			else:
				if new_key_word not in KEY_WORDS:
					new_key_word = ''
					skip_line = False
				else:
					looking_for = new_key_word
					new_key_word = ''
					skip_line = True
				break
		if not skip_line:
			if looking_for == 'Terminais':
				for char in line:
					if char in string.ascii_letters:
						aux += char
					elif char in KEY_CHARS and aux:
						terminals.append(aux)
						aux = ''
					elif char == '}':
						aux = ''
						break

			if looking_for == 'Inicial':
				for char in line:
					if char in string.ascii_letters:
						initial += char
					elif char == '}':
						break

			if looking_for == 'Regras':
				rules_switch = True
				rules_left = ''
				rules_right = ''
				for char in line:
					if rules_switch:
						if char in string.ascii_letters:
							rules_left += char
						elif char == '>':
							if rules_left not in rules:
								rules[rules_left] = []
							rules_switch = False
					else:
						if char in string.ascii_letters or char == ',':
							rules_right += char
						elif char == '}':
							if rules_right not in rules[rules_left]:
								rules[rules_left].append(rules_right)
							rules_right = ''
							rules_left = ''
							break

	variables = rules.keys()
	return [terminals, variables, initial, rules]


class CYKParser:
	def __init__(self, grammar):
		self.grammar = grammar
		self.N = 0
		self.chart = None
		self.parsing = None

	def CYK(self, sentence):
		self.N = len(sentence)
		self.chart = [[[] for row in range(0,self.N+1)] for column in range(0,self.N+1)]
		self.parsing = [[[] for row in range(0,self.N+1)] for column in range(0,self.N+1)]
		pair = []
		for column in range(1,self.N+1):
			self.chart[0][column] = sentence[column-1]
			for variable in self.grammar[VARIABLES]:
				if sentence[column-1] in grammar[RULES][variable]:
					self.chart[1][column].append(variable)
					self.parsing[1][column].append(Node(variable, sentence[column-1], column+10*column))

		for row in range(2,self.N+1):
			for column in range(1,self.N+2-row):
				for inner_row in range(1,row):
					for i in range(0,len(self.chart[inner_row][column])):
						pair = [self.chart[inner_row][column][i]]
						for j in range(0,len(self.chart[row-inner_row][inner_row+column])):
							pair.append(self.chart[row-inner_row][inner_row+column][j])
							for variable in self.grammar[VARIABLES]:
								if ','.join(pair) in grammar[RULES][variable]:
									self.chart[row][column].append(variable)
									new_node = Node(variable, '', ((self.parsing[row-inner_row][inner_row+column][j].code)%10)+10*((self.parsing[inner_row][column][i].code)//10))
									new_node.left = self.parsing[inner_row][column][i]
									new_node.right = self.parsing[row-inner_row][inner_row+column][j]
									self.parsing[row][column].append(new_node)
							pair.remove(self.chart[row-inner_row][inner_row+column][j])

	def print_chart(self, chart):
		for i in range(1, self.N+1):
			for cell in self.chart[i]:
				if cell:
					print '[',
					for variable in set(cell):
						print variable, 
					print ']',
			print ''

	def print_parsing_tree(self, root, depth):
		if root:
			for i in range(self.N-depth, self.N):
				print '-',
			print root.symbol
			if not root.terminal:
				self.print_parsing_tree(root.left, depth+1)
				self.print_parsing_tree(root.right, depth+1)
			else:
				for i in range(0,self.N):
					print '-',
				print root.terminal

	def print_parse(self, parsing_chart):
		for i in range(1,self.N+1):
			print '(',
			for j in range(1,self.N+1):
				if parsing_chart[i][j]:
					print '(',
					aux = []
					last_aux = []
					for node in parsing_chart[i][j]:
						last_aux = aux
						aux = []
						aux.append([node.symbol, node.code])
						if node.terminal:
							aux.append(node.terminal)
						else:
							aux.append([node.left.symbol, node.left.code])
							aux.append([node.right.symbol, node.right.code])
						if last_aux != aux:
							last_aux = aux
							aux = []
							print node.symbol, node.code,
							aux.append([node.symbol, node.code])
							if node.terminal:
								print '->', node.terminal,
								aux.append(node.terminal)
							else:
								print '(', node.left.symbol, node.left.code, '/',
								print node.right.symbol, node.right.code, ')',
								aux.append([node.left.symbol, node.left.code])
								aux.append([node.right.symbol, node.right.code])
					print ')',
			print ')\n'

				

	def successfull(self, chart):
		return grammar[INITIAL] in self.chart[self.N][1]


class Node:
	def __init__(self, symbol, terminal, code):
		self.symbol = symbol
		self.terminal = terminal
		self.code = code
		self.left = None
		self.right = None

#sentence = ['the', 'cat', 'cat', 'coffee', 'coffee', 'barks']
sentence = nltk.word_tokenize(raw_input('Type in a sentence: '))
grammar = get_grammar(open('gramatica.txt'))
print 'Grammar: \n\n', grammar, '\n\n'
parser = CYKParser(grammar)
parser.CYK(sentence)
print 'CYK Chart:\n'
parser.print_chart(parser.chart)
if parser.successfull(parser.chart):
	print 'Sentence accepted.\n\nSuccessful trees:\n'
	for initial in parser.parsing[parser.N][1]:
		parser.print_parsing_tree(initial, 0)
	print '\nParsing:\n'
	parser.print_parse(parser.parsing)
else:
	print 'Sentence not accepted by the current grammar.\n'