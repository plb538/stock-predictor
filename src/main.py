#!/usr/bin/python

from pandas_datareader import data as pdr

import fix_yahoo_finance as y

y.pdr_override()


if __name__ == '__main__':

	data = pdr.get_data_yahoo('AMD', start='2017-01-01', end='2018-01-01').to_csv('test.csv')
	print(data)


