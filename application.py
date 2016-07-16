from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return "Hello world!"

@app.route('/signup', methods=['POST'])
def signup():
	return 'Signup page'

@app.route('/authtoken', methods=['POST'])
def authtoken():
	return 'Auth token page'

@app.route('/company', methods=['POST'])
def company_signup():
	if request.method == 'POST':
		data = request.form()
		name = data['name']

		try:
			
	return "Company sign up page"

@app.route('/company/<id>', methods=["GET", "PATCH"])
def company_information(id):
	return "Company information page"

@app.route('/company/<id>/document/<id_document>', methods=["GET", "POST", "PATCH"])
def company_document(id, id_document):
	return "Company document page"

@app.route('/company/<id>/document/<id_document>/element/<id_element>', methods=['GET', 'POST', 'PATCH'])
def company_document_element(id, id_doucment, id_element):
	return "Company document element page"

if __name__ == '__main__':
	app.run()