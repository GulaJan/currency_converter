#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: CLI class

import urllib.request
import re
import json

def fetchData():
	apiUrl = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
	data = urllib.request.urlopen(apiUrl).read()		
	return data

def filterData(data):
	data = data.decode()
	pattern = "currency='([a-z,A-Z]{3})'\srate='([\d]+[.][\d]+)'"
	result = dict()
	matched = re.findall(pattern, data)
#		result['currencies'] = matched.group(1)
#		result['rates'] = matched.group(2)
	return matched

def convert(amount, inCurr, outCurr, data):
	if(outCurr == 'EUR'):
		outRate = 1
	if(inCurr == 'EUR'):
		inRate = 1
	for item in data:
		if(item[0] == inCurr):
			inRate = item[1]
		if(item[0] == outCurr): #item[0] = currencies, item[1] = rates
			outRate = item[1]

	return amount / float(inRate) * float(outRate)

def printJSON(amount, inCurr, outCurr, result):
	result = "%.2f" % result 
	print(json.dumps({'input': {'amount': amount, 'currency': inCurr}, 'output': {outCurr : result}}, indent = 4, sort_keys=True))
