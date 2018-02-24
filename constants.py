
#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# File: mapping the symbol of a currency to its 3 letter abbreviation

def decipher_symbol(symbol):
	# Note: Countries with same currency symbols e.g. US Dollars and AU Dollars have their default currency
	# USD for [AUD CAD HKD MXN NZD SGD], DKK for [SEK, ISK, NOK], JPY for [CNY]
	return{
		'€': 'EUR',
		'$': 'USD',
#			'$': 'AUD',
#			'$': 'CAD',
#			'$': 'HKD',
#			'$': 'MXN',
#			'$': 'NZD',
#			'$': 'SGD',
		'¥': 'JPY',
#			'¥': 'CNY',
		'л' + 'в': 'BGN',
		'K' + 'č': 'CZK',
		'k' + 'r': 'DKK',
#			'k' + 'r': 'SEK',
#			'k' + 'r': 'ISK',
#			'k' + 'r': 'NOK',
		'£': 'GBP',
		'F' + 't': 'HUF',
		'z' + 'ł': 'PLN',
		'l' + 'e' + 'i': 'RON',
		'C' + 'H' + 'F': 'CHF',
		'k' + 'n': 'HRK',
		'₽': 'RUB',
		'₺': 'TRY',
		'R' + '$': 'BRL',
		'R' + 'p': 'IDR',
		'₪': 'ILS',
		'₹': 'INR',
		'₩': 'KRW',
		'R' + 'M': 'MYR',
		'₱': 'PHP',
		'฿': 'THB',
		'R': 'ZAR',											
	}[symbol]
