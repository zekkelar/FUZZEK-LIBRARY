import os
import sys
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import uuid
from flask_cors import CORS
from werkzeug.utils import secure_filename

import database.potensiometer as potensiometer


class this_potensiometer(Resource):
	def __init__(self):
		self.potensiometer = potensiometer.this_potensiometer()

	def add(self, value):
		get = self.potensiometer.add(value)
		if get:
			return jsonify({'status':'Success'})
		else:
			return jsonify({'status':'Failed'})
			
	def view(self):
		get = self.potensiometer.view()
		if get:
			return jsonify({'result':{'value':get[-1][0], 'datetime':get[-1][1]}})
		else:
			return jsonify({'result':'no result'})

	def get(self):
		id = request.args.get('id')
		if id=='add':
			value = request.args.get('value')
			return self.add(value)
		else:
			return self.view()

