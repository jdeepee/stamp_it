from flask import Flask, request, render_template
from passlib.hash import bcrypt
import uuid

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return render_template("index.html")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
	if request.method == "POST":
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
			return 'Insert failed'
			raise

		finally:
			db.session.close()

	elif request.method == "GET":
		return "User signup page"

# @app.route('/authtoken', methods=['POST'])
# def authtoken():
# 	return 'Auth token page'

@app.route('/company', methods=['POST', 'GET'])
def company_signup():
	if request.method == 'POST':
		data = request.form()
		name = data['name']
		jwt_t = str(request.headers.get('JWT-Auth'))
		payload = jwt.decode(jwt_t, signkey, algorithms=['HS512']) #Decoding JWT token
		jwt_id = payload['uuid'] #Getting Username in payload of JWT to ensure people cant upload referencing other peoples usernames 
		id = uuid.uuid4()

		try:
			data = Company(id=id, name=name, user_id=user_id)
			db.session.add(data)
			db.session.commit()

		except:
			db.session.rollback()
			return "Insert failed"
			raise

		finally:
			db.session.close()

	elif request.method == 'GET':
		return "Company sign up page"

@app.route('/company/<id>', methods=["GET", "PATCH"])
def company_information(id):
	if request.method == 'GET':
		pass

	elif request.method == 'PATCH':
		pass

@app.route('/company/<id>/document/<id_document>', methods=["GET", "POST", "PATCH"])
def company_document(id, id_document):
	return "Company document page"

@app.route('/company/<id>/document/<id_document>/element/<id_element>', methods=['GET', 'POST', 'PATCH'])
def company_document_element(id, id_doucment, id_element):
	return "Company document element page"

@app.route('/interest', methods=["GET", 'POST'])
def interest_creation():
	pass

@app.route('/interest/<id>', methods=["GET", "PATCH"])
def interest_information(id):
	pass

@app.route('/test', methods=["GET", 'POST'])
def test_creation():
	pass

@app.route('/test/<id>', methods=['GET', 'PATCH'])
def test_information(id):
	pass

@app.route('/test/<id>/result/<result_id>', methods=["GET", "POST"])
def test_result_information(id, result_id):
	pass

if __name__ == '__main__':
	app.run()