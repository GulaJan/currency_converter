# Currency converter in Python
## Task
My task was to implement a **Command Line Interface (CLI)** and an **Application Programming Interface (API)** of a currency converter using the Python language.
## Implementation
The first step was to download the current currency rates for this purpose I've used the **urllib.request** command to download them in a .XML format from (http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml).  
After fetching our data it was necessary to filter them leaving only the currency name and rate, this was solved by a **regular expression**. In these filtered data we could easily find the input and output currency.   A tricky part of the implementation was that the currency could be inserted by its symbol, which ment I've had to map the symbols to its 3 letter abbreviation. This is done in the **constants.py** file. This also brought up a problem with currencies having the same symbol e.g. USD and AUD both have $. My solution to this problem was to have a default currency for each case. Default currencies are defined in the constants.py file.  
The last step was to finish the conversion. Any conversion could be done by this formula: **amount / input_currency * output_currency**    
The converted amount was then represented using JSON's library for Python.  
After we've implemented the CLI functions the only thing left was to implement an API. I've done this by using the **Flask framework for Python** that accepts requests and writes responses using JSON's jsonify.
## Usage
### CLI
	python3 ./currency_converter.py --amount 500 --input_currency=CZK --output_currency=USD
### API
	python3 ./api.py

	For a localhost test

	127.0.0.1:5000/currency_converter?amount=0.9&input_currency=EUR&output_currency=CZK
