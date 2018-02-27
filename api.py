#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: API using Flask

import sys
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
		if output_currency:
			output_currency = recognize_symbol(output_currency, rates)
	except KeyError:
		err_msg = 'Input or output symbol was not recognized'

	if err_msg:
		response = jsonify({'error': {'code' : '202', 'message': err_msg}})		
		response.status_code = 202
		return response

	try:
		converted_val = convert_to_output_currency(amount, input_currency, output_currency, rates)
	except UnboundLocalError:
		response = jsonify({'error': {'code' : '202', 'message': 'Input or output currency was not recognized'}})
		response.status_code = 202
		return response
	if output_currency:
		converted_val = str(round(converted_val, 2))
		output = {output_currency : converted_val}
	else:
		output = converted_val
	return jsonify({'input': {'amount': str(amount), 'currency': input_currency}, 'output': output })

if __name__ == '__main__' :
	app.run('127.0.0.1', 5000)
	#Set for localhost listening on the default port 5000
	#To reach from outside of localhost use these settings:
	#app.run('0.0.0.0')
		