import requests
import os
import sys
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import uuid
from flask_cors import CORS
from werkzeug.utils import secure_filename

import database.mpu605 as mpu605


class this_mpu605(Resource):
	def __init__(self):
		self.mpu605_d = mpu605.this_mpu605()

	def add(self, ax, ay, az, gx, gy, gz):
		get = self.mpu605_d.add(ax, ay, az, gx, gy, gz)
		if get:
			return jsonify({'status':'Success'})
		else:
			return jsonify({'status':'Failed'})

	def view(self):
		get = self.mpu605_d.view()
		if get!=False:		
			print(get[-1])	
			
			return jsonify({'result':{'ax':get[-1][0], 
									  'ay':get[-1][1], 
									  'az':get[-1][2], 
									  'gx':get[-1][3], 
									  'gy':get[-1][4], 
									  'gz':get[-1][5], 
									  'datetime':get[-1][6]}})

		  	
			
			
		else:
			return jsonify({'result':'no result'})

	def get(self):
		id = request.args.get('id')
		if id=='add':
			ax = request.args.get('ax')
			ay = request.args.get('ay')
			az = request.args.get('az')
			gx = request.args.get('gx')
			gy = request.args.get('gy')
			gz = request.args.get('gz')
			return self.add(ax, ay, az, gx, gy, gz)
		else:
			return self.view()

