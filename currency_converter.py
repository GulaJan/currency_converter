#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: Shared functions for both CLI and API

import urllib.request
import re
import json
import decimal  # needed?
from constants import decipher_symbol

def fetch_rates():
	# xmltodict or https://docs.python.org/3.6/library/xml.etree.elementtree.html
	url = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
	all_rates = urllib.request.urlopen(url).read()		
	decoded_rates = all_rates.decode()
	pattern = "currency='([a-z,A-Z]{3})'\srate='([\d]+[.][\d]+)'"
	matched = re.findall(pattern, decoded_rates)
	# matched contains key/value pairs where keys are 3 letter currency codes (string) and values are rates (float)
	return matched

def calculate_result(amount, input_currency, output_currency, rates):
	#  simplify
	if(output_currency == 'EUR'):
		output_rate = 1
	if(input_currency == 'EUR'):
		input_rate = 1
	for item in rates:
		if(item[0] == input_currency):
			input_rate = item[1]
		if(item[0] == output_currency): #item[0] = string - currencies, item[1] = float - rates
			output_rate = item[1]

	
	return amount / decimal.Decimal(input_rate) * decimal.Decimal(output_rate)

def recognize_symbol(currency):
	# simplify... for example use .get(symbol) in decipher_symbol :)
	if((len(currency) != 3) or (not(currency.isupper()))):
		try:
			currency = decipher_symbol(currency)
		except KeyError:
			raise KeyError

	return currency

def convert_to_output_currency(amount, input_currency, output_currency, filtered_rates):
	if(output_currency == None):
		all_currencies = {}
		convert_to_euro = calculate_result(amount, input_currency, 'EUR', filtered_rates)
		two_places_result = str(round(convert_to_euro, 2))
		# If no output is set we have to explicitly add EUR because it's the base in our data source
		all_currencies['EUR'] = two_places_result
		# item[0] = string - currency code, item[1] = float - currency rate
		for item in filtered_rates:
			try:
				converted_value = calculate_result(amount, input_currency, item[0], filtered_rates)
			except UnboundLocalError:
				raise UnboundLocalError

			two_places_result = str(round(converted_value, 2))
			all_currencies[item[0]] = two_places_result

		return all_currencies

	else:
		try:
			converted_value = calculate_result(amount, input_currency, output_currency, filtered_rates)
		except UnboundLocalError:
			raise UnboundLocalError
		return converted_value
