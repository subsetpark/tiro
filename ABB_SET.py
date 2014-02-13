#!/usr/bin/env python
# -*- coding: utf-8 -*-

WORDS = [{'pattern':r'(?<=\b)the(?=\b)','name':'THE','uni_rep':u'\u00F0'},
		{'pattern':r'(?<=\b)and(?=\b)','name':'AND','uni_rep':u'\u204A'},
		{'pattern':r'(?<=\b)with(?=\b)','name':'WITH','uni_rep':''},
		{'pattern':r'(?<=\b)can','name':'CAN','uni_rep':u'\u00E7'},
		{'pattern':r'(?<=\b)we(?=\b)','name':'WE','uni_rep':u'w\u0303'},
		{'pattern':r'(?<=\b)me(?=\b)','name':'ME','uni_rep':u'm\u0303'},
		{'pattern':r'(?<=\b)us(?=\b)','name':'US','uni_rep':u'u\u0303'},
		{'pattern':r'(?<=\b)is(?=\b)','name':'IS','uni_rep':u'\u01c2'}
		]

TRIGRAPHS = [{'pattern':'rse','name':'RSE','uni_rep':''},
			{'pattern':'rce','name':'RCE','uni_rep':''},
			]	
DIGRAPHS = [{'pattern':'th','name':'TH','uni_rep':u'\u00F0'},
			{'pattern':'ch','name':'CH','uni_rep':''},
			{'pattern':'ck','name':'CK','uni_rep':''},
			{'pattern':
				r'er(?=\b)|(?=\b)er','name':'TERMINAL_ER','uni_rep':u'\u0118'},
			{'pattern':r'(?<=\w)er(?=\w)','name':'MEDIAL_ER','uni_rep':''},
			{'pattern':'gh','name':'YOGH','uni_rep':u'\u021D'},
			{'pattern':r'ed(?=\b)','name':'TERMINAL_ED','uni_rep':u'\u0333'},
			{'pattern':r'ly(?=\b)','name':'TERMINAL_LY','uni_rep':u'\u1DCF'},
			{'pattern':r'(?<=[aeiou])nk','name':'O_NK','uni_rep':u'\u0330'},
			{'pattern':r'(?<=[aeiou])ng','name':'O_NG','uni_rep':u'\u032B'},
			{'pattern':r'(?<=[aeiou])nt','name':'O_NT','uni_rep':u'\u0303'},
			{'pattern':r'(?<=[aeiou])nd','name':'O_ND','uni_rep':u'\u036B'}
			]
		
SINGLETONS = [
			{'pattern':'s(?=\w)','name':'LONG_S','uni_rep':u'\u017F'},
			{'pattern':r'(?<=[bdhmnopquw])r',
				'name':'R_ROTUNDA','uni_rep':u'\uA75B'},
			{'pattern':r'(?<=\w)e(?=(\b|s))',
				'name':'TERMINAL_E','uni_rep':u"\u032F"}	
			]
			
			# MAJOR TODO: Right now the RE engine sees unicode control characters as non-word.