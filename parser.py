import re
import ABB_SET

class Glyph(object):
	"""
	Each single-space character is a single glyph. This includes single
	word glyphs, multi-letter glyphs, and composed characters.
	"""
	def __init__(self, name):
		self.name = name
		
	def __repr__(self):
		return self.name
		
		
class Body(object):
	"""
	The body is a list of glyphs which can be read out to a renderer.
	"""
	def __init__(self):
		self.glyph_list = []
	
	def read(self):
		return self.glyph_list
	
	def append(self, glyph):
		self.glyph_list.append(glyph)

def lookup_and_substitute(word, set):
	for master, value in set.iteritems():
		pattern = re.compile(master)
		matches = re.finditer(pattern, word)
		word = list(word)
		for match in matches:
			word[match.span()[0]:match.span()[1]] = []
			word.insert(match.span[0]+1, Glyph(value))
			
def abbreviate(word):
	"""
	Looks up a word in the abbreviation set, then looks up its characters
	
	>>> abbreviate("the")
	THE
	
	>> abbreviate("dijkstra")
	None
	
	>>> abbreviate("source")
	"""
	# return a full-word substitute
	if word in ABB_SET.WORDS:
		return Glyph(ABB_SET.WORDS[word])
	
	# for in-word substitutions we need to convert the word to a list
	#else:
	#	for trigraph, value in ABB_SET.TRIGRAPHS.iteritems():
	#		pattern = re.compile(trigraph)
	#		word = re.sub(pattern, value, word)	
	else:
		lookup_and_substitute(word, ABB_SET.TRIGRAPHS)
	
	return word
		
def parse(text):
	words = text.split()
	map(abbreviate, words)
	
	
	
if __name__ == '__main__':
	import doctest
	doctest.testmod()