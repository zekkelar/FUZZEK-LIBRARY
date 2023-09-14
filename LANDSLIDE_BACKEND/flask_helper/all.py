import os
import sys
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import uuid
from flask_cors import CORS
from werkzeug.utils import secure_filename

import database.temperature as temperature
import database.humidity as humidity
import database.mpu605 as mpu605
import database.potensiometer as potensiometer
import database.raindrop as raindrop
import database.soil as soil


class this_all(Resource):
	def __init__(self):
		self.temperature = temperature.this_temperature()
		self.humidity = humidity.this_humidity()
		self.mpu605 = mpu605.this_mpu605()
		self.potensiometer = potensiometer.this_potensiometer()
		self.raindrop = raindrop.this_raindrop()
		self.soil = soil.this_soil()

	def upload(self, temperature, humidity, 
					potensiometer, raindrop, 
						soil, accelerator, gyroscope):
		try:
			self.temperature.add(temperature)
			self.humidity.add(humidity)
			self.potensiometer.add(potensiometer)
			self.raindrop.add(raindrop)
			self.soil.add(soil)
			ax, ay, az = accelerator.split("|")
			gx, gy, gz = gyroscope.split("|")
			self.mpu605.add(ax, ay, az, gx, gy, gz)
			return jsonify({'Status':"Success"})
		except Exception as e:
			return jsonify({'Status':'Failed'})


	def get(self):
		temperature = request.args.get("temperature")
		humidity = request.args.get("humidity")
		potensiometer = request.args.get("potensiometer")
		raindrop = request.args.get("raindrop")
		soil = request.args.get("soil")
		accelerator = request.args.get("accelerator")
		gyroscope = request.args.get("gyroscope")

		return self.upload(temperature, humidity, potensiometer, raindrop, soil, accelerator, gyroscope)

