from flask import Flask, request, render_template, redirect
from models.model import User, Company, Interest, Test, TestResult, DocumentElement, Document
from passlib.hash import bcrypt
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

		response = json.dumps(data, cls=JoinEncoder)
		return render_template("company.html", data=response)

@application.route('/company/newdocument', methods=["GET", "POST"])
def new_document():
	if request.method == "POST":
		file = request.files['file']
		filename = file.filename
		file.save(os.path.join(application.config['UPLOAD_FOLDER'], filename))
		file_hash = hashlib.sha256(open(os.path.join(application.config['UPLOAD_FOLDER'], filename),'rb').read()).hexdigest()

	return render_template('newfile.html')


@application.route('/company/<id>/document/<id_document>', methods=["GET"])
def company_document(id, id_document):
	if request.method == "GET":
		pass



@application.route('/company/<id>/document/<id_document>/element/<id_element>', methods=['GET'])
def company_document_element(id, id_doucment, id_element):
	return "Company document element page"

@application.route('/interest', methods=["GET", 'POST'])
def interest_creation():
	pass

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