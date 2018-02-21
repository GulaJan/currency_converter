
#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
# Author: Jan Gula
# Date: 02/2018
# Project: mapping the symbol of a currency to its 3 letter abbreviation

def decipherSymbol(symbol):
	# Note: Countries with same currency symbols e.g. US Dollars and AU Dollars have their default currency
	# USD for [AUD CAD HKD MXN NZD SGD], DKK for [SEK, ISK, NOK], JPY for [CNY]
	return{
		chr(8364): 'EUR',
		chr(36): 'USD',
#			chr(36): 'AUD',
#			chr(36): 'CAD',
#			chr(36): 'HKD',
#			chr(36): 'MXN',
#			chr(36): 'NZD',
#			chr(36): 'SGD',
		chr(165): 'JPY',
#			chr(165): 'CNY',
		chr(1083) + chr(1074): 'BGN',
		chr(75) + chr(269): 'CZK',
		chr(107) + chr(114): 'DKK',
#			chr(107) + chr(114): 'SEK',
#			chr(107) + chr(114): 'ISK',
#			chr(107) + chr(114): 'NOK',
		chr(163): 'GBP',
		chr(70) + chr(116): 'HUF',
		chr(122) + chr(322): 'PLN',
		chr(108) + chr(101) + chr(105): 'RON',
		chr(67) + chr(72) + chr(70): 'CHF',
		chr(107) + chr(110): 'HRK',
		chr(8381): 'RUB',
		chr(8378): 'TRY',
		chr(82) + chr(36): 'BRL',
		chr(82) + chr(112): 'IDR',
		chr(8362): 'ILS',
		chr(8377): 'INR',
		chr(8361): 'KRW',
		chr(82) + chr(77): 'MYR',
		chr(8369): 'PHP',
		chr(3647): 'THB',
		chr(82): 'ZAR',											
	}[symbol]
