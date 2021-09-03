import requests
import json
import time

class SubscanClient:
	def __init__(self, network, api_key):
		self.root_url = 'https://{}.subscan.io/api/'.format(network)
		self.api_key = api_key

	# Request some data from the Subscan API.
	def _subscan_get(self, endpoint, params={}):
		try:
			response = requests.get(endpoint, params)
		except:
			print('Unable to connect to Subscan.')
		return self._process_response(response)

	# Post some data to the Subscan API.
	def _subscan_post(self, endpoint, post_data):
		header = {
			'Content-type' : 'application/json',
			'X-API-Key' : str(self.api_key),
		}
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

	# General API

	# Subscan server timestamp
	def general_timestamp(self):
		return self._subscan_post(self.root_url + 'now')

	# Subscan global stats
	def general_metadata(self):
		return self._subscan_post(self.root_url + 'scan/metadata')

	# Array of blocks from the connected chain. Requires `row` and `page`.
	def general_blocks(self, row=20, page=1):
		path = self.root_url + 'scan/blocks'
		data = {
			'row' : row,
			'page': page,
		}
		return self._subscan_post(path, data)

	# Get information about a block.
	# `block_hash` overrides `block_number`.
	def general_block(self, block_number=None, block_hash=None):
		path = '{}scan/block'.format(self.root_url)
		data = {}
		if block_hash:
			block_hash = str(block_hash)
			assert(block_hash[0:2] == '0x')
			assert(len(block_hash) == 66)
			data = { 'block_hash' : block_hash }
		elif block_number:
			data = { 'block_num' : int(block_number) }
		return self._subscan_post(path, data)

	# Get a list of extrinsics.
	def general_extrinsics(self, 
		signed=None,
		address=None,
		module=None,
		call=None,
		block_num=None,
		row=20,
		page=1
	):
		path = '{}scan/extrinsics'.format(self.root_url)
		data = {
			'row':row,
			'page': page,
		}
		if signed:
			data['signed'] = str(signed)
		if address:
			data['address'] = str(address)
		if module:
			data['module'] = str(module)
		if call:
			data['call'] = str(call)
		if block_num:
			data['block_num'] = str(block_num)
		return self._subscan_post(path, data)

	# Get information about an extrinsic. Index takes the form `blocknumber-index` and supercedes
	# hash.
	def general_extrinsic(self, extrinsic_index=None, hash=None):
		path = '{}scan/extrinsic'.format(self.root_url)
		data = {}
		if extrinsic_index:
			data = { 'extrinsic_index' : extrinsic_index }
		elif hash:
			data = { 'hash' : hash }
		return self._subscan_post(path, data)

	# Get a list of events.
	def general_events(self, module=None, call=None, block_number=None, row=20, page=1):
		path = '{}scan/events'.format(self.root_url)
		data = {
			'row' : row,
			'page' : page,
		}
		if module:
			data['module'] = module
		if call:
			data['call'] = call
		if block_number:
			data['block_number'] = block_number
		return self._subscan_post(path, data)

	# Get detailed information on a particular event. `event_index` takes the form
	# `blocknumber-index`.
	def general_event(self, event_index=None):
		path = '{}scan/event'.format(self.root_url)
		data = {}
		if event_index:
			data['event_index'] = event_index
		return self._subscan_post(path, data)

	# Search for a block number, account, or extrinsic.
	def general_search(self, key, row=20, page=1):
		path = '{}scan/search'.format(self.root_url)
		data = { 'key' : key }
		return self._subscan_post(path, data)

	# Get time-based network statistics.
	#
	# start:    yyyy-mm-dd
	# end:      yyyy-mm-dd
	# format:   'day', 'hour', '6hour'
	# category: 'transfer', 'extrinsic', 'NewAccount', 'ActiveAccount', 'Treasury', 'TreasurySpend',
	#           'Unbond', 'UnbondKton', 'Fee', 'Bonded', 'BondedKton'
	def general_daily(self, start, end, format, category):
		path = '{}scan/daily'.format(self.root_url)
		data = {
			'start' : start,
			'end' : end,
			'format' : format,
			'category' : category,
		}
		return self._subscan_post(path, data)

	# List of transfers.
	def general_transfers(self, address=None, from_block=None, to_block=None, row=20, page=1):
		path = '{}scan/transfers'.format(self.root_url)
		data = {
			'row' : row,
			'page' : page,
		}
		if address:
			data['address'] = address
		if from_block:
			data['from_block'] = from_block
		if to_block:
			data['to_block'] = to_block
		return self._subscan_post(path, data)

	# Check if a hash is a block or an extrinsic.
	def general_check_hash(self, hash: str):
		path = '{}scan/check_hash'.format(self.root_url)
		assert(hash[0:2] == '0x')
		assert(len(hash) == 66)
		data = { 'hash' : hash }
		return self._subscan_post(path, data)

	# Get a list of accounts.
	#
	# order:       'desc', 'asc'
	# order_field: 'balance', 'kton_balance', 'kton_balance', 'kton_lock'
	# filter:      'validator', 'nominator', 'councilMember', 'techcomm', 'registrar'
	def general_accounts(self, order=None, order_field=None, filter=None, row=20, page=1):
		path = '{}scan/accounts'.format(self.root_url)
		data = {
			'row' : row,
			'page' : page,
		}
		if order:
			data['order'] = order
		if order_field:
			data['order_field'] = order_field
		if filter:
			data['filter'] = filter
		return self._subscan_post(path, data)

	# Information about the network token.
	def general_token(self):
		path = '{}scan/token'.format(self.root_url)
		return self._subscan_post(path)


'''
OLD API, NEED TO UPDATE

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
'''