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
		self.pattern = abb_data[0]
		self.name = abb_data[1]
		
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
	
	"""
	def add_sequence(self, set_sequence):
		new_sequence = []
		# construct a list of all abbreviation in a given set,
		# then append them to the list of all sequences.
		for pattern in set_sequence:
			# create the pattern here.
			new_sequence.append(Abbreviation(pattern, self.serial))
			self.serial += 1
		self.abb_sequences.append(new_sequence)
	
	def __init__(self, *set_sequences):
		self.abb_sequences = []
		# begin creating unicode characters at the beginning 
		# of the private use space
		self.serial = 57344
		for sequence in set_sequences:
			self.add_sequence(sequence)
	
	def lookup_and_substitute(self, word, sequence):
		working_word = word
		for abbreviation in sequence:
			working_word = re.sub(abbreviation.pattern, abbreviation.codepoint, working_word) 
		return working_word	
	
	def abbreviate_text(self, text):
		working_text = text
		for sequence in self.abb_sequences:
			working_text = self.lookup_and_substitute(working_text, sequence)
		return working_text

	
if __name__ == "__main__":
	import doctest
	doctest.testmod()
	
	text = " ".join(sys.argv[1:])
	
	words = text.split()
	abba = Abbreviation_dictionary(ABB_SET.WORDS, ABB_SET.TRIGRAPHS, ABB_SET.DIGRAPHS)
	
	print abba.abbreviate_text(text)
