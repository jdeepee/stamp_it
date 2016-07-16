from flask import Flask, request, render_template, redirect
from models.model import User, Company, Interest, Test, TestResult, DocumentElement, Document
from passlib.hash import bcrypt
from models.encoder import AlchemyEncoder, JoinEncoder
from coinbase.wallet.client import Client
import uuid, hashlib, requests, os, time
from celery import Celery

application = Flask(__name__)
UPLOAD_FOLDER = '/static/'
client = Client(os.environ['COINBASE_API_KEY'], os.environ['COINBASE_API_SECRET'])

application.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
application.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

@celery.task
def to_the_blockchain(file_hash):
	api_call = requests.get('https://www.proofofexistence.com/api/v1/register', data=file_hash)

	if api_call.status_code == 200:
		body = api_call.json()

		tx = client.send_money('2bbf394c-193b-5b2a-9155-3b4732659ede', 
                       {'to': body['pay_address'],
                        'amount': int(float(body['price'])*float(0.00000001)),
                        'currency': 'BTC',
                        'idem': '9316dd16-0c05'})

		check = False:
		while check == False:
			api_call_check = requests.get('https://www.proofofexistence.com/api/v1/status', data=file_hash)
			body = api_call_check.json()

			if body['pending'] == 'true':
				time.sleep(10)

			else:
				#execute database code
				check = True
				return
	else:
		return None

@application.route('/', methods=['GET'])
def index():
	return render_template("index.html")

# @application.route('/signup', methods=['POST', 'GET'])
# def signup():
# 	error = ''

# 	if request.method == "POST": 
# 		data = request.form()
# 		username = data['username']
# 		password = bcrypt.encrypt(data['password'])
# 		email = data['email']
# 		name = data['name']
# 		id = uuid.uuid4()

# 		try:
# 			data = User(id=id, username=username, password=password, email=email, name=name)
# 			db.session.add(data)
# 			db.session.commit()

# 		except:
# 			db.session.rollback()
# 			error = 'Something went wrong'
# 			raise

# 		finally:
# 			db.session.close()

# 		return redirect('/', code=200)

# 	return render_template("signup.html", error=error, form=form)

@application.route('/company', methods=['POST', 'GET'])
def company_signup():
	error = ''

	if request.method == 'POST':
		data = request.form()
		name = data['name']
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

		return redirect('/company/'+id, code=200)

	return render_template('new_company.html', form=form, error=error)

@application('/companies', methods=["GET"])
def all_companies():
	error = ''

	if request.method == "GET":
		data = db.session.query(Company).all()

		return render_template("all_companies.html", data=data)

@application.route('/company/<id>', methods=["GET"])
def company_information(id):
	if request.method == 'GET':
		data = db.session.query(Company, Document, DocumentElement).join(Document).join(DocumentElement).filter(Company.id == id).all()

		if data is None:
			return render_template("company.html", data=None)

		response = json.dumps(data, cls=JoinEncoder)
		return render_template("company.html", data=response)

@application.route('/company/<id>/newdocument', methods=["GET", "POST"])
def new_document():
	if request.method == "POST":
		file = request.files['file']
		filename = file.filename
		file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
		file_hash = hashlib.sha256(open(os.path.join(application.config['UPLOAD_FOLDER'], filename),'rb').read()).hexdigest()
		#file_hash = hashlib.sha256(file).hexdigest()

		#Celery task here to upload hash to blockchain and wait for transaction and then update database values
		#After update occurs also to check to see if anyone who is interested in this company should be notified
		#Also insert into document elements with each element from the document

	return render_template('new_document.html')

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

@application.route('/interests', methods=["GET"])
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
	application.run()