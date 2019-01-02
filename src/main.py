#!/usr/bin/python

import fix_yahoo_finance as y
from pandas_datareader import data as pdr
import traceback as tb

y.pdr_override()


if __name__ == '__main__':

	while True:
		try:
			data = pdr.get_data_yahoo('AMD', start='2017-01-01', end='2018-01-01')
		except ValueError:
			pass
		else:
			break

	data = data.to_csv('test.csv')
