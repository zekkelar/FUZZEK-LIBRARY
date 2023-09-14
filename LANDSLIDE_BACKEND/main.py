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


import flask_helper.humidity as humidity
import flask_helper.raindrop as raindrop
import flask_helper.mpu605 as mpu605
import flask_helper.soil as soil
import flask_helper.potensiometer as potensiometer
import flask_helper.temperature as temperature
import flask_helper.all as all_
import flask_helper.fuzzyy as fuzzy

app = Flask(__name__)
api = Api(app)
CORS(app)

@app.route('/')
def hello():
    return 'Hello World!'

api.add_resource(humidity.this_humidity, '/humidity', methods=['GET'])
api.add_resource(raindrop.this_raindrop, '/raindrop', methods=['GET'])
api.add_resource(mpu605.this_mpu605, '/mpu605', methods=['GET'])
api.add_resource(soil.this_soil,'/soil', methods=['GET'])
api.add_resource(potensiometer.this_potensiometer, '/potensiometer', methods=['GET'])
api.add_resource(temperature.this_temperature, '/temperature', methods=['GET'])
api.add_resource(all_.this_all, '/all', methods=['GET'])
api.add_resource(fuzzy.this_fuzzy, '/fuzzy', methods=['GET'])

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
