#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# Project: Currency converter

import sys
import argparse
import urllib.request
import re

class CLI:
	def argParsing():	
		parser = argparse.ArgumentParser()
		parser.add_argument('--amount', action="store", required=True, type=float, dest="amount", help='The amount of input currency to convert.')
		parser.add_argument('--input_currency', action="store", required=True, dest="inCurr", help='Currency from which we want to convert. A 3 letter name or the currency symbol.')
		parser.add_argument('--output_currency', action="store", dest="outCurr", help='Currency to convert to. A 3 letter name or the currency symbol.')
		args = parser.parse_args()
		if(args.inCurr == args.outCurr):
			sys.stderr.write("Output currency has to differ from the input currency!")
			sys.exit(1)
		if(args.amount < 0):
			sys.stderr.write("Cannot convert a negative value!")
			sys.exit(1)
		return args

	def fetchData():
#		This part is switchable
#		apiUrl = "https://api.fixer.io/latest?base=" + inCurr
		apiUrl = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
		data = urllib.request.urlopen(apiUrl).read()		
		return data

	def filterData(inCurr, outCurr, data):
		data = data.decode()
		print(data)
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
		print(inRate)
		print(outRate)
		print(amount)
		return amount / float(inRate) * float(outRate)


	arguments = argParsing()
	data = fetchData()
	filteredData = filterData(arguments.inCurr, arguments.outCurr, data)
	res = convert(arguments.amount, arguments.inCurr, arguments.outCurr, filteredData)
	print(res)
	sys.exit(0)


	# TO DO:
	# 1. CURRENCY SYMBOLS
	# 2. NO OUTPUT
	# 3. CONVERTING EUROS
	# 4. FULL API
