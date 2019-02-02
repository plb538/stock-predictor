 #!/usr/bin/env python

import fix_yahoo_finance as y
import matplotlib as plt
import numpy as np
from pandas_datareader import data as pdr
import traceback as tb

y.pdr_override()


class Company:
	def __init__(self, name):
		self.name = name


def sort_data(data):
	data = data.split('\n')
	data_dict = {}
	dates = []
	open_prices = []
	high_prices = []
	low_prices = []
	close_prices = []
	adj_close_prices = []
	vol_prices = []
	for i in data[1:]:
		l = i.split(',')
		if len(l) != 7:
			continue
		dates.append(l[0])
		open_prices.append(float(l[1]))
		high_prices.append(float(l[2]))
		low_prices.append(float(l[3]))
		close_prices.append(float(l[4]))
		adj_close_prices.append(float(l[5]))
		vol_prices.append(float(l[6]))
	data_dict['dates'] = dates
	data_dict['open_prices'] = open_prices
	data_dict['high_prices'] = high_prices
	data_dict['low_prices'] = low_prices
	data_dict['close_prices'] = close_prices
	data_dict['adj_close_prices'] = adj_close_prices
	data_dict['vol_prices'] = vol_prices

	return data_dict


if __name__ == '__main__':

	company0 = Company('AMD')

	output_dest = '/home/plb538/Repos/stock-predictor/test/test.txt'

	# Clear text file
	fd = open(output_dest, 'w')
	fd.close()

	fd = open(output_dest, 'a')
	fd.write("{} Summary\n\n".format(company0.name))

	while True:
		try:
			data = pdr.get_data_yahoo(company0.name, start='2017-01-01', end='2017-02-28')
		except ValueError:
			print("Retrying")
			pass
		else:
			break


	data = data.to_csv()
	fd.write(data)


	data_dict = sort_data(data)
	print(data_dict['dates'])


	#x_range = np.arange(1, len(close_prices)+1, 1)
	#print(x_range)

	#axis = plt.axes()
	#axis.set_xticks(x_range)
	#axis.set_yticks(close_prices)
	#axis.grid()
	#plt.plot(x_range, close_prices)
	#plt.show()

	fd.close()
