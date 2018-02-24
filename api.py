#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: API using Flask

import sys
import decimal
from flask import Flask, request, jsonify
from currency_converter import fetch_rates, rates_to_array, convert, recognize_symbol
app = Flask(__name__)

@app.route('/currency_converter')
def api():
	amount = request.args.get('amount')
	input_currency = request.args.get('input_currency')
	output_currency = request.args.get('output_currency')
	if(not(amount.replace('.','',1).isdigit())):
		return "Amount has to be a positive number!"
	if(amount == None):
		return "Amount required!"
	if(input_currency == None):
		return "Input currency required!"
	if(input_currency == output_currency):
		return "Output currency has to differ from the input currency!"
	
	rates = fetch_rates()
	filtered_rates = rates_to_array(rates)

	currencies = {'input_currency': input_currency, 'output_currency':output_currency}
	currencies = recognize_symbol(currencies)
	
	if(currencies == KeyError):	
		return "Input or output symbol was not recognized!\n"

	input_currency = currencies['input_currency']
	output_currency = currencies['output_currency']

	decimal_amount = decimal.Decimal(amount)

	if(output_currency == None):
		try:
			all_currencies = convert(decimal_amount, input_currency, output_currency, filtered_rates)
		except(UnboundLocalError):
			return "Input currency was not recognized!\n"

		return jsonify({'input': {'amount': str(decimal_amount), 'currency': input_currency}, 'output': all_currencies})

	else:
		converted_val = convert(decimal_amount, input_currency, output_currency, filtered_rates)
		if(converted_val == UnboundLocalError):
			return "Input or output currency was not recognized!\n"

		two_decimal_places = str(round(converted_val, 2))
		return jsonify({'input': {'amount': str(decimal_amount), 'currency': input_currency}, 'output': {output_currency : two_decimal_places}})

if __name__ == '__main__' :
	app.run('127.0.0.1', 5000)
	#Set for localhost listening on the default port 5000
	#To reach from outside of localhost use these settings:
	#app.run('0.0.0.0')
		