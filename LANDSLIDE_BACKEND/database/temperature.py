import os
import sys
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import uuid
from flask_cors import CORS
from werkzeug.utils import secure_filename


import database.conn as connection
import helpers.config as keys
import datetime



#DATABASE SENSOR SOIL

class this_temperature:
	def __init__(self):
		self.conn = connection.connect()
		self.now = datetime.datetime.now()

	def add(self, value):
		get = self.conn.connect()
		query = f"INSERT INTO temperature (value, datetime) VALUES (%s, %s)"
		val = (value, self.now)
		try:
			get[1].execute(query, val)
			get[0].commit()
			get[0].close()
			return True
		except Exception as e:
			print(e)
			return False


	def view(self):
		get = self.conn.connect()
		query = f"SELECT * FROM temperature"
		get[1].execute(query)
		result = get[1].fetchall()
		if result!=None:
			return result
		else:
			return False
