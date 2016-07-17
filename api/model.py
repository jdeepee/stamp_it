from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import UUIDType
from sqlalchemy.sql import func
from config import *
from app import application

engine = create_engine(application.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(application)

Base = declarative_base()

class User(Base):
	__tablename__ = 'customer'

	id = db.Column('id', UUIDType(binary=False), primary_key=True)
	username = db.Column('username', db.Unicode, unique=True)
	email = db.Column('email', db.Unicode, unique=True)
	password = db.Column('password', db.Unicode)
	name = db.Column('name', db.Unicode)

class Interest(Base):
	__tablename__ = 'interest'

	id = db.Column('id', UUIDType(binary=False), primary_key=True)
	company_id = db.Column('company_id', UUIDType(binary=False), db.ForeignKey('company.id'))
	test_id = db.Column('test_id', UUIDType(binary=False), db.ForeignKey('test.id'))

	company = db.relationship('Company', foreign_keys=company_id)
	test = db.relationship('Test', foreign_keys=test_id)

class Test(Base):
	__tablename__ = "test"

	id = db.Column('id', UUIDType(binary=False), primary_key=True)
	company_id = db.Column('company_id', UUIDType(binary=False), db.ForeignKey('company.id'))
	test_type = db.Column('test_type', db.Unicode)
	threshold = db.Column('threshold', db.Integer)

	company = db.relationship('Company', foreign_keys=company_id)

class TestResult(Base):
	__tablename__ = 'test_result'

	id = db.Column('id', UUIDType(binary=False), primary_key=True)
	result = db.Column('result', db.Unicode)
	test_id = db.Column('test_id', UUIDType(binary=False), db.ForeignKey('test.id'))
	blockchain_transaction = db.Column('blockchain_transaction', db.Unicode)
	time = db.Column('time', db.DateTime, server_default=func.now())

	test = db.relationship('Test', foreign_keys=test_id)

class Company(Base):
	__tablename__ = "company"

	id = db.Column('id', UUIDType(binary=False), primary_key=True)
	name = db.Column('name', db.Unicode)

	def __json__(self):
		return ['id', 'name']

class Document(Base):
	__tablename__ = "document"

	id = db.Column('id', UUIDType(binary=False), primary_key=True)
	company_id = db.Column('company_id', UUIDType(binary=False), db.ForeignKey('company.id'))
	company_name = db.Column('company_name', db.Unicode)
	blockchain_transaction = db.Column('blockchain_transaction', db.Unicode)
	document_name = db.Column('document_name', db.Unicode)
	time_uploaded = db.Column('time_uploaded', db.DateTime, server_default=func.now())

	companyid = db.relationship("Company", foreign_keys=company_id)

	def __json__(self):
		return ['company_id', 'company_name', 'blockchain_transaction', 'document_name', 'time_uploaded']

class DocumentElement(Base):
	__tablename__ = "document_elemnet"

	id = db.Column('id', UUIDType(binary=False), primary_key=True)
	blockchain_transaction = db.Column('blockchain_transaction', db.Unicode)
	master_document = db.Column('master_document', UUIDType(binary=False), db.ForeignKey('document.id'))
	document_element_name = db.Column('document_element_name', db.Unicode)

	document = db.relationship("Document", foreign_keys=master_document)

	def __json__(self):
		return ['blockchain_transaction', 'master_document', 'document_element_name']

