#!/usr/bin/env python
# -*- coding: utf-8 -*-
uCOM_TIL = u'\u0303'
uTH = u'\u00F0'
uWH = u'\u2c72'
uROT = u'\uA75B'
uSUB_E = u'\u032F'
uSUB_O = u'\u0325'

WORDS = [{'pattern':r'(?<=\b)the(?=\b)','name':'THE','uni_rep':uTH},
		{'pattern':r'(?<=\b)this(?=\b)','name':'THIS','uni_rep':uTH+'s'},
		{'pattern':r'(?<=\b)then(?=\b)','name':'THEN','uni_rep':uTH+'n'},
		{'pattern':r'(?<=\b)that(?=\b)','name':'THAT','uni_rep':uTH+'t'},
		{'pattern':r'(?<=\b)there(?=\b)','name':'THERE','uni_rep':uTH+'r'},
		{'pattern':r'(?<=\b)and(?=\b)','name':'AND','uni_rep':u'\u204A'},
		{'pattern':r'(?<=\b)with(?=\b)','name':'WITH','uni_rep':''},
		{'pattern':r'(?<=\b)can','name':'CAN','uni_rep':u'\u00E7'},
		{'pattern':r'(?<=\b)we(?=\b)','name':'WE','uni_rep':u'w'+uCOM_TIL},
		{'pattern':r'(?<=\b)me(?=\b)','name':'ME','uni_rep':u'm'+uCOM_TIL},
		{'pattern':r'(?<=\b)us(?=\b)','name':'US','uni_rep':u'u'+uCOM_TIL},
		{'pattern':r'(?<=\b)is(?=\b)','name':'IS','uni_rep':u'\u01c2'},
		{'pattern':r'(?<=\b)what(?=\b)','name':'WHAT','uni_rep':uWH+'t'},
		{'pattern':r'(?<=\b)when(?=\b)','name':'WHEN','uni_rep':uWH+'n'},
		{'pattern':r'(?<=\b)which(?=\b)','name':'WHICH','uni_rep':uWH+'c'},
		{'pattern':r'(?<=\b)why(?=\b)','name':'WHY','uni_rep':uWH+'y'},
		{'pattern':r'(?<=\b)where(?=\b)','name':'WHERE','uni_rep':uWH+uROT},
		{'pattern':r'(?<=\b)you(?=\b)','name':'YOU','uni_rep':u'\u1eff'},
		{'pattern':r'(?<=\b)in','name':'IN','uni_rep':u'\u0279'},
		{'pattern':r'to(?![aeiouywy])','name':'TO','uni_rep':u'\u0167'},
		{'pattern':r'(?<=\b)at(?=\b)','name':'AT','uni_rep':u'@'},
		]

TRIGRAPHS = [{'pattern':r'rse','name':'RSE','uni_rep':''},
			{'pattern':r'rce','name':'RCE','uni_rep':''},
			]	
DIGRAPHS = [{'pattern':r'th','name':'TH','uni_rep':uTH},
			{'pattern':r'ch','name':'CH','uni_rep':u'\u0256'},
			{'pattern':r'ck','name':'CK','uni_rep':u'\u13D0'},
			{'pattern':
				r'er(?=\b)|(?=\b)er','name':'TERMINAL_ER','uni_rep':u'\u0119'},
			{'pattern':
				r'(?<=\w)er(?=\w)','name':'MEDIAL_ER','uni_rep':u'\u0a6d'},
			{'pattern':r'gh','name':'YOGH','uni_rep':u'\u021D'},
			{'pattern':r'ed(?=\b)','name':'TERMINAL_ED','uni_rep':u'\u0333'},
			{'pattern':r'ly(?=\b)','name':'TERMINAL_LY','uni_rep':u'\u1DCF'},
			{'pattern':r'(?<=[aeiouy])nk','name':'O_NK','uni_rep':u'\u0330'},
			{'pattern':r'(?<=[aeiouy])ng','name':'O_NG','uni_rep':u'\u032B'},
			{'pattern':r'(?<=[aeiouy])nt','name':'O_NT','uni_rep':uCOM_TIL},
			{'pattern':r'(?<=[aeiouy])nd','name':'O_ND','uni_rep':u'\u036B'},
			{'pattern':r'(?<=[aeiouy])ct','name':'O_CT','uni_rep':u'\u0265'},
			{'pattern':r'oo','name':'OO','uni_rep':'o'+uSUB_O},
			{'pattern':r'll','name':'LL','uni_rep':u'\u2016'},
			{'pattern':r'ss(?=\w)','name':'MEDIAL_SS','uni_rep':u'\u00DF'},
			]
		
SINGLETONS = [
			{'pattern':r's(?=\w)','name':'LONG_S','uni_rep':u'\u017F'},
			{'pattern':r'(?<=[bdhmnopquw])r',
				'name':'R_ROTUNDA','uni_rep':uROT},
			{'pattern':r'(?<=\w)e(?=(\b|s))',
				'name':'TERMINAL_E','uni_rep':uSUB_E}	
			]
			
			# MAJOR TODO: Right now the RE engine sees unicode control characters as non-word.