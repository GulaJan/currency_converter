#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: Shared functions for both CLI and API

import urllib.request
import re
import json
import decimal
from constants import decipher_symbol

def fetch_rates():
	url = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
	all_rates = urllib.request.urlopen(url).read()		
	return all_rates

def rates_to_array(all_rates):
	all_rates = all_rates.decode()
	pattern = "currency='([a-z,A-Z]{3})'\srate='([\d]+[.][\d]+)'"
	matched = re.findall(pattern, all_rates)
	return matched

def calculate(amount, input_currency, output_currency, rates):
	if(output_currency == 'EUR'):
		output_rate = 1
	if(input_currency == 'EUR'):
		input_rate = 1
	for item in rates:
		if(item[0] == input_currency):
			input_rate = item[1]
		if(item[0] == output_currency): #item[0] = currencies, item[1] = rates
			output_rate = item[1]

	return amount / decimal.Decimal(input_rate) * decimal.Decimal(output_rate)

def recognize_symbol(arguments):
	if(arguments['output_currency'] != None) :	
		if((len(arguments['output_currency']) != 3) or (not(arguments['output_currency'].isupper()))):
			try:
				arguments['output_currency'] = decipher_symbol(arguments['output_currency'])
			except (KeyError):
				return KeyError

	if((len(arguments['input_currency']) != 3) or (not(arguments['input_currency'].isupper()))):
		try:
			arguments['input_currency'] = decipher_symbol(arguments['input_currency'])
		except(KeyError):
			return KeyError
	return arguments

def convert(amount, input_currency, output_currency, filtered_rates):
	if(output_currency == None):
		all_currencies = {}
		convert_to_euro = calculate(amount, input_currency, 'EUR', filtered_rates)
		two_places_result = str(round(convert_to_euro, 2))
		# If no output is set we have to explicitly add EUR because it's the base in our data source
		all_currencies['EUR'] = two_places_result
		for item in filtered_rates:
			try:
				converted_value = calculate(amount, input_currency, item[0], filtered_rates)
			except(UnboundLocalError):
				return UnboundLocalError

			two_places_result = str(round(converted_value, 2))
			all_currencies[item[0]] = two_places_result

		return all_currencies

	else:
		try:
			converted_value = calculate(amount, input_currency, output_currency, filtered_rates)
		except(UnboundLocalError):
			return UnboundLocalError
		return converted_value