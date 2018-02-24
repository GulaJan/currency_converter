#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: API using Flask

import sys
import decimal
from flask import Flask, request, jsonify
from currency_converter import fetch_rates, convert_to_output_currency, recognize_symbol
app = Flask(__name__)

@app.route('/currency_converter')
def api():
	amount = request.args.get('amount')
	input_currency = request.args.get('input_currency')
	output_currency = request.args.get('output_currency')
	if(amount == None):
		response = jsonify({'error': {'code' : '201', 'message': 'Amount required'}})
		response.status_code = 201
		return response
	if(not(amount.replace('.','',1).isdigit())):
		response = jsonify({'error': {'code' : '201', 'message': 'Amount has to be a positive number'}})
		response.status_code = 201
		return response
	if(input_currency == None):
		response = jsonify({'error': {'code' : '201', 'message': 'Input currency required'}})
		response.status_code = 201
		return response
	
	try:
		input_currency = recognize_symbol(input_currency)
	except KeyError:
		response = jsonify({'error': {'code' : '202', 'message': 'Input symbol was not recognized'}})
		response.status_code = 202
		return response

	if(output_currency != None):
		try:
			output_currency = recognize_symbol(output_currency)
		except KeyError:
			response = jsonify({'error': {'code' : '202', 'message': 'Output symbol was not recognized'}})
			response.status_code = 202
			return response

	decimal_amount = decimal.Decimal(amount)

	rates = fetch_rates()

	if(output_currency == None):
		try:
			all_currencies = convert_to_output_currency(decimal_amount, input_currency, output_currency, rates)
		except UnboundLocalError:
			response = jsonify({'error': {'code' : '202', 'message': 'Input currency was not recognized'}})
			response.status_code = 202
			return response

		return jsonify({'input': {'amount': str(decimal_amount), 'currency': input_currency}, 'output': all_currencies})

	else:
		try:
			converted_val = convert_to_output_currency(decimal_amount, input_currency, output_currency, rates)
		except UnboundLocalError:
			response = jsonify({'error': {'code' : '202', 'message': 'Input or output currency was not recognized'}})
			response.status_code = 202
			return response

		two_decimal_places = str(round(converted_val, 2))
		return jsonify({'input': {'amount': str(decimal_amount), 'currency': input_currency}, 'output': {output_currency : two_decimal_places}})

if __name__ == '__main__' :
	app.run('127.0.0.1', 5000)
	#Set for localhost listening on the default port 5000
	#To reach from outside of localhost use these settings:
	#app.run('0.0.0.0')
		