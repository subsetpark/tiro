import collections, re, random, configparser

def generate_word_abbreviations(text, pool):
	word_counter = collections.Counter(re.findall("\\w\\w+", text)).most_common(20)
	word_patterns = {}
	for most_common in [element[0] for element in word_counter]:
		word_patterns[most_common.upper()] = {
					"pattern":most_common + "#word",
					"uni_rep":chr(next(pool))
					}
	return word_patterns

def generate_sequence_abbreviations(text, pool):
	seq_counter = collections.Counter(re.findall("\\w\\w", text)).most_common(15)
	seq_patterns = {}
	for most_common in [element[0] for element in seq_counter]:
		seq_patterns['_'+most_common.upper()] = {
						"pattern":most_common,
						"uni_rep":chr(next(pool))
						}
	return seq_patterns

def generate_rules(text):
	"""
	Analyze a text, and construct an abbreviation list.

	"""	
	
	# Take some interesting unicode ranges and cat them into a list.
	pool = sum([list(range(x,y)) for x,y in [(383,447),(502,687),(913,1071),(1120,1319)]],[])
	# shuffle the list. (must be in-place)
	random.shuffle(pool)
	# make an iterator out of the list.
	pool = iter(pool)
	
	config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation(),allow_no_value=True)
	
	config.read_dict(generate_word_abbreviations(text, pool))
	config.read_dict(generate_sequence_abbreviations(text, pool))
	return config
