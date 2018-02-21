#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: API using Flask

from flask import Flask, request
from cli import fetchData, filterData, convert
app = Flask(__name__)

@app.route('/currency_converter')
def api():
	amount = request.args.get('amount')
	inCurr = request.args.get('input_currency')
	outCurr = request.args.get('output_currency')
	return 'Result : %s' % result

if __name__ == '__main__' :
	app.run('127.0.0.1', 5002, debug = True)
