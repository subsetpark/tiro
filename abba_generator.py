import collections

def generate_word_abbreviations(text):
	word_counter = collections.Counter()
	for word in text.split():
		word_counter[word] += 1

	word_patterns = []	
	ordinal = 994
	for most_common in [element[0] for element in word_counter.most_common(15)]:
		new_pattern = {}
		new_pattern["name"] = most_common
		new_pattern["pattern"] = "(?<=\\b)" + most_common + "(?=\\b)"
		new_pattern["uni_rep"] = chr(ordinal)
		ordinal += 1
		word_patterns.append(new_pattern)

	return word_patterns

def generate_sequence_abbreviations(text):
	seq_counter = collections.Counter(text.replace(" ","")[i:i+2] for i in range(len(text)-2)).most_common(10)
	del seq_counter[0]

	seq_patterns = []	
	ordinal = 1329
	for most_common in [element[0] for element in seq_counter]:
		new_pattern = {}
		new_pattern["name"] = most_common
		new_pattern["pattern"] = "(?<=\\b)" + most_common + "(?=\\b)"
		new_pattern["uni_rep"] = chr(ordinal)
		ordinal += 1
		seq_patterns.append(new_pattern)

	return seq_patterns

def generate_rules(text):
	"""
	Analyze a text, and construct an abbreviation list.

	>>> generate_abbreviations("Hello hacker school! I'm presenting a small application I'm working on, called *abba*. Abba is an abbreviation generator. It reads in a set of rules of text substitutions, applies them in sequence, and then returns the resulting text. What's sort of fun is that the text is not necessarily returned as a string: the text substitutions are not performed as string operations, but rather the substitutes are inserted into the text in the form of unicode control characters taken from the private use area, that refer back to abbreviation objects. These objects can therefore report on their output in a number of ways.")
	"""	
	word_set = {}
	word_set["class"] = "words"
	word_set["patterns"] = generate_word_abbreviations(text)
	seq_set = {}
	seq_set["class"] = "digraphs"
	seq_set["patterns"] = generate_sequence_abbreviations(text)
	abb_dict = [word_set] + [seq_set]
	return abb_dict