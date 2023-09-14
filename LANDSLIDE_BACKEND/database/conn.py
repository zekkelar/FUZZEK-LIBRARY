import uuid
import mysql.connector
import datetime
import os
from datetime import datetime as hyakimaru


import helpers.config as keys

class connect:
	def __init__(self):
		self.host = keys.HOST_DATABASE
		self.user = keys.USERNAME_DATABASE
		self.password = keys.PASSWORD_DATABASE
		self.database = keys.NAME_DATABASE
		self.now = datetime.datetime.now()
		self.tanggal_waktu = self.now.strftime("%d/%m/%Y %H:%M:%S")



	def connect(self):
		mydb = mysql.connector.connect(
			host = self.host,
			user = self.user,
			password = self.password,
			database = self.database
			)
		mycursor = mydb.cursor()
		return mydb, mycursor