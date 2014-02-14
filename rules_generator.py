import collections, re, random

def generate_word_abbreviations(text, pool):
	word_counter = collections.Counter(re.findall("\\w\\w+", text)).most_common(20)
	
	word_patterns = []	
	for most_common in [element[0] for element in word_counter]:
		new_pattern = {"name":most_common.upper(), 
						"pattern":"(?<=\\b)" + most_common + "(?=\\b)",
						"uni_rep":chr(next(pool))}
		word_patterns.append(new_pattern)
	return word_patterns

def generate_sequence_abbreviations(text, pool):
	seq_counter = collections.Counter(re.findall("\\w\\w", text)).most_common(15)

	seq_patterns = []	
	for most_common in [element[0] for element in seq_counter]:
		new_pattern = {"name":'_'+most_common.upper(), 
						"pattern":most_common,
						"uni_rep":chr(next(pool))}
		seq_patterns.append(new_pattern)
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
	
	
	abb_dict = [{"class":"words",
				"patterns":generate_word_abbreviations(text, pool)}, 
			   {"class":"digraphs",
				"patterns":generate_sequence_abbreviations(text, pool)}]
	return abb_dict
