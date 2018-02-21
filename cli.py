#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: CLI class

import sys
import argparse
import urllib.request
import re
import json
from constants import decipherSymbol

class CLI:
	def argParsing():
		parser = argparse.ArgumentParser()
		parser.add_argument('--amount', action="store", required=True, type=float, dest="amount", help='The amount of input currency to convert.')
		parser.add_argument('--input_currency', action="store", required=True, dest="inCurr", help='Currency from which we want to convert. A 3 letter name or the currency symbol.')
		parser.add_argument('--output_currency', action="store", dest="outCurr", help='Currency to convert to. A 3 letter name or the currency symbol.')
		args = parser.parse_args()
		if(args.inCurr == args.outCurr):
			sys.stderr.write("Output currency has to differ from the input currency!\n")
			sys.exit(1)
		if(args.amount < 0):
			sys.stderr.write("Cannot convert a negative value!\n")
			sys.exit(1)

		return args

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

	arguments = argParsing()
	data = fetchData()
	filteredData = filterData(data)
	if(arguments.outCurr != None) :	
		if((len(arguments.outCurr) != 3) or (not(arguments.outCurr.isupper()))):
			try:
				arguments.outCurr = decipherSymbol(arguments.outCurr)
			except(KeyError):
				sys.stderr.write("Output symbol was not recognized!\n")
				sys.exit(3)

	if((len(arguments.inCurr) != 3) or (not(arguments.inCurr.isupper()))):
		try:
			arguments.inCurr = decipherSymbol(arguments.inCurr)
		except(KeyError):
			sys.stderr.write("Input symbol was not recognized!\n")
			sys.exit(3)

	if(arguments.outCurr == None):
		res = convert(arguments.amount, arguments.inCurr, 'EUR', filteredData)
		for item in filteredData:
			try:
				res = convert(arguments.amount, arguments.inCurr, item[0], filteredData)
			except(UnboundLocalError):
				sys.stderr.write("Input or output currency was not recognized!\n")
				sys.exit(3)

	else:
		try:
			res = convert(arguments.amount, arguments.inCurr, arguments.outCurr, filteredData)
		except(UnboundLocalError):
			sys.stderr.write("Input or output currency was not recognized!\n")
			sys.exit(3)

	res = "%.2f" % res 
	print(json.dumps({'input': {'amount': arguments.amount, 'currency': arguments.inCurr}, 'output': {arguments.outCurr : res}}, indent = 4, sort_keys=True))
	sys.exit(0)
