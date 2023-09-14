import requests
import os
import sys
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask import Flask, render_template, request
from flask_uploads import UploadSet, configure_uploads, IMAGES
import uuid
from flask_cors import CORS

import database.fuzzy as fuzzy

import numpy as np

import FUZZY.define_mfs as define_mfs
import FUZZY.calculate as calculate
import FUZZY.find_mfs as find_mfs
import FUZZY.implication as implication
import FUZZY.fuzzyfication as fuzzyfication
import FUZZY.defuzzyfication as defuzzyfication
import FUZZY.automatic as automatic
import os,sys

class run:
	def __init__(self):
		self.ctrl = define_mfs.control()

	def main(self,ch, s, g, t, p):
		self.ctrl.Antecendents('CH', np.arange(0, 1, 0.1))
		self.ctrl.Antecendents('S', np.arange(0, 1, 0.1))
		self.ctrl.Antecendents('G', np.arange(0, 1, 0.1))
		self.ctrl.Antecendents('T', np.arange(0, 1, 0.1))
		self.ctrl.Antecendents('P', np.arange(0, 1, 0.1))

		self.ctrl.Consequents('tingkat_keparahan', np.arange(0, 10, 0.1))


		self.ctrl.trapmf('Antecendent', 'CH', 'TdkHujan', [800, 900, 1024, 1200])
		self.ctrl.trapmf('Antecendent', 'CH', 'Sedang', [400, 500, 800, 900])
		self.ctrl.trapmf('Antecendent', 'CH', 'Hujan', [-1000, 0, 400, 500])

		self.ctrl.trapmf('Antecendent', 'S', 'Kering', [600, 750, 1024, 1200])
		self.ctrl.trapmf('Antecendent', 'S', 'Normal', [300, 350, 600, 750])
		self.ctrl.trapmf('Antecendent', 'S', 'Basah',  [-100, 0, 300, 350])

		self.ctrl.trapmf('Antecendent', 'G', 'Rendah', [0,0, 0.6, 0.9])
		self.ctrl.trapmf('Antecendent', 'G', 'Sedang', [0.6, 0.9, 1.6, 1.9])
		self.ctrl.trapmf('Antecendent', 'G', 'Tinggi', [1.6, 1.9, 10, 20])

		self.ctrl.trapmf('Antecendent', 'T', 'Dingin', [-1000, 0, 15, 20])
		self.ctrl.trapmf('Antecendent', 'T', 'Hangat', [15, 20, 30, 35])
		self.ctrl.trapmf('Antecendent', 'T', 'Panas', [30, 35, 60, 100])

		self.ctrl.trapmf('Antecendent', 'P', 'Tinggi',[0, 300, 400, 500])
		self.ctrl.trapmf('Antecendent', 'P', 'Sedang', [400, 500, 700, 800])
		self.ctrl.trapmf('Antecendent', 'P', 'Rendah', [700, 800, 900, 1024])

		self.ctrl.trimf('Consequents', 'tingkat_keparahan', 'Rendah', [1, 1.5, 4])
		self.ctrl.trimf('Consequents', 'tingkat_keparahan', 'Sedang', [4, 5.5, 7])
		self.ctrl.trimf('Consequents', 'tingkat_keparahan', 'Tinggi', [7, 8.5, 10])

		self.ctrl.add_rules_external('FUZZY/rules.txt')
		self.calculate = calculate.this_calculate(self.ctrl, 'CH', int(float(ch)))
		self.calculate = calculate.this_calculate(self.ctrl, 'S', int(s))
		self.calculate = calculate.this_calculate(self.ctrl, 'G', abs(int(float(g))))
		self.calculate = calculate.this_calculate(self.ctrl, 'T', int(float(t)))
		self.calculate = calculate.this_calculate(self.ctrl, 'P', int(p))
		auto = automatic.this_automatic(self.ctrl)
		a = auto.compute('sugeno')
		return a[0], a[1]


class this_fuzzy(Resource):
	def __init__(self):
		self.fuzzy_d = fuzzy.this_fuzzy()

	def upload(self, curah_hujan, soil, gyro, temp, potensio):
		fuzzy_start = run()
		defuz = fuzzy_start.main(curah_hujan, soil, gyro, temp, potensio)
		start = self.fuzzy_d.upload(curah_hujan, soil, gyro, temp, potensio, defuz[0], defuz[1])
		if start:
			return jsonify({'status':'Success'})
		else:
			return jsonify({'status':'Failed'})

	def view(self):
		start = self.fuzzy_d.view()
		if start!=False:
			new_ = {'curah_hujan':start[-1][0], 'soil':start[-1][1], 'gyro':start[-1][2], 'temperature':start[-1][3], 'potensiometer':start[-1][4], 'datetime':start[-1][5], 'fuzzy_output':start[-1][6], 'fuzzy_output_sugeno':start[-1][7]}
			return jsonify(new_)
		else:
			return jsonify({'cant fetch':'data null'})

	def get(self):
		id = request.args.get('id')
		if id == 'add':
			curah_hujan = request.args.get('ch')
			soil = request.args.get('s')
			gyro = request.args.get('g')
			temp = request.args.get('t')
			potensio = request.args.get('p')
			return self.upload(curah_hujan, soil, gyro, temp, potensio)

		if id == 'view':
			return self.view()
