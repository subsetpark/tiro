#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ABB_SET
import sys
import re

class Abbreviation(object):
	"""
	Objects which represent abbreviation glyphs and can be regexped.
	
	"""
	def __init__(self, abb_data, serial):
		self.codepoint = unichr(serial)
		self.pattern = abb_data['pattern']
		self.name = abb_data['name']
		if abb_data['uni_rep']:
			self.uni_rep = abb_data['uni_rep']
		else:
			self.uni_rep = ''
	
	def uni_report(self):
		if self.uni_rep:
			return self.uni_rep	
		else:
			return None
			
	def __repr__(self):
		return self.name
	
	def __unicode__(self):
		return self.codepoint
	
	
			
class Abbreviation_dictionary(object):
	"""
	This object contains sequences of glyph transformations which it
	can run on text objects.

	>>> abba = Abbreviation_dictionary()
	>>> abba.add_sequence(ABB_SET.WORDS)
	>>> abba.lookup_and_substitute("the", abba.abb_sequences[0])
	u'\ue000'
	>>> abba.add_sequence(ABB_SET.TRIGRAPHS)
	>>> abba.lookup_and_substitute("source", abba.abb_sequences[1])
	u'sou\ue004'
	>>> abba.abbreviate_text("the source")
	u'\ue000 sou\ue004'
	>>> print abba.uni_lookup(u'\ue000')
	∂
	"""
	
	def add_to_lookup(self, abbreviation):
		self.lookup_table[abbreviation.codepoint] = abbreviation
		
	def lookup(self, char):
		return self.lookup_table[char].name
		
	def uni_lookup(self, char):
		return self.lookup_table[char].uni_report()
		
	def add_sequence(self, set_sequence):
		new_sequence = []
		# construct a list of all abbreviation in a given set,
		# then append them to the list of all sequences.
		for pattern in set_sequence:
			# create the pattern here.
			new_abbreviation = Abbreviation(pattern, self.serial)
			new_sequence.append(new_abbreviation)
			self.add_to_lookup(new_abbreviation)
			self.serial += 1
		self.abb_sequences.append(new_sequence)
	
	def __init__(self, *set_sequences):
		self.abb_sequences = []
		self.lookup_table = {}
		# begin creating unicode characters at the beginning 
		# of the private use space
		self.serial = 57344
		for sequence in set_sequences:
			self.add_sequence(sequence)
	
	def lookup_and_substitute(self, word, sequence):
		working_word = word
		for abbreviation in sequence:
			working_word = re.sub(abbreviation.pattern, abbreviation.codepoint, working_word.lower()) 
		return working_word	
	
	def abbreviate_text(self, text):
		working_text = text
		for sequence in self.abb_sequences:
			working_text = self.lookup_and_substitute(working_text, sequence)
		return working_text

def base_decode(text, abb_dict):
	"""
	Takes abbreviated text with unicode entities and renders them in ASCII 
	"""
	working_text = list(text)
	render = ""
	for index, char in enumerate(working_text):
		if ord(char) >= 57344:
			render += abb_dict.lookup(char)
		else:
			render += char
	return render
		
def uni_decode(text, abb_dict):
	"""
	Takes abbreviated text with unicode entities and renders them in unicode (or whatever.)
	"""
	working_text = list(text)
	render = u""
	for char in working_text:
		if ord(char) >= 57344:
			if abb_dict.uni_lookup(char):
				render += abb_dict.uni_lookup(char).decode('utf-8')
			else:
				render += abb_dict.lookup(char).decode('utf-8')
		else:
			render += char.decode('utf-8')
	return render
	
if __name__ == "__main__":
	import doctest
	doctest.testmod()
	
	text = " ".join(sys.argv[1:])
	
	words = text.split()
	abba = Abbreviation_dictionary(ABB_SET.WORDS, ABB_SET.TRIGRAPHS, ABB_SET.DIGRAPHS, ABB_SET.SINGLETONS)
	
	print base_decode(abba.abbreviate_text(text), abba)
	print uni_decode(abba.abbreviate_text(text), abba)
