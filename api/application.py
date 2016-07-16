from flask import Flask, request, render_template, redirect
from models.model import User, Company, Interest, Test, TestResult, DocumentElement, Document
from passlib.hash import bcrypt
from models.encoder import AlchemyEncoder, JoinEncoder
import uuid, hashlib

application = Flask(__name__)
UPLOAD_FOLDER = '/static/'

@application.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@application.route('/signup', methods=['POST', 'GET'])
def signup():
	form = SignUpForm(request.form)
	error = ''

	if request.method == "POST" and form.validate(): 
		data = request.form()
		username = data['username']
		password = bcrypt.encrypt(data['password'])
		email = data['email']
		name = data['name']
		id = uuid.uuid4()

		try:
			data = User(id=id, username=username, password=password, email=email, name=name)
			db.session.add(data)
			db.session.commit()

		except:
			db.session.rollback()
			error = 'Something went wrong'
			raise

		finally:
			db.session.close()

		return redirect('/', code=200)

	return render_template("signup.html", error=error, form=form)

@application.route('/company', methods=['POST', 'GET'])
def company_signup():
	form = ComapnySignUpForm(request.form)
	error = ''

	if request.method == 'POST' and form.validate():
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

	return render_template('company_signup.html', form=form, error=error)

@application.route('/company/<id>', methods=["GET"])
def company_information(id):
	if request.method == 'GET':
		data = db.session.query(Company, Document, DocumentElement).join(Document).join(DocumentElement).filter(Company.id == id).all()

		if data is None:
			return render_template("company.html", data=None)

		response = json.dumps(data, cls=JoinEncoder)
		return render_template("company.html", data=response)

@application.route('/company/newdocument', methods=["GET", "POST"])
def new_document():
	if request.method == "POST":
		file = request.files['file']
		filename = file.filename
		company_id = request.form['id']
		file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
		file_hash = hashlib.sha256(open(os.path.join(application.config['UPLOAD_FOLDER'], filename),'rb').read()).hexdigest()
		#file_hash = hashlib.sha256(file).hexdigest()

		#Celery task here to upload hash to blockchain and wait for transaction and then update database values
		#After update occurs also to check to see if anyone who is interested in this company should be notified

	return render_template('newfile.html')


@application.route('/company/<id>/document/<id_document>', methods=["GET"])
def company_document(id, id_document):
	if request.method == "GET":
		data = db.session.query(Document).filter(Document.id == id_document).first()

		if data is None:
			return render_template("company_document.html", data=None)

		response = json.dumps(data, cls=AlchemyEncoder)
		return render_template("company_document.html", data=response)


@application.route('/company/<id>/document/<id_document>/element/<id_element>', methods=['GET'])
def company_document_element(id, id_document, id_element):
	if request.method == "GET":
		data = db.session.query(DocumentElement).filter(DocumentElement == id_element).first()

		if data is None:
			return render_template("company_element.html", data=None)

		response = json.dumps(data, cls=AlchemyEncoder)
		return render_template("compant_element.html", data=response)

@application.route('/interest', methods=["GET", 'POST'])
def interest_creation():
	form = InterestForm(request.form)
	error = ''

	if request.method == "POST" and form.validate():
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

	return render_template("interest.html", form=form, error=error)

@application.route('/interest/<id>', methods=["GET", "PATCH"])
def interest_information(id):
	pass

@application.route('/test', methods=["GET", 'POST'])
def test_creation():
	pass

@application.route('/test/<id>', methods=['GET', 'PATCH'])
def test_information(id):
	pass

@application.route('/test/<id>/result/<result_id>', methods=["GET", "POST"])
def test_result_information(id, result_id):
	pass

if __name__ == '__main__':
	application.run()