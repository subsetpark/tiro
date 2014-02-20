def base_decode(text, abb_dict):
	"""
	Take abbreviated text with control entities and renders them in ASCII 
	"""
	working_text = list(text)
	render = ""
	for index, char in enumerate(working_text):
		if 57344 <= ord(char) < 63743:
			render += abb_dict.lookup(char)
		else:
			render += char
	return render

def uni_decode(text, abb_dict):
	"""
	Take abbreviated text with control entities and renders them in unicode 
	"""
	working_text = list(text)
	render = ""
	for char in working_text:
		if 57344 <= ord(char) < 63743:
			if abb_dict.lookup(char, 'uni_rep'):
				render += abb_dict.lookup(char, 'uni_rep')
			else:
				render += abb_dict.lookup(char, 'name')
		else:
			render += char
	return render
