from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import UUIDType
from ..config import *

engine = create_engine(application.config['SQLALCHEMY_DATABASE_URI'])
db = SQLAlchemy(application)

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = db.Column('id', UUIDType(binary=False), primary_key=True)
	username = db.Column('username', db.Unicode, unique=True)
	email = db.Column('email', db.Unicode, unique=True)
	password = db.Column('password', db.Unicode)
	name = db.Column('name', db.Unicode)

class Company(Base):
	__tablename__ = "company"

	id = db.Column('id', UUIDType(binary=False), primary_key=True)
	name = db.Column('name', db.Unicode)
	user_id = db.Column('user', db.Unicode, db.ForeignKey('user.id'))

    user = db.relationship('User', foreign_keys=user)

class Document(Base):
	__tablename__ = "document"

	id = db.Column('id', UUIDType(binary=False), primary_key=True)
	company_id = db.Column('company_id', UUIDType(binary=False), db.ForeignKey('company.id'))
	company_name = db.Column('company_name', db.Unicode, db.ForeignKey('company.name'))
	blockchain_block = db.Column('blockchain_block', db.Unicode)
	blockchain_transaction = db.Column('blockchain_transaction', db.Unicode)
	document_name = db.Column('document_name', db.Unicode)

	companyid = db.relationship("Company", foreign_keys=company_id)
	companyname = db.relationship("Company", foreign_keys=company_name)

class DocumentElement(Base):
	__tablename__ = "document_element"

	id = db.Column('id', UUIDType(binary=False), primary_key=True)
	company_id = db.Column('company_id', UUIDType(binary=False), db.ForeignKey('company.id'))
	company_name = db.Column('company_name', db.Unicode, db.ForeignKey('company.name'))
	blockchain_block = db.Column('blockchain_block', db.Unicode)
	blockchain_transaction = db.Column('blockchain_transaction', db.Unicode)
	master_document = db.Column('master_document', UUIDType(binary=False), db.ForeignKey('document.id'))
	document_element_name = db.Column('document_element_name', db.Unicode)

	companyid = db.relationship("Company", foreign_keys=company_id)
	companyname = db.relationship("Company", foreign_keys=company_name)
	document = db.relationship("Document", foreign_keys=master_document)

