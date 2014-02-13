#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, re, json, warnings, collections
from abba_generator import generate_rules

class Abbreviation(object):
	"""
	Objects which represent abbreviation glyphs and can be regexped.
	"""
	def __init__(self, abb_data, serial):
		self.codepoint = chr(serial)
		self.pattern = abb_data['pattern']
		self.name = abb_data['name']
		self.uni_rep = abb_data.get('uni_rep',"")
		
	
	def uni_report(self):
		return self.uni_rep
		
			
	def __repr__(self):
		return self.name
	
	def __unicode__(self):
		return self.codepoint
			
class Abbreviation_dictionary(object):
	"""
	This object contains sequences of glyph transformations which it
	can run on text objects.
	"""
	
	def add_to_lookup(self, abbreviation):
		self.lookup_table[abbreviation.codepoint] = abbreviation
		
	def lookup(self, char):
		return self.lookup_table[char].name
		
	def uni_lookup(self, char):
		return self.lookup_table[char].uni_report()
		
	def add_sequence(self, pattern_sequence):
		new_sequence = []
		# construct a list of all abbreviation in a given set,
		# then append them to the list of all sequences.
		for pattern in pattern_sequence['patterns']:
			# create the pattern here.
			new_abbreviation = Abbreviation(pattern, self.serial)
			new_sequence.append(new_abbreviation)
			self.add_to_lookup(new_abbreviation)
			self.serial += 1
		self.abb_sequences.append(new_sequence)
	
	def __init__(self, sequence_set):
		self.abb_sequences = []
		self.lookup_table = {}
		# begin creating unicode characters at the beginning 
		# of the private use space
		self.serial = 57344
		for sequence in sequence_set:
			self.add_sequence(sequence)
	
	def lookup_and_substitute(self, text, sequence):
		"""
		Performs simple regexp subs given a sequence of transforms and a text.
		Each transform subs in a dynamically generated unicode 
		control character.
		"""
		working_word = text
		for abbreviation in sequence:
			working_word = re.sub(r'(?i)'+abbreviation.pattern, abbreviation.codepoint, working_word) 
		return working_word	
	
	def abbreviate_text(self, text):
		"""
		Runs each sequence of transforms in the order they were loaded into the
		controller.
		>>> abb_set = load_rules("tna.json")
		>>> abba = Abbreviation_dictionary(abb_set)
		>>> print(uni_decode(abba.abbreviate_text("this"), abba))
		ðs
		>>> print(uni_decode(abba.abbreviate_text("we are cömbined"), abba))
		w̃ ar̯ cömbin̳
		>>> print(uni_decode(abba.abbreviate_text("Don't forget"), abba))
		Don't foꝛget
		>>> print(uni_decode(abba.abbreviate_text(""), abba))
		<BLANKLINE>
		
		"""

		working_text = text
		for sequence in self.abb_sequences:
			working_text = self.lookup_and_substitute(working_text, sequence)
		return working_text


	
def load_rules(filename):
	input = open(filename)
	return json.load(input)

def base_decode(text, abb_dict):
	"""
	Takes abbreviated text with unicode entities and renders them in ASCII 
	"""
	working_text = list(text)
	render = u""
	for index, char in enumerate(working_text):
		if ord(char) >= 57344:
			render += abb_dict.lookup(char)
		else:
			render += char
	return render
		
def uni_decode(text, abb_dict):
	"""
	Takes abbreviated text with unicode entities and renders them in unicode 
	"""
	working_text = list(text)
	render = u""
	for char in working_text:
		if ord(char) >= 57344:
			if abb_dict.uni_lookup(char):
				render += abb_dict.uni_lookup(char)
			else:
				render += abb_dict.lookup(char)
		else:
			render += char
	return render
	

if __name__ == "__main__":
	
	import doctest
	doctest.testmod()
	
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-g', '--generate', help="""
	Analyze a text for frequency and generate abbreviations on the fly.""", action="store_true")
	parser.add_argument("--ruleset", help="""
					The ruleset to use. Uses The New Abbreviations if
					none is supplied.""", default="tna.json")
	parser.add_argument('-i', '--infile', type=argparse.FileType('r'))
	parser.add_argument('-t', '--text', nargs="+", help="""	The text to operate on.""")	
	args = parser.parse_args()
	
	if not sys.stdin.isatty():
		text = sys.stdin.read().strip("\r\n")
	elif args.infile:
		text = (args.infile).read()
	elif args.text:
		text = " ".join(args.text)
	else:
		exit("No input received. Run 'python3 abba.py -h' for more information.")
		
	ruleset = args.ruleset
	
	if args.generate:
		abb_set = generate_rules(text)
	else:
		abb_set = load_rules(ruleset)
	abba = Abbreviation_dictionary(abb_set)
	
	print(uni_decode(abba.abbreviate_text(text), abba))
