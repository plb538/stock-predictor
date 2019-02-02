 #!/usr/bin/env python

import fix_yahoo_finance as y
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr

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
	start_date = '2017-01-01'
	end_date = '2017-01-31'
	output_dir = '/home/plb538/Repos/stock-predictor/test/'
	output_file = 'test.txt'
	output_file_dest = "{}/{}".format(output_dir, output_file)

	# Create/erase text file
	fd = open(output_file_dest, 'w')
	fd.close()

	# Open file
	fd = open(output_file_dest, 'a')
	fd.write("{} Summary\n\n".format(company0.name))

	# Try to get data from Yahoo
	attempts = 0
	while True:
		try:
			data = pdr.get_data_yahoo(company0.name, start=start_date, end=end_date)
		except ValueError:
			print("Retrying...")
			if attempts == 5:
				print("Failed to download data from Yahoo.")
				exit(0)
			else:
				attempts += 1
		else:
			print("Successfully downloaded data from Yahoo.")
			break

	# Write data to file
	data = data.to_csv()
	fd.write(data)
	fd.close()

	# Turn data into dict
	data_dict = sort_data(data)

	# Setup X coordinates
	x_data = data_dict['dates']

	# Setup Y coordinates
	y_data_open_prices = data_dict['open_prices']
	y_data_close_prices = data_dict['close_prices']
	y_data_low_prices = data_dict['low_prices']
	y_data_high_prices = data_dict['high_prices']

	### PLOT 1 ###
	plt.figure()

	# Setup axis
	axis = plt.axes()
	axis.grid()

	# Setup plots
	plt.plot(x_data, y_data_open_prices, 'r-')
	plt.plot(x_data, y_data_close_prices, 'g-')
	plt.plot(x_data, y_data_low_prices, 'r:')
	plt.plot(x_data, y_data_high_prices, 'g:')
	plt.legend(['Open', 'Close', 'Low', 'High'])

	# Plot details
	plt.title("{} Summary From {} To {}".format(company0.name, start_date, end_date))
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.xticks(rotation='vertical')

	plt.tight_layout()

	# Show/save plots
	# plt.show()
	plt.savefig("{}/{}".format(output_dir, 'summary.png'))
	plt.close()
	######

	### PLOT 2 ###
	fig, (ax1, ax2) = plt.subplots(2, 1)
	ax1.plot(x_data, y_data_open_prices, 'r-')
	ax1.plot(x_data, y_data_close_prices, 'g-')
	ax1.legend(['Open', 'Close'])
	ax1.grid()
	ax1.set_title("{} Open/Close Prices From {} To {}".format(company0.name, start_date, end_date))
	ax1.set_xlabel('Date')
	ax1.set_ylabel('Price')
	for tick in ax1.get_xticklabels():
		tick.set_rotation(90)

	ax2.plot(x_data, y_data_low_prices, 'r-')
	ax2.plot(x_data, y_data_high_prices, 'g-')
	ax2.legend(['Low', 'High'])
	ax2.grid()
	ax2.set_title("{} Low/High Prices From {} To {}".format(company0.name, start_date, end_date))
	ax2.set_xlabel('Date')
	ax2.set_ylabel('Price')
	for tick in ax2.get_xticklabels():
		tick.set_rotation(90)

	plt.tight_layout()

	# Show/save plots
	# plt.show()
	plt.savefig("{}/{}".format(output_dir, 'comparison.png'))
	plt.close()
	######

	print("Finished.")
