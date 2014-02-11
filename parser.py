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

def word_manager(word, func):
	substring = []
	subword = False
	for position in word:
		# souRCE
		if isinstance(position, str) and not subword:
			sublist.append(position)
		# CHapter
		elif not isinstance(position, str) and not sublist:
			continue
		elif not instance(position, str) and sublist:
			subword = str(sublist)
			return lookup_and_substitute(word, set)

def separate_strings_and_symbols(token_list):
	"""
	
	>>> separate_strings_and_symbols(['a', 'b', Glyph('RCE'), 'h'])
	(['ab', 'h'], [RCE])
	
	"""
	
	
	symbol_indices_and_symbols = [(i,x) for i,x in enumerate(token_list) if isinstance(x, Glyph)]
	symbol_indices, symbols = (zip(*symbol_indices_and_symbols)
							   if symbol_indices_and_symbols else ((),()))

	string_indices = [(i+1, j) for i,j in zip((-1,)+symbol_indices,symbol_indices+(len(token_list),))]
	string_list = ["".join(token_list[i:j]) for i,j in string_indices]
	return (string_list, list(symbols))

def for_each_string(list, func):
	"""
	Takes a list of chars and non-chars, makes strings out of 
	consecutive chars, and then applies a function to those chars.
	Returns a list of chars and non-chars.
	"""
	strings, symbols = separate_strings_and_symbols(list)
	new_strings = [func(string) for string in strings]
	
	product = new_strings[0][:]
	for symbol, string in zip(symbols, strings[1:]):
		product.append(symbol)
		product.extend(string)
	return product	

def substitute_trigraphs(word): 
	return lookup_and_substitute(word, ABB_SET.TRIGRAPHS)
def substitute_digraphs(word):
	return lookup_and_substitute(word, ABB_SET.DIGRAPHS)
	
def lookup_and_substitute(word, set):
	for master, value in set.iteritems():
		pattern = re.compile(master)
		matches = pattern.finditer(word)
		working_word = list(word)
		for match in matches:
			working_word[match.span()[0]:match.span()[1]] = []
			working_word.insert(match.span()[0]+1, Glyph(value))
	return working_word
			
def abbreviate(word):
	"""
	Looks up a word in the abbreviation set, then looks up its characters
	
	>>> abbreviate("the")
	THE
	
	>> abbreviate("dijkstra")
	None
	
	>>> abbreviate("source")
	['s', 'o', 'u', RCE]
	"""
	# return a full-word substitute
	# TODO: Short-circuit full words
	#if word in ABB_SET.WORDS:
	#	return Glyph(ABB_SET.WORDS[word])
	
	else:
		# We could put this into a loop that goes through dictionary sets
		result = for_each_string(list(word), 
								lambda x: lookup_and_substitute(x, ABB_SET.WORDS))	
		result = for_each_string(list(word), 
								lambda x: lookup_and_substitute(x, ABB_SET.TRIGRAPHS))
		result = for_each_string(list(word), 
								lambda x: lookup_and_substitute(x, ABB_SET.DIGRAPHS))		
	return word
		
def parse(text):
	words = text.split()
	map(abbreviate, words)
	
	
	
if __name__ == '__main__':
	import doctest
	doctest.testmod()
	
	#abbreviate("source")