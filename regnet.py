import re, functools

"""
The processing language for describing matching patterns for abbreviations.
Users can describe text with a series of tags, which are compiled into the appropriate regular expression. EG:

'foo.initial' expands to a regular expression that matches all occurances of 'foo' at the beginning of a word.
"""
    
rules = [(re.compile("(?P<pat>\\w+).initial"), "(?<=\\\\b)\g<pat>"), 
        (re.compile("(?P<pat>\\w+).terminal"), "\g<pat>(?=\\\\b)")
        ]

def sub_pattern(rule, text):
	return re.sub(rule[0], rule[1], text)

def compile_regnet(pattern):
    regnet = functools.reduce(lambda x,y: sub_pattern(y, x), rules, pattern)
    return re.compile(regnet)