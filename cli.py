#!/usr/bin/python3.6
#-*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: CLI

import sys
import argparse
import decimal
import json
from currency_converter import fetch_rates, rates_to_array, calculate, recognize_symbol, convert
from constants import decipher_symbol

class __main__():
	parser = argparse.ArgumentParser()
	parser.add_argument('--amount', action="store", required=True, type=float, dest="amount", help='The amount of input currency to convert.')
	parser.add_argument('--input_currency', action="store", required=True, dest="input_currency", help='Currency from which we want to convert. A 3 letter name or the currency symbol.')
	parser.add_argument('--output_currency', action="store", dest="output_currency", help='Currency to convert to. A 3 letter name or the currency symbol.')
	arguments = parser.parse_args()
	if(arguments.input_currency == arguments.output_currency):
		sys.stderr.write("Output currency has to differ from the input currency!\n")
		sys.exit(1)
	if(arguments.amount < 0):
		sys.stderr.write("Cannot convert a negative value!\n")
		sys.exit(1)

	rates = fetch_rates()
	filtered_rates = rates_to_array(rates)
	
	currencies = {'input_currency': arguments.input_currency, 'output_currency': arguments.output_currency}
	currencies = recognize_symbol(currencies)
	arguments.input_currency = currencies['input_currency']
	arguments.output_currency = currencies['output_currency']
	
	arguments.amount = str(round(arguments.amount, 2))
	arguments.amount = decimal.Decimal(arguments.amount)
	if(arguments.output_currency == None):
		try:
			all_currencies = convert(arguments.amount, arguments.input_currency, arguments.output_currency, filtered_rates)
		except(UnboundLocalError):
			sys.stderr.write("Input currency was not recognized!\n")
			sys.exit(2)

		print(json.dumps({'input': {'amount': str(arguments.amount), 'currency': arguments.input_currency}, 'output': all_currencies}, indent = 4, sort_keys=True))
	else:
		converted_val = convert(arguments.amount, arguments.input_currency, arguments.output_currency, filtered_rates)
		if(converted_val == UnboundLocalError):
			sys.stderr.write("Input or output currency was not recognized!\n")
			sys.exit(2)
		two_decimal_places = str(round(converted_val, 2))
		print(json.dumps({'input': {'amount': str(arguments.amount), 'currency': arguments.input_currency}, 'output': {arguments.output_currency : str(two_decimal_places)}}, indent = 4, sort_keys=True))

	sys.exit(0)
