import collections, re, random

class Rules_generator(object):
	def __init__(self):
		self.pool = iter(sum([list(range(x,y)) for x,y in [(383,447),(502,687),(913,1071),(1120,1319)]],[]))

	def generate_word_abbreviations(self, text):
		self.word_counter = collections.Counter(re.findall("\\w+", text)).most_common(20)
		
		self.word_patterns = []	
		for most_common in [element[0] for element in self.word_counter]:
			new_pattern = {"name":most_common, 
							"pattern":"(?<=\\b)" + most_common + "(?=\\b)",
							"uni_rep":chr(next(self.pool))}
			self.word_patterns.append(new_pattern)
		return self.word_patterns
	
	def generate_sequence_abbreviations(self, text):
		self.seq_counter = collections.Counter(re.findall("\\w\\w\\w", text)).most_common(15)
	
		self.seq_patterns = []	
		for most_common in [element[0] for element in self.seq_counter]:
			new_pattern = {"name":most_common, 
							"pattern":"(?<=\\b)" + most_common + "(?=\\b)",
							"uni_rep":chr(next(self.pool))}
			self.seq_patterns.append(new_pattern)
		return self.seq_patterns
	
	def generate(self, text):
		"""
		Analyze a text, and construct an abbreviation list.
	
		"""	
		abb_dict = [{"class":"words","patterns":self.generate_word_abbreviations(text)}]+ [{"class":"digraphs","patterns":self.generate_sequence_abbreviations(text)}]
		return abb_dict
		
def generate_rules(text):
	generator = Rules_generator()
	return generator.generate(text)