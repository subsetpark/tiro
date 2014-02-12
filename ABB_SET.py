#!/usr/bin/env python
# -*- coding: utf-8 -*-

WORDS = [{'pattern':'the','name':'THE','uni_rep':'∂'},
		{'pattern':'and','name':'AND','uni_rep':'⁊'},
		{'pattern':'with','name':'WITH','uni_rep':''},
		]

TRIGRAPHS = [{'pattern':'rse','name':'RSE','uni_rep':''},
			{'pattern':'rce','name':'RCE','uni_rep':''},
			]	
DIGRAPHS = [{'pattern':'th','name':'TH','uni_rep':''},
			{'pattern':'ch','name':'CH','uni_rep':''},
			]
		
SINGLETONS = [{'pattern':'a','name':'a','uni_rep':''},
			{'pattern':'s ','name':'s ','uni_rep':''},
			{'pattern':'s\w','name':' LONG_S','uni_rep':'ſ'},
			]