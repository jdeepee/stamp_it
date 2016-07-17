from flask import Flask, request, render_template, redirect
from model import *
from passlib.hash import bcrypt
from encoder import AlchemyEncoder, JoinEncoder
from coinbase.wallet.client import Client
import uuid, hashlib, requests, os, time, json, urllib, urllib2
from celery import Celery
from config import *

application = Flask(__name__)

celery_app = Celery('api', broker='redis://localhost:6379/0', CELERY_RESULT_BACKEND='redis://localhost:6379/0')
celery_app.conf.update(application.config)

@celery_app.task()
def to_the_blockchain(file_hash, company_id, document_name):
	api_call = requests.get('https://www.proofofexistence.com/api/v1/register', data=file_hash)

	if api_call.status_code == 200:
		body = api_call.json()
		client = Client(os.environ['COINBASE_API_KEY'], os.environ['COINBASE_API_SECRET'])

		tx = client.send_money('2bbf394c-193b-5b2a-9155-3b4732659ede', 
                       {'to': str(body['pay_address']),
                        'amount': int(float(body['price'])*float(0.00000001)),
                        'currency': 'BTC',
                        'idem': '9316dd16-0c05'})

		check = False
		while check == False:
			api_call_check = requests.get('https://www.proofofexistence.com/api/v1/status', data=file_hash)
			body = api_call_check.json()

			if body['pending'] == 'true':
				time.sleep(10)

			else:
				query = db.session.query(Company).filter(Company.id == company_id).first()
				company_name = query.company_name
				tx = body['tx']
				id = uuid.uuid4()
				try:
					data = Document(id=id, company_id=company_id, company_name=company_name, blockchain_transaction=tx, document_name=document_name)
					db.session.add(data)
					db.session.commi()

				except:
					db.session.rollback()
					return None

				finally:
					db.session.close()

				check = True
				return
	else:
		return None

@application.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@application.route('/company', methods=['POST', 'GET'])
def company_signup():
	error = ''

	if request.method == 'POST':
		name = request.form['name']
		id = uuid.uuid4()

		try:
			data = Company(id=id, name=name)
			db.session.add(data)
			db.session.commit()

		except:
			db.session.rollback()
			error = "Something went wrong"
			raise

		finally:
			db.session.close()

		return redirect('/company/'+str(id), code=200)

	return render_template('new_company.html', error=error)

@application.route('/companies', methods=["GET"])
def all_companies():
	error = ''

	if request.method == "GET":
		data = db.session.query(Company).all()
		data = json.dumps(data, cls=AlchemyEncoder)
		data = json.loads(data)
		data = [item for item in data]
		return render_template("all_companies.html", data=data)

@application.route('/company/<id>', methods=["GET"])
def company_information(id):
	if request.method == 'GET':
		#try:
		data = db.session.query(Company, Document, DocumentElement).outerjoin(Document).outerjoin(DocumentElement).filter(Company.id == id).all()

		# except:
		# 	db.session.rollback()
		# 	data = db.session.query(Company).filter(Company.id == id).all()

		if data is None:
			return render_template("individual_company.html", data=None)

		response = json.dumps(data, cls=JoinEncoder)
		response = json.loads(response)
		data = [{"Company id": response[0]['Company']['id'], "Company name": response[0]['Company']['name']},{"Document name": response[0]['Document']['document_name'], "Blockchain transaction": response[0]['Document']['blockchain_transaction'], "Time Uploaded": response[0]['Document']["time_uploaded"]},{"Document Elements": "Cash, Revenue, Recievables and Debt"}]
		return render_template("individual_company.html", data=data)

