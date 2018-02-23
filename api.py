#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: API using Flask
import json
from flask import Flask, request, jsonify
from cli import fetchData, filterData, convert, printJSON
app = Flask(__name__)

@app.route('/currency_converter')
def api():
	amount = request.args.get('amount')
	inCurr = request.args.get('input_currency')
	outCurr = request.args.get('output_currency')
	data = fetchData()
	filteredData = filterData(data)
	flamount = float(amount)
	res = convert(flamount, inCurr, outCurr, filteredData)
	result = "%.2f" % res 
	string = json.dumps({'input': {'amount': amount, 'currency': inCurr}, 'output': {outCurr : result}}, indent = 4, sort_keys=True)
	return jsonify(string)

if __name__ == '__main__' :
	app.run('127.0.0.1', 5003, debug = True)
