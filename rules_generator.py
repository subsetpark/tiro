import collections, re

def generate_word_abbreviations(text):
	word_counter = collections.Counter()
	for word in re.findall("\\w+", text):
		word_counter[word.lower()] += 1

	word_patterns = []	
	ordinal = 994
	for most_common in [element[0] for element in word_counter.most_common(15)]:
		new_pattern = {"name":most_common, 
						"pattern":"(?<=\\b)" + most_common + "(?=\\b)",
						"uni_rep":chr(ordinal)}
		ordinal += 1
		word_patterns.append(new_pattern)
	return word_patterns

def generate_sequence_abbreviations(text):
	seq_counter = collections.Counter(text.replace(" ","")[i:i+2] for i in range(len(text)-2)).most_common(10)
	del seq_counter[0]

	seq_patterns = []	
	ordinal = 1329
	for most_common in [element[0] for element in seq_counter]:
		new_pattern = {"name":most_common, 
						"pattern":"(?<=\\b)" + most_common + "(?=\\b)",
						"uni_rep":chr(ordinal)}
		ordinal += 1
		seq_patterns.append(new_pattern)
	return seq_patterns

def generate_rules(text):
	"""
	Analyze a text, and construct an abbreviation list.

	"""	
	word_set = {}
	word_set["class"] = "words"
	word_set["patterns"] = generate_word_abbreviations(text)
	seq_set = {}
	seq_set["class"] = "digraphs"
	seq_set["patterns"] = generate_sequence_abbreviations(text)
	abb_dict = [word_set] + [seq_set]
	return abb_dict