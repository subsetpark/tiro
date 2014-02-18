import collections, re, random, configparser


class Generator(object):
	def __init__(self, text):
		# Take some interesting unicode ranges and cat them into a list.
		self.symbol_pool = sum([list(range(x,y)) for x,y in [(383,447),(502,687),(913,1071),(1120,1319)]],[])
		# shuffle the list. (must be in-place)
		random.shuffle(self.symbol_pool)
		# make an iterator out of the list.
		self.symbol_pool = iter(self.symbol_pool)
		self.text = text
		
	def dict_builder(self, counter, name_prefix="", pattern_suffix=""):
		patterns = {}
		for most_common, _ in counter:
			patterns[name_prefix + most_common.upper()] = { 
				"pattern": most_common + pattern_suffix,
				"uni_rep": chr(next(self.symbol_pool))
			}
		return patterns
		
	def token_counter(self, pattern, count):
		return collections.Counter(re.findall(pattern, self.text)).most_common(count)
		
	def generate_abbreviations(self):
		patterns = self.dict_builder(self.token_counter("\\w\\w", 15), name_prefix='_')
		patterns.update(self.dict_builder(self.token_counter("\\w\\w+", 20), pattern_suffix="#word"))
		return patterns
		
	def generate_rules(self):
		"""
		Analyze a text, and construct an abbreviation list.
		"""	
		config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation(),allow_no_value=True)
		
		config.read_dict(self.generate_abbreviations())
		return config
