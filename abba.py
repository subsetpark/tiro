#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, re, configparser, regnet
from rules_generator import generate_rules

class Abbreviation(object):
	"""
	Objects which represent abbreviation glyphs and can be regexped.
	"""

	def __init__(self, name, pattern, codepoint):
		self.codepoint = codepoint
		self.pattern = pattern
		self.name = name
			
	def __repr__(self):
		return self.name
	
	def __unicode__(self):
		return self.codepoint
			
class Abbreviation_dictionary(object):
	"""
	This object contains sequences of glyph transformations which it
	can run on text objects.
	
	>>> file = open('tna.ini')
	>>> abb_set = load_rules(file)
	>>> abba = Abbreviation_dictionary(abb_set)
	
	"""
	def __init__(self, config):
		self.abb_sequences = []
		self.lookup_table = {}
		# begin creating unicode characters at the beginning 
		# of the private use space
		self.pool = iter(range(57344,63743))
		rep_search = re.compile("_rep$")
		for section in config.sections():
			has_a_rep = False
			codepoint = chr(next(self.pool))
			self.add_to_dict(section, regnet.Regnet(config[section]['pattern']), codepoint)
			for option in config.options(section):
				# Go through each section's options. If it has _rep in it,
				# It's a representation method. Add it to the lookup.
				if re.search(rep_search, option):
					has_a_rep = True
					self.add_to_lookup(codepoint, section, option=option, 
						value=self.parse_rules(list(config[section][option])))
			if not has_a_rep: 
				self.add_to_lookup(codepoint, section)						
	
	def add_to_lookup(self, codepoint, section, option=None, value=None):
		"""
		Add a representation method to the reverse lookup table as we create
		the dictionary.
		"""
		if not codepoint in self.lookup_table:
			self.lookup_table[codepoint] = { 'name': section, option: value}
		self.lookup_table[codepoint][option] = value
		
	def lookup(self, char):
		return self.lookup_table[char]['name']
		
	def uni_lookup(self, char):
		"""
		Return unicode representation of abbreviation
		"""
		if 'uni_rep' in self.lookup_table[char]:
			return self.lookup_table[char]['uni_rep']
		else:
			return self.lookup_table[char]['name']
			
	def add_to_dict(self, section, regnet, serial):
		"""
		Given the makings of an abbreviation, create a new object
		and add it to the sequences list.
		"""
		# build abb_sequences to the number of prec levels
		while len(self.abb_sequences) < regnet.prec + 1:
			self.abb_sequences.append([])
		# add a new abbreviation object to the correct prec sequence
		self.abb_sequences[regnet.prec].append(Abbreviation(
								section, regnet.pattern, serial))
								
	def parse_rules(self, value):
		"""
		Read the formatted .ini looking for references to unicode characters. 
		Recurse through the uni_rep, replacing codepoint references as you go.
		"""
		
		if '{' not in value or value[value.index('{')+5] is not '}':
			return ''.join(value)
		else:
			i = value.index('{')
			value[i:i+6] = chr(int('0x' + ''.join(value[i+1:i+5]), 16))
			return ''.join(self.parse_rules(value))
				
	def lookup_and_substitute(self, text, sequence):
		"""
		Performs simple regexp subs given a sequence of transforms and a text.
		Each transform subs in a dynamically generated unicode 
		control character.
		"""
		for abbreviation in sequence:
			text = re.sub(abbreviation.pattern, abbreviation.codepoint, text) 
		return text	
	
	def abbreviate_text(self, text):
		"""
		Runs each sequence of transforms in the order they were loaded into the
		controller.
		"""
		working_text = text
		for sequence in self.abb_sequences:
			working_text = self.lookup_and_substitute(working_text, sequence)
		return working_text
	
	def generate_legend(self):
		"""
		Generate a unicode legend to print before the text. Right now
		it's brittle because it assumes unicode renderer.
		"""
		legend = ""
		for key in self.lookup_table.keys():
			try:
				legend += "{}: '{}'\n".format(self.lookup_table[key]['uni_rep'], self.lookup_table[key]['name'])
			except KeyError:
				legend += "{}: '{}'\n".format(self.lookup_table[key]['name'], self.lookup_table[key]['name'])
		return legend

def load_rules(filename):
	"""
	Build a config object from the provided file
	"""
	config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation(),allow_no_value=True)
	config.read_file(filename)
	return config

def base_decode(text, abb_dict):
	"""
	Take abbreviated text with control entities and renders them in ASCII 
	"""
	working_text = list(text)
	render = ""
	for index, char in enumerate(working_text):
		if 63743 > ord(char) >= 57344:
			render += abb_dict.lookup(char)
		else:
			render += char
	return render
		
def uni_decode(text, abb_dict):
	"""
	Take abbreviated text with control entities and renders them in unicode 
	"""
	working_text = list(text)
	render = ""
	for char in working_text:
		if 63743 > ord(char) >= 57344:
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
	
	# Parse command line arguments
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-g', '--generate', help="""
	Analyze a text for frequency and generate abbreviations on the fly.""", action="store_true")
	parser.add_argument("--ruleset", help="""
					The ruleset to use. Uses The New Abbreviations if
					none is supplied.""", default="tna.ini")
	parser.add_argument('-i', '--infile', type=argparse.FileType('r'))
	parser.add_argument('-t', '--text', nargs="+", help="""	The text to operate on.""")	
	parser.add_argument('-r', '--render', help="""
					Render method. Accepts 'unicode' or 'base'.
					""", default='unicode')
	parser.add_argument('-l', '--legend', help="""
					Print a legend at the top of the text.
					""", action="store_true") 
	args = parser.parse_args()
	
	# Determine input method
	if not sys.stdin.isatty():
		text = sys.stdin.read().strip("\r\n")
	elif args.infile:
		text = (args.infile).read()
	elif args.text:
		text = " ".join(args.text)
	else:
		exit("No input received. Run 'python3 abba.py -h' for more information.")
	
	# Get a ruleset and use it to generate an abbreviation dictionary
	if args.generate:
		abb_set = generate_rules(text)
	else:
		ruleset = open(args.ruleset)
		abb_set = load_rules(ruleset)
	abba = Abbreviation_dictionary(abb_set)
	
	# Generate a legend
	if args.legend:
		legend = (abba.generate_legend())
	
	# Choose the rendering method	
	if args.render == "unicode":
		if args.legend: print(legend)
		print(uni_decode(abba.abbreviate_text(text), abba))
	else:
		if args.legend: print(legend)
		print(base_decode(abba.abbreviate_text(text), abba))
