#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, re, configparser, collections
import regnet
import rules_generator
import render

"""
Abba: The Abbreviation engine

This application works in several stages:

1. It reads abbreviation definitions written in the regnet markup from a .ini file.
2. It compiles each abbreviation definition into a regnet object in order to obtain a regexp and a precedence ranking.
3. It builds an abbreviation dictionary by:
	a. creating a new abbreviation object using the regexp and putting it into the correct order indicated by the precedence ranking.
	b. adding that abbreviation's rendering information to a lookup table.
4. It runs through a provided text, replacing matching patterns with single unicode control codepoints that are linked to abbreviation objects.
5. It renders the text according to the user's preference, referencing the control codepoints to the desired render method.

"""

# Objects which represent abbreviation glyphs and can be regexped.
Abbreviation = collections.namedtuple("Abbreviation", "name, pattern, codepoint")

class Abbreviation_dictionary(object):
	"""
	This object contains sequences of glyph transformations which it
	can run on text objects.
	"""
	def __init__(self, config):
		self.abb_sequences = []
		self.lookup_table = {}
		# begin creating unicode characters at the beginning 
		# of the private use space
		self.pool = iter(range(57344,63743))
		rep_search = re.compile("_rep$")
		# Read through the config file, pulling out abbreviation schemae
		for section in config.sections():
			has_a_rep = False
			# Pull a control character from the pool
			codepoint = chr(next(self.pool))
			# Analyze the regnet markup and move it into the abbreviation dict
			self.add_to_dict(section, regnet.Regnet(config[section]['pattern']), codepoint)
			for option in config.options(section):
				# Go through each section's options. If it has _rep in it,
				# It's a representation method. Add it to the lookup.
				if re.search(rep_search, option):
					has_a_rep = True
					self.add_to_lookup(codepoint, section, option=option, 
						value=regnet.parse_regnet(list(config[section][option])))
			if not has_a_rep: 
				self.add_to_lookup(codepoint, section)						
			
	def add_to_lookup(self, codepoint, section, option=None, value=None):
		"""
		Add a representation method to the reverse lookup table as we create
		the dictionary.
		"""
		if codepoint not in self.lookup_table:
			self.lookup_table[codepoint] = {'name': section}
			if option and value:
				self.lookup_table[codepoint][option] = value
		else:
			self.lookup_table[codepoint][option] = value
		
	def lookup(self, char, option='uni_rep'):
		"""
		Generic accessor for the lookup table.
		"""
		try:
			return self.lookup_table[char][option]
		except KeyError:
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
			name = self.lookup(key, 'name')
			rep = self.lookup(key)
			legend += "{}: '{}'\n".format(rep, name)
		return legend

def load_rules(filename):
	"""
	Build a config object from the provided file
	"""
	config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation(),allow_no_value=True)
	config.read_file(filename)
	return config
	

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
		abb_config = rules_generator.Generator(text).generate_rules()
	else:
		with open(args.ruleset) as ruleset:
			abb_config = load_rules(ruleset)
	abba = Abbreviation_dictionary(abb_config)
	
	# Generate a legend
	if args.legend:
		legend = (abba.generate_legend())
	
	# Choose the rendering method	
	if args.legend: 
		print(legend)
	if args.render == "unicode":
		print(render.uni_decode(abba.abbreviate_text(text), abba))
	else:
		print(render.base_decode(abba.abbreviate_text(text), abba))
