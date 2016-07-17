import urllib2, urllib, json, hashlib, os
from coinbase.wallet.client import Client

file_hash = str(hashlib.sha256(open('/Users/Josh/Documents/stamp_it/data_examples/MasterDataBook v2.xlsx', 'rb').read()).hexdigest())

values = {'d': file_hash}

data = urllib.urlencode(values)
api_call = urllib2.Request('https://www.proofofexistence.com/api/v1/register', data)
response = urllib2.urlopen(api_call) 
the_page = response.read()

json_data = json.loads(the_page)

print json_data['price']*float(0.00000001)

print int(float(json_data['price'])*float(0.00000001))

if response.getcode() == 200:
	json_data = json.loads(the_page)
	client = Client(os.environ['COINBASE_API_KEY'], os.environ['COINBASE_API_SECRET'])
	primary_account = client.get_primary_account()

	primary_account.send_money(to=str(json_data['pay_address']), amount=int(json_data['price']*float(0.00000001)), currency="BTC")
	check = False
	while check == False:
		api_call = urllib2.Request('https://www.proofofexistence.com/api/v1/register', data)
		response = urllib2.urlopen(api_call) 
		the_page = response.read()

		body = json.loads(the_page)

		if body['pending'] == 'true':
			time.sleep(10)

		else:
			print body