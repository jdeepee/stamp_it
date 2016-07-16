from application import application, UPLOAD_FOLDER

application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://josh:password@localhost/stamp_it_db'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER