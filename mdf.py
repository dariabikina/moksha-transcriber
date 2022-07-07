# This is an attempt to create a program that takes Moksha texts written in cyrillic and transcribes them.
#It is not an IPA transcription, but the system of transcription elaborated for the Moksha project
#By now it does a preliminary transcription,
# where E = "to choose between epsilon and [e]" (in the beginning of a word it has to be taken from the dictionary and cannot be predicted)
# A = "to choose between [a], epsilon and schwa" (same problem)

import sys

import re

s1 = sys.stdin.readlines()
s =''.join(s1)
s = s.lower()

#easy non-ambigious cases
tr = {'б' : 'b', 'в' : 'v', 'г' : 'g', 'д' : 'd', 'ж' : '\u017E', 
'з' : 'z', 'к' : 'k', 'м' : 'm', 'н' : 'n', 
'п' : 'p', 'с' : 's', 'т' : 't', 'у' : 'u', 'ф' : 'f', 
'ц' : 'c', 'ч' : '\u010D', 'ш' : '\u0161', 'щ' : '\u0161\u010D', 'ы' : 'i'}

sonor = {'л' : 'l', 'р' : 'r'}

word_end = ['.', ' ', '!', ',', ':', ';', '?', '"', ')']

paired_cons = ['н', 'д', 'т', 'з', 'с', 'ц', 'р', 'л']

paired_cons_tr = ['n', 'd', 't', 'z', 'c', 's', 'r', 'l']

vowels = ['a', 'i', 'o', 'u', 'e', '\u025B']

converted_line = ''
	
for index, char in enumerate(s):
	transchar = ''

# the following part makes devoiced sonorants; 
# in cyrillic Moksha writing they are written with 2 or 3 symbols (лх, рх, льх, рьх, йх, хь)
	if char in sonor:
		if len(s) > index+1:
			if s[index+1] == 'х':
				transchar = sonor[char] + '\u0325'
			elif ((s[index+1] == 'ь') & (s[index+2] == 'х')):
				transchar = sonor[char] + '\u0325\u2019'
			else:
				transchar = sonor[char]
		else:
			transchar = sonor[char]
	elif char == 'й':
		if len(s) > index+1:
			if s[index+1] == 'х':
				transchar = 'j\u030A'
			else:
				transchar = 'j'
		else:
			transchar = 'j'
#and this deletes the extra symbols
	elif char == 'ь':
		if ((len(s) > index+1) & (index > 1)):
			if ((s[index-1] in sonor) & (s[index+1] == 'х')):
				transchar = ''
			if s[index-1] == 'х':
				transchar = ''
			else:
				transchar = '\u2019'
	elif char == 'х':
		if ((len(s) > index+1) & (index > 1)):
			if s[index-1] in sonor:
				transchar = ''
			elif ((s[index-1] == 'ь') & (s[index-2] in sonor)):
				transchar = ''
			elif s[index-1] == 'й':
				transchar = ''
			elif s[index+1] == 'ь':
				transchar = 'j\u030A'
			else:
				transchar = 'x'

# Then we deal with vowel symbols
	elif char == 'а':
		if len(s) > index+ 1:
			if s[index+1] not in word_end:
				transchar = 'a'
			else:
				transchar = 'A' #at the end of the word it can be either a or schwa
	elif char == 'я':
		if len(s) > index+1:
			if s[index+1] in word_end:
				if s[index-1] in paired_cons:
					transchar = '\u2019a'
				else:
					transchar = 'A'
			elif s[index-1] in paired_cons:
					transchar = '\u2019a'
			elif s[index-1] == ' ':
				transchar = 'ja'
			else:
				transchar = '\u025B'
	elif char == 'е':
		if len(s) > index+1:
			if s[index+1] in word_end:
				if s[index-1] in paired_cons:
					transchar = '\u2019A'
				else:
					transchar = 'A'
			else: 
				if s[index-1] == ' ':
					transchar = 'je'
				elif s[index-1] in paired_cons:
					transchar = '\u2019e'
				else:
					transchar = 'e'
	elif char == 'о':
		transchar = 'o'
	elif char == 'ю':
		if len(s) > index+1:
			if s[index-1] == ' ':
				transchar = 'ju'
			elif s[index-1] in paired_cons:
				transchar = '\u2019u'
			else:
				transchar = 'u'
	elif char == 'ё':
		if len(s) > index+1:
			if s[index-1] == ' ':
				transchar = 'jo'
			elif s[index-1] in paired_cons:
				transchar = '\u2019o'
			else:
				transchar = 'o'
	elif char == 'э':
		if len(s) > index+1:
			if s[index-1] == ' ':
				transchar = 'E'
			else:
				transchar = 'e'
	elif char == 'и':
		if len(s) > index+1:
			if s[index-1] in paired_cons:
				transchar = '\u2019i'
			else:
				transchar = 'i'
	elif char in tr:
		transchar = tr[char]
	else:
		transchar = char
	converted_line += transchar


#The following part replaces "o" and "e" in non-first syllables with schwa

tokens = converted_line.split(' ')
for token in tokens:
	number_syllables = 0
	tok_new = ''
	for index, i in enumerate(token):
		if i in vowels:
			number_syllables = number_syllables +1
			if len(token) > index+1:
				
				if (i == 'o'):
					if (number_syllables > 1):
						i = '\u0259'
						tok_new+=i
					else:
						tok_new+=i
				elif (i == 'e') & (number_syllables > 1) & (token[index-2] in paired_cons_tr) & (token[index-1] == '\u2019'):
					i = '\u0259'
					tok_new+=i
				else:
					tok_new+=i
			else: 
				tok_new +=i
#Affricatization of sibilants after n
		elif (i == 's') & (token[index-1] == 'n'):
			i = 'c'
			tok_new+=i
		elif (i == '\u0161') & (token[index-1] == 'n'):
			i = '\u010D'
			tok_new+=i
		else:
			tok_new+=i
	converted_line = converted_line.replace(token, tok_new)
fd = open('mdf_transribed.txt', 'w+')
fd.write(converted_line)
fd.close()
			

