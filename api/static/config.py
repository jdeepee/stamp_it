from .app import *

signkey = 'ecbd75dd-9198-4a4e-9ce8-7184a3ee37e6' #Current key for hashin JWT tokens (CHANGE THIS)
google_api_key = 'AIzaSyDIbYyVhkyABsFoFbEBfJVif7jatFuSouk'
application.config['S3_KEY'] = 'AKIAILZJYMW7TDJIRILQ' #User key for connecting to AWS
application.config['S3_SECRET'] = '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' #Secret key for AWS
application.config['S3_BUCKET'] = 'elasticbeanstalk-us-west-1-152609361256' #s3 bucket instance name 
application.config['S3_UPLOAD_DIRECTORY'] = ''
application.config['S3_URL'] = 'https://s3-us-west-1.amazonaws.com/' #URL for writing URL's of user uploads
application.config['S3_URL_MAIN'] = 's3-us-west-2.amazonaws.com'
application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://josh:pursued3vr4therThanSch00L@api-db.ciy2qyqwn3ta.us-west-1.rds.amazonaws.com/loop_db'
#application.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Josh:lambolp640@localhost/holler_db'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#Variables for validation, defined here so we can change entire app with one edit
lifetime_max_upload = 24
default_radius = 5
#Extensions allowed on picture or video
ALLOWED_EXTENSIONS = set(['jpeg', 'mp4']) #Allowed file extensions for user uploads