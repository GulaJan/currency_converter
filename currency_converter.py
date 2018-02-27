#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: Shared functions for both CLI and API

import urllib.request
import xmltodict
import json
import decimal
from constants import decipher_symbol

def fetch_rates():
	url = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
	xml_content = xmltodict.parse(urllib.request.urlopen(url).read())
	currency_rates_dict = {}
	
	for item in xml_content['gesmes:Envelope']['Cube']['Cube']['Cube']:
		currency_rates_dict[item['@currency']] = item['@rate']
	# currency = key and rates = value
	currency_rates_dict.update({'EUR':1})
	return currency_rates_dict

def calculate_result(amount, input_currency, output_currency, currency_rates):
	input_rate = currency_rates.get(input_currency)
	output_rate = currency_rates.get(output_currency)
	return decimal.Decimal(amount) / decimal.Decimal(input_rate) * decimal.Decimal(output_rate)

def recognize_symbol(currency, rates):
	if not rates.get(currency):
		currency = decipher_symbol(currency)
		if not currency:
			raise KeyError
	return currency

def convert_to_output_currency(amount, input_currency, output_currency, filtered_rates):
	if not output_currency:
		all_currencies = {}
		convert_to_euro = calculate_result(amount, input_currency, 'EUR', filtered_rates)
		two_places_result = str(round(convert_to_euro, 2))
		# If no output is set we have to explicitly add EUR because it's the base in our data source
		all_currencies['EUR'] = two_places_result
		for currency_code in filtered_rates:
			try:
				converted_value = calculate_result(amount, input_currency, currency_code, filtered_rates)
			except UnboundLocalError:
				raise UnboundLocalError

			two_places_result = str(round(converted_value, 2))
			all_currencies[currency_code] = two_places_result

		return all_currencies

	else:
		try:
			converted_value = calculate_result(amount, input_currency, output_currency, filtered_rates)
		except UnboundLocalError:
			raise UnboundLocalError
		return converted_value

