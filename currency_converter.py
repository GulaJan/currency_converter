#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# Project: Currency converter

import sys
import argparse
import urllib.request
import re
import json

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
#		This part is switchable
#		apiUrl = "https://api.fixer.io/latest?base=" + inCurr
		apiUrl = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
		data = urllib.request.urlopen(apiUrl).read()		
		return data

	def filterData(inCurr, outCurr, data):
		data = data.decode()
#		print(data)
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

	def decipherSymbol(symbol):
		# Errors : Countries with same symbols but different rates ? [USD AUD CAD HKD MXN NZD SGD], [DKK, SEK, ISK, NOK], [JPY, CNY]
		return{
			chr(36): 'USD',
#			chr(36): 'AUD',
#			chr(36): 'CAD',
#			chr(36): 'HKD',
#			chr(36): 'MXN',
#			chr(36): 'NZD',
#			chr(36): 'SGD',
			chr(165): 'JPY',
#			chr(165): 'CNY',
			chr(1083) + chr(1074): 'BGN',
			chr(75) + chr(269): 'CZK',
			chr(107) + chr(114): 'DKK',
#			chr(107) + chr(114): 'SEK',
#			chr(107) + chr(114): 'ISK',
#			chr(107) + chr(114): 'NOK',
			chr(163): 'GBP',
			chr(70) + chr(116): 'HUF',
			chr(122) + chr(322): 'PLN',
			chr(108) + chr(101) + chr(105): 'RON',
			chr(67) + chr(72) + chr(70): 'CHF',
			chr(107) + chr(110): 'HRK',
			chr(8381): 'RUB',
			chr(8378): 'TRY',
			chr(82) + chr(36): 'BRL',
			chr(82) + chr(112): 'IDR',
			chr(8362): 'ILS',
			chr(8377): 'INR',
			chr(8361): 'KRW',
			chr(82) + chr(77): 'MYR',
			chr(8369): 'PHP',
			chr(3647): 'THB',
			chr(82): 'ZAR',											
		}[symbol]

	arguments = argParsing()
	data = fetchData()
	filteredData = filterData(arguments.inCurr, arguments.outCurr, data)

	if((len(arguments.outCurr) != 3) or (not(arguments.outCurr.isupper()))):
		try:
			arguments.outCurr = decipherSymbol(arguments.outCurr)
		except:
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
#		print(res)
		for item in filteredData:
			try:
				res = convert(arguments.amount, arguments.inCurr, item[0], filteredData)
			except(UnboundLocalError):
				sys.stderr.write("Input or output currency was not recognized!\n")
				sys.exit(3)

#			print(res)
	else:
		try:
			res = convert(arguments.amount, arguments.inCurr, arguments.outCurr, filteredData)
		except(UnboundLocalError):
			sys.stderr.write("Input or output currency was not recognized!\n")
			sys.exit(3)

#	print("%.2f" % round(res,2))
#	res = str(round(res,2))
	res = "%.2f" % res 
#	print(arguments.outCurr)
	print(json.dumps({'input': {'amount': arguments.amount, 'currency': arguments.inCurr}, 'output': {arguments.outCurr : res}}, indent = 4, sort_keys=True))
	sys.exit(0)


	# TO DO:
	# 3. JSON
	# 4. FULL API
