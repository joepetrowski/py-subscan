import requests
import json
import time

class SubscanClient:
	def __init__(self, network):
		self.root_url = 'https://{}.subscan.io/api/'.format(network)

	# Request some data from the Subscan API.
	def _subscan_get(self, endpoint, params={}):
		try:
			response = requests.get(endpoint, params)
		except:
			print('Unable to connect to Subscan.')
		return self._process_response(response)

	# Post some data to the Subscan API.
	def _subscan_post(self, endpoint, post_data):
		header = {'Content-type' : 'application/json'}
		try:
			response = requests.post(
				endpoint,
				json=post_data,
				headers=header
			)
		except:
			print('Unable to connect to Subscan.')
		return self._process_response(response)

	# Process HTTP response.
	def _process_response(self, response):
		data = {}
		if response and response.ok:
			data = json.loads(response.text)
		else:
			error_message = 'Response Error: {}'.format(response.status_code)
			print(error_message)
			data = { 'error' : error_message }
		return data

	# Get information about a block.
	# `block_hash` overrides `block_number`.
	def block(self, block_number=None, block_hash=None):
		path = '{}open/block'.format(self.root_url)
		data = {}
		if block_hash:
			block_hash = str(block_hash)
			assert(block_hash[0:2] == '0x')
			assert(len(block_hash) == 66)
			data = { 'block_hash' : block_hash }
		elif block_number:
			data = { 'block_num' : int(block_number) }
		return self._subscan_post(path, data)

	# Get information about an account.
	def account(self, address, row=0, page=None):
		path = '{}open/account'.format(self.root_url)
		data = {
			'address':str(address),
			'row':row
		}
		if page:
			data['page'] = str(page)
		return self._subscan_post(path, data)

	# Get information about rewards and slashes for an account.
	def reward_slash(self, address, row=20, page=None):
		path = '{}scan/account/reward_slash'.format(self.root_url)
		data = {
			'address':str(address),
			'row':row
		}
		if page:
			data['page'] = str(page)
		return self._subscan_post(path, data)

	# Get information about extrinsics from an account.
	def extrinsics(self, address, row=20, page=None):
		path = '{}open/account/extrinsics'.format(self.root_url)
		data = {
			'address':str(address),
			'row':row
		}
		if page:
			data['page'] = str(page)
		return self._subscan_post(path, data)

	# Get information about an extrinsic.
	def extrinsic(self, extrinsic):
		path = '{}open/extrinsic'.format(self.root_url)
		data = {
			'hash':str(extrinsic),
		}
		return self._subscan_post(path, data)

	# Get a list of currency conversions available.
	def currencies(self):
		path = '{}open/currencies'.format(self.root_url)
		data = {}
		return self._subscan_post(path, data)

	# Get price at a given time `at`. `at` can be epoch time or block number.
	def price(self, at=None):
		path = '{}open/price'.format(self.root_url)
		if not at:
			at = int(time.time())
		data = { 'time' : at }
		return self._subscan_post(path, data)

	# Convert price at a given time `at`. `at` can be epoch time or block number.
	def price_converter(self, value, base, quote, at=None):
		path = '{}open/price'.format(self.root_url)
		if not at:
			at = int(time.time())
		data = {
			'value' : value,
			'from' : base,
			'quote' : quote,
			'time' : at
		}
		return self._subscan_post(path, data)
