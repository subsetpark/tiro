import re, functools

"""
The processing language for describing matching patterns for abbreviations.
Users can describe text with a series of tags, which are compiled into the appropriate regular expression. EG:

'foo.initial' expands to a regular expression that matches all occurances of 'foo' at the beginning of a word.

I need to be able to specify other classes in the regexp. For instance, 'before the end of the word or another suffix.' Not sure how to do that.

A lot of these come to order of operation. So one way to deal with this is to process the tags in batches. For instance, as long as abbreviation characters are also word boundaries, then the only difference between suffix (ion) and final (s) is that s is rendered first.

So in that case the compiler would return two objects - the compiled regexp, and the class that it falls under.

Better, I think, to create a regnet object, which contains a compiled pattern and a precedence indicator.
"""
rules = [
(re.compile("(?P<pat>\\w+)#pref"), "(?<=\\\\b)\g<pat>", 2), 
(re.compile("(?P<pat>\\w+)#suf"), "\g<pat>(?=\\\\b)", 2),
(re.compile("(?P<pat>\\w+)#init"), "(?<=\\\\b)\g<pat>", 0),
(re.compile("(?P<pat>\\w+)#final"), "\g<pat>(?=\\\\b)", 0),
(re.compile("(?P<pat>\\w+)#iso"), "(?<=\\\\b)\g<pat>(?=\\\\b)", 0),    
(re.compile("(?P<pat>\\w+)#word"), "(?<=\\\\b)\g<pat>", 1),
(re.compile("(?P<pat>^\\w\\w\\w$)"), "\g<pat>", 2),
(re.compile("(?P<pat>^\\w\\w$)"), "\g<pat>", 3),
(re.compile("(?P<pat>^\\w$)"), "\g<pat>", -1),
(re.compile("(?P<pat>\\w+)#vow"), "(?<=[aeiouy])\g<pat>", 2),
(re.compile("(?P<pat>\\w+)#hard"), "\g<pat>", 0)
] 


class Regnet(object):
	def __init__(self, pattern):
		"""
		Given a user-defined pattern, compile it into a regnet.
		A regnet has two parts: a compiled regexp, and its precedence level.
		
		So a finalized regnet takes this:
		"foo#init"
		
		And produces: 
		a compiled regexp for "(?<=\\\\b)foo" and
		prec = 0
		
		So actually, regnet rules are exclusive. Every pattern can only have one tag on it.
		
		"""
		
		#find the rule that applies to this regnet, compile a regexp and assign
		for rule in rules:
			if re.match(rule[0], pattern):
				self.pattern = re.compile(re.sub(rule[0], rule[1], pattern), re.IGNORECASE)
				self.prec = rule[2]
				break
		else:
			self.prec = -1
			self.pattern = re.compile(pattern, re.IGNORECASE)
		
