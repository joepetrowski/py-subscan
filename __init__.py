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

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#
	# General API
	#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#
	# STAKING API
	#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	# Get the sum of staking rewards for an address.
	def staking_reward_sum(self, address: str, row=20, page=1):
		path = '{}scan/staking_history'.format(self.root_url)
		data = {
			'address' : address,
			'row' : row,
			'page' : page,
		}
		return self._subscan_post(path, data)

	# status:  'unbonding', 'bonded'
	# address: address of interest
	# locked:  0 or 1
	def staking_bond_list(self, status: str, address: str, locked=None, row=20, page=1):
		path = '{}wallet/bond_list'.format(self.root_url)
		data = {
			'status' : status,
			'address' : address,
			'row' : row,
			'page' : page,
		}
		if locked:
			assert(int(locked) == 0 or int(locked) == 1)
			data['locked'] = locked
		return self._subscan_post(path, data)

	# Information on validators who are in the active set.
	#
	# key:         int?
	# order:       'desc', 'asc'
	# order_field: 'rank_validator', 'bonded_nominators', 'bonded_owner', 'count_nominators',
	#              'validator_prefs_value'
	def staking_validators(self, key=None, order=None, order_field=None):
		path = '{}scan/staking/validators'.format(self.root_url)
		data = {}
		if key:
			data['key'] = key
		if order:
			data['order'] = order
		if order_field:
			data['order_field'] = order_field
		return self._subscan_post(path, data)

	# Information on waiting validators.
	#
	# key:         int?
	# order:       'desc', 'asc'
	# order_field: 'bonded_nominators', 'bonded_owner', 'count_nominators', 'validator_prefs_value'
	def staking_waiting_validator(self, key=None, order=None, order_field=None):
		path = '{}scan/staking/waiting'.format(self.root_url)
		data = {}
		if key:
			data['key'] = key
		if order:
			data['order'] = order
		if order_field:
			data['order_field'] = order_field
		return self._subscan_post(path, data)

	# Information about nominees.
	#
	# address:     address
	# order:       'asc', 'desc'
	# order_field: 'bonded_nominators', 'bonded_owner', 'count_nominators', 'validator_prefs_value'
	def staking_voted(self, address: str, order=None, order_field=None):
		path = '{}scan/staking/voted'.format(self.root_url)
		data = { 'address' : address }
		if order:
			data['order'] = order
		if order_field:
			data['order_field'] = order_field
		return self._subscan_post(path, data)

	# Information about nominators.
	#
	# address:     address
	# order:       'asc', 'desc'
	# order_field: 'rank_nominator', 'bonded'
	def staking_nominators(self, address: str, order=None, order_field=None, row=20, page=1):
		path = '{}scan/staking/nominators'.format(self.root_url)
		data = {
			'address' : address,
			'row' : row,
			'page' : page,
		}
		if order:
			data['order'] = order
		if order_field:
			data['order_field'] = order_field
		return self._subscan_post(path, data)

	# Stats about a list of eras for an address.
	def staking_era_stat(self, address: str, row=20, page=1):
		path = '{}scan/staking/era_stat'.format(self.root_url)
		data = {
			'address' : address,
			'row' : row,
			'page' : page,
		}
		return self._subscan_post(path, data)

	# Information about a particular validator.
	def staking_validator(self, stash: str):
		path = '{}scan/staking/validator'.format(self.root_url)
		data = { 'stash' : stash }
		return self._subscan_post(path, data)

	# Stats about a stash.
	def staking_bond_stat(self, stash: str, row=20, page=1):
		path = '{}scan/staking/validator/bond_stat'.format(self.root_url)
		data = {
			'stash' : stash,
			'row' : row,
			'page' : page,
		}
		return self._subscan_post(path, data)

	# Information about rewards and slashes on a particular address. For rewards, this is the
	# reward destination, which may not be the stash.
	def staking_reward_slash(self, address: str, row=20, page=1):
		path = '{}scan/account/reward_slash'.format(self.root_url)
		data = {
			'address' : address,
			'row' : row,
			'page' : page,
		}
		return self._subscan_post(path, data)

	# Unbonding chunks of an address.
	def staking_unbonding(self, address: str):
		path = '{}scan/staking/unbonding'.format(self.root_url)
		data = { 'address' : address }
		return self._subscan_post(path, data)

	# Information about a particular nominator.
	def staking_nominator(self, address: str):
		path = '{}scan/staking/nominator'.format(self.root_url)
		data = { 'address' : address }
		return self._subscan_post(path, data)

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#
	# PRICE API
	#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#
	# GOVERNANCE API
	#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
	#
	# RUNTIME API
	#
	# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
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