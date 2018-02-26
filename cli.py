#!/usr/bin/python3.6
#-*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: CLI

import sys
import argparse
import decimal
import json
from currency_converter import fetch_rates, recognize_symbol, convert_to_output_currency
from constants import decipher_symbol

# simplify pls
# so much try except

class __main__():
	parser = argparse.ArgumentParser()
	parser.add_argument('--amount', action="store", required=True, type=float, dest="amount", help='The amount of input currency to convert.')
	parser.add_argument('--input_currency', action="store", required=True, dest="input_currency", help='Currency from which we want to convert. A 3 letter name or the currency symbol.')
	parser.add_argument('--output_currency', action="store", dest="output_currency", help='Currency to convert to. A 3 letter name or the currency symbol.')
	arguments = parser.parse_args()
	if(arguments.amount < 0):
		sys.stderr.write("Cannot convert a negative value!\n")
		sys.exit(1)

	try:
		arguments.input_currency = recognize_symbol(arguments.input_currency)
	except KeyError:
		sys.stderr.write("Input currency was not recognized!\n")
		sys.exit(2)

	# here
	if(arguments.output_currency != None):
		try:
			arguments.output_currency = recognize_symbol(arguments.output_currency)
		except KeyError:
			sys.stderr.write("Output currency was not recognized!\n")
			sys.exit(2)
	
	arguments.amount = str(round(arguments.amount, 2))
	arguments.amount = decimal.Decimal(arguments.amount)

	rates = fetch_rates()

	if(arguments.output_currency == None):
		try:
			all_currencies = convert_to_output_currency(arguments.amount, arguments.input_currency, arguments.output_currency, rates)
		except UnboundLocalError:
			sys.stderr.write("Input currency was not recognized!\n")
			sys.exit(2)

		print(json.dumps({'input': {'amount': str(arguments.amount), 'currency': arguments.input_currency}, 'output': all_currencies}, indent = 4, sort_keys=True))
	else:
		try:
			converted_val = convert_to_output_currency(arguments.amount, arguments.input_currency, arguments.output_currency, rates)
		except UnboundLocalError:
			sys.stderr.write("Input or output currency was not recognized!\n")
			sys.exit(2)
		two_decimal_places = str(round(converted_val, 2))
		print(json.dumps({'input': {'amount': str(arguments.amount), 'currency': arguments.input_currency}, 'output': {arguments.output_currency : str(two_decimal_places)}}, indent = 4, sort_keys=True))

	sys.exit(0)
