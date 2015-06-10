#CYK algorythm
#Implemented by
#Carolina Lange Mello - 
#Gunter Hertz -
#Lucas Bertolini Pizzo - 220484
#Natalia Felix Tergolina - 242241

import nltk
import sys
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
						if char in string.ascii_letters:
							rules_right += char
						elif char == ',' or char == '}':
							if rules_right not in rules[rules_left]:
								rules[rules_left].append(rules_right)
							rules_right = ''
							if char == '}':
								rules_left = ''
								break

	return [terminals, variables, initial, rules]
        

'''
def CYK(
    a,  		# cadeia de caracteres [1 to n] a ser testada
    R, 			# gramática [1 to r] contendo símbolos terminais e não-terminais
    initial,    # símbolos de início da gramática
    P			# vetor [n,n,r] de booleanos inicializado em Falso
    ):
    for char in a:
        for Producao:R_j \to char:
            P[i,1,j] = Verdadeiro
    for i in xrange(2, n+1):
        for j in xrange(1, n-i+2):
            for k in xrange(1, i):
                for Produção(R_A \to R_B R_C):
                    if P[j,k,B] and P[j+k,i-k,C]:
                        P[j,i,A] = Verdadeiro
    for x in initial:
        if P[1,n,x] = True:
            return "membro da linguagem"
        else
            return "não-membro da linguagem"
'''


sentence = nltk.word_tokenize(raw_input('Type in a sentence: '))
print sentence
grammar = get_grammar(open('gramatica.txt'))
terminals = grammar[0]
variables = grammar[1]
initial = grammar[2]

print grammar
