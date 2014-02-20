def decode(text, abb_dict, encoding):
	"""
	Take abbreviated text with control entities and renders them in unicode or base
	"""
	render = ""
	for char in text:
		if 57344 <= ord(char) < 63743:
			render += abb_dict.lookup(char, option = encoding)
		else:
			render += char
	return render
