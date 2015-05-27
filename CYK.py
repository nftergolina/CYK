#CYK algorythm
#Implemented by
#Carolina Lange Mello - 
#Gunter Hertz -
#Lucas Bertolini Pizzo -
#Natalia Felix Tergolina - 242241

import string

KEY_WORDS 	= ['Terminais', 'Variaveis', 'initial', 'Regras']
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
		#get key word
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
			#get terminals
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

			#get variables
			if looking_for == 'Variaveis':
				for char in line:
					if char in string.ascii_letters:
						aux += char
					elif char in KEY_CHARS and aux:
						variables.append(aux)
						aux = ''
					elif char == '}':
						aux = ''
						break

			#get initial
			if looking_for == 'initial':
				for char in line:
					if char in string.ascii_letters:
						aux += char
					elif char == '}':
						initial = aux
						aux = ''
						break

			#get rules
			if looking_for == 'Regras':
				pass

	return [terminals, variables, initial, rules]
        

def get_phrase():
	pass

def CYK():
	pass



grammar = get_grammar(open('gramatica.txt'))
terminals = grammar[0]
variables = grammar[1]
initial = grammar[2]

print grammar
