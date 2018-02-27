#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: API using Flask

import sys
# decimal still needed :thinking_face: ?
import decimal
from flask import Flask, request, jsonify
from currency_converter import fetch_rates, convert_to_output_currency, recognize_symbol
app = Flask(__name__)

@app.route('/currency_converter')
def api():
	amount = request.args.get('amount')
	input_currency = request.args.get('input_currency')
	output_currency = request.args.get('output_currency')
	err_msg = ""
	if not amount:
		err_msg = 'Amount required'
	# Supposedly fastest way to check if a string is a number, benchmark results https://i.stack.imgur.com/DFoK6.png
	# Problem discussed here https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
	elif not(amount.replace('.','',1).isdigit()):
		err_msg = 'Amount has to be a positive number'
	elif not input_currency:
		err_msg = 'Input currency required'

	if err_msg:
		response = jsonify({'error': {'code' : '201', 'message': err_msg}})		
		response.status_code = 201
		return response

	rates = fetch_rates()

	try:
		input_currency = recognize_symbol(input_currency, rates)
		# if output_currency:
		if(output_currency != None):
			output_currency = recognize_symbol(output_currency, rates)
	except KeyError:
		err_msg = 'Input or output symbol was not recognized'

	# why ( ) ... L29 not
	if(err_msg):
		response = jsonify({'error': {'code' : '202', 'message': err_msg}})		
		response.status_code = 202
		return response

	decimal_amount = decimal.Decimal(amount)

	# L50-L70 I see duplicate code > merge it please
	if not output_currency :
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
		
