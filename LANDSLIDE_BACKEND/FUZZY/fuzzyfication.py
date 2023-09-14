from itertools import product
from itertools import cycle

class this_fuzzyfication:
	def __init__(self, control, mfs_found, implication_rules):
		self.Antecendent = control.Antecendent
		self.Consequent = control.Consequent
		self.Rules = control.Rules

		self.implication_rules = implication_rules

	def aturan_trapmf(self, name_mf, var):
		"""
		name_mf: CH
		var (variable): Basah / Sedang / Tinggi
		"""
		x = float(self.Antecendent[name_mf]['input_value'])
		if x <= self.Antecendent[name_mf][var][0] or x >= self.Antecendent[name_mf][var][-1]:
			return 0
		if self.Antecendent[name_mf][var][0] <= x <= self.Antecendent[name_mf][var][1]:
			cal = (x-self.Antecendent[name_mf][var][0])/(self.Antecendent[name_mf][var][1]-self.Antecendent[name_mf][var][0])
			return cal
		if self.Antecendent[name_mf][var][1] <= x <= self.Antecendent[name_mf][var][2]:
			return 1
		if self.Antecendent[name_mf][var][2] <= x <= self.Antecendent[name_mf][var][3]:
			cal = (self.Antecendent[name_mf][var][3]-x)/(self.Antecendent[name_mf][var][3]-self.Antecendent[name_mf][var][2])
			return cal
		"""
		if var == self.Antecendent[name_mf][var]:
			if x >= self.Antecendent[name_mf][var][-1]:
				return 0
			if self.Antecendent[name_mf][var][-2] <= x <= self.Antecendent[name_mf][var][-1]:
				cal = (self.Antecendent[name_mf][var][-2]-x)/(self.Antecendent[name_mf][var][-1]-self.Antecendent[name_mf][var][-2])
				return cal
			if x <= self.Antecendent[name_mf][var][-2]:
				return 1


		if var == self.Antecendent[name_mf][var]:
			if x <= self.Antecendent[name_mf][var][0]:
				return 0
			if self.Antecendent[name_mf][var][0] <= x <= self.Antecendent[name_mf][var][-1]:
				cal = (x-self.Antecendent[name_mf][var][0])/(self.Antecendent[name_mf][var][-1] - self.Antecendent[name_mf][var][0])
				return cal
			if x <= self.Antecendent[name_mf][var][-2]:
				return 1
		
		else:
			if x <= self.Antecendent[name_mf][var][0] or x >= self.Antecendent[name_mf][var][-1]:
				return 0
			if self.Antecendent[name_mf][var][0] <= x <= self.Antecendent[name_mf][var][1]:
				cal = (x-self.Antecendent[name_mf][var][0])/(self.Antecendent[name_mf][var][1]-self.Antecendent[name_mf][var][0])
				return cal
			if self.Antecendent[name_mf][var][1] <= x <= self.Antecendent[name_mf][var][2]:
				return 1
			if self.Antecendent[name_mf][var][2] <= x <= self.Antecendent[name_mf][var][3]:
				cal = (self.Antecendent[name_mf][var][3]-x)/(self.Antecendent[name_mf][var][3]-self.Antecendent[name_mf][var][2])
				return cal
		"""


	def aturan_trimf(self, name_mf, var):
		x = float(self.Antecendent[name_mf]['input_value'])
		if x <= self.Antecendent[name_mf][var][0] or x >= self.Antecendent[name_mf][var][-1]:
			return 0
		if self.Antecendent[name_mf][var][0] <= x <= self.Antecendent[name_mf][var][1]:
			cal = (x-self.Antecendent[name_mf][var][0])/(self.Antecendent[name_mf][var][1]-self.Antecendent[name_mf][var][0])
			return cal 
		if self.Antecendent[name_mf][var][1] <= x <= self.Antecendent[name_mf][var][-1]:
			cal = (self.Antecendent[name_mf][var][-1]-x)/(self.Antecendent[name_mf][var][-1]-self.Antecendent[name_mf][var][1])
			return cal 
		else:
			return 1
			
		
	def start(self):		
		enhancment = dict()
		for key in self.implication_rules:
			enhancment[key] = {}
			for val in key:
				pass

			for res in (self.implication_rules[key]):
				#res = ('curah_hujan|sedang', 'soil|normal')
				if type(res) != str:
					for a in res:
						result = []
						name_mf, var = a.split('|')
						enhancment[key].update({name_mf:{}})
					for res_child in res:
						name_mf, var = res_child.split('|')
						if self.Antecendent[name_mf]['Type-Plot'] == 'Trapmf':
							result_fuzzy = (self.aturan_trapmf(name_mf, var))
						if self.Antecendent[name_mf]['Type-Plot'] == 'Trimf':
							result_fuzzy = (self.aturan_trimf(name_mf, var))
						enhancment[key][name_mf] = {var:result_fuzzy}
				else:
					name,rules_number = res.split(':')
					enhancment[key].update({'RulesIntegration':rules_number})
			

		#{'1': {'curah_hujan': {'sedang': 1.0}, 'soil': {'normal': 0}}
		return enhancment
					
						