@application.route('/company/<id>/newdocument', methods=["GET", "POST"])
def new_document(id):
	if request.method == "POST":
		file = request.files['file']
		document_name = request.form['name']
		filename = file.filename
		file.save('/Users/Josh/Documents/stamp_it/api/static/'+filename)
		file_hash = hashlib.sha256(open('/Users/Josh/Documents/stamp_it/api/static/'+filename,'rb').read()).hexdigest()

		#task = to_the_blockchain.delay(file_hash, id, document_name)

		#task_1_result = task.get(timeout=1)
		#Celery task here to upload hash to blockchain and wait for transaction and then update database values
		#After update occurs also to check to see if anyone who is interested in this company should be notified
		#Also insert into document elements with each element from the document

		# values = {'d': file_hash}

		# data = urllib.urlencode(values)
		# api_call = urllib2.Request('https://www.proofofexistence.com/api/v1/register', data)
		# response = urllib2.urlopen(api_call) 
		# the_page = response.read()

		# if response.getcode() == 200:
		# 	json_data = json.loads(the_page)
		# 	client = Client(os.environ['COINBASE_API_KEY'], os.environ['COINBASE_API_SECRET'])
		# 	primary_account = client.get_primary_account()

		# 	primary_account.send_money(to=str(json_data['pay_address']), amount=int(json_data['price']*float(0.00000001)), currency="BTC")
		# 	check = False
		# 	while check == False:
		# 		api_call_check = requests.get('https://www.proofofexistence.com/api/v1/status', data=file_hash)
		# 		body = api_call_check.json()

		# 		if body['pending'] == 'true':
		# 			time.sleep(10)

		# 		else:
		# 			query = db.session.query(Company).filter(Company.id == company_id).first()
		# 			company_name = query.company_name
		# 			tx = body['tx']
		# 			id = uuid.uuid4()
		# 			try:
		# 				data = Document(id=id, company_id=company_id, company_name=company_name, blockchain_transaction=tx, document_name=document_name)
		# 				db.session.add(data)
		# 				db.session.commi()

		# 			except:
		# 				db.session.rollback()

		# 			finally:
		# 				db.session.close()

		# 			check = True
		# 			return
		# else:
		# 	return render_template('new_document.html', error='request failed')

		return render_template('new_document.html', file_hash=file_hash)
		#return redirect('/company/'+id, code=200)
	return render_template('new_document.html')

# @application.route('/insertdata', methods=["GET"])
# def go():
# 	id='e1e537ad-5640-4d43-aec6-9002b035ecc5'
# 	db.session.query(Company).filter_by(id = id).update({'name': 'Company B'})
# 	db.session.commit()
# 	db.session.close()

# 	return 'done'

@application.route('/company/<id>/document/<id_document>', methods=["GET"])
def company_document(id, id_document):
	if request.method == "GET":
		data = db.session.query(Company, Document).join(Company).filter(Company.id == id, Document.id == id_document).all()

		if data is None:
			return render_template("document.html", data=None)

		response = json.dumps(data, cls=AlchemyEncoder)
		return render_template("document.html", data=response)

@application.route('/company<id>/element/<id_element>', methods=['GET'])
def company_document_element(id, id_element):
	if request.method == "GET":
		data = db.session.query(Company, DocumentElement).joing(Company).filter(Company.id == id, DocumentElement == id_element).first()

		if data is None:
			return render_template("element.html", data=None)

		response = json.dumps(data, cls=AlchemyEncoder)
		return render_template("element.html", data=response)

@application.route('/interest', methods=["GET", 'POST'])
def interest_creation():
	error = ''

	if request.method == "POST":
		data = request.form()
		company_name = data['name']
		test_type = data['type']
		threshold = data['threshold']
		id = uuid.uuid4()
		test_id = uuid.uuid4()

		query = db.session.query(Company).filter(Company.name == company_name).first()
		company_id = query.id

		try:
			data = Test(id=test_id, company_id=company_id, test_type=test_type, threshold=threshold)
			db.session.add(data)
			db.session.commit()

		except:
			db.session.rollback()
			error = "Something went wrong"
			raise

		finally:
			db.session.close()

		try:
			data = Interest(id=id, company_id=company_id, test_id=test_id)
			db.session.add(data)
			db.session.commit()

		except:
			db.session.rollback()
			error = "Something went wrong"
			raise

		finally:
			db.session.close()

		return redirect('/interest'+id, code=200)
	return render_template("new_interest.html", form=form, error=error)

@application.route('/interests/user/ddf7140c-2175-4c3c-b39f-86235ad0786e/', methods=["GET"])
def all_interests():
	error = ''

	if request.method == "GET":
		data = db.session.query(Interest).all()
		return render_template("interests.html", data=data)

@application.route('/interest/<id>', methods=["GET"])
def interest_information(id):
	error = ''

	if request.method == 'GET':
		data = db.session.query(Interest, Test).join(Test).filter(Interest.id == id).all()
		return render_template("interest.html", data=data)

@application.route('/interest/<id>/test/<id_test>', methods=["GET"])
def test_result_information(id, id_test):
	error = ''

	if request.method == "GET":
		data = db.session.query(TestResult).filter(TestResult.id == id_test, TestResult.test_id == id).all()
		return render_template('results.html', data=data)

if __name__ == '__main__':
	application.run(debug=True)
