from itertools import product
import re

class trimf(object):
	def __init__(self, control):
		self.Antecendent = control.Antecendent
		self.Consequent = control.Consequent
		self.Rules = control.Rules

	def left(self, domain, fuzzyfication):
		calc = domain[1] - domain[0]
		subt = fuzzyfication * calc
		result = subt + domain[0]
		return result

	def mid(self, domain):
		pass

	def right(self, domain, fuzzyfication):
		calc = domain[-1] - domain[1]
		subt = calc * fuzzyfication
		result = domain[-1] - subt
		return result


class integration(object):
	def __init__(self, control):
		self.Antecendent = control.Antecendent
		self.Consequent = control.Consequent
		self.Rules = control.Rules

	def linear_up(self, batas_atas, batas_bawah, _type_, z):
		if _type_ == "momen":
			return ((z-batas_bawah)/(batas_atas-batas_bawah)) * z

		if _type_ == "area":
			return ((z-batas_bawah)/(batas_atas-batas_bawah)) 

	def linear_down(self, batas_atas, batas_bawah, _type_, z):
		if _type_ == "momen":
			return ((batas_atas-z)/(batas_atas-batas_bawah)) * z
		if _type_ == "area":
			return ((batas_atas-z)/(batas_atas-batas_bawah)) 

	def stable(self, z, _type_, fuzzyfikasi):
		if _type_ == "momen":
			return (fuzzyfikasi)*z
		if _type_ == "area":
			return (fuzzyfikasi)

	def main(self, type_calc, batas_bawah, batas_atas, type_integral, fuzzyfikasi):
		if type_calc == "linear_up":
			n = 1000
			h = (float(batas_atas)- float(batas_bawah)) / n
			integral = 0
			for i in range(n+1):
			    x = float(batas_bawah) + i * h
			    if i == 0 or i == n:
			        integral += self.linear_up(batas_atas, batas_bawah, type_integral, x) / 2
			    else:
			        integral += self.linear_up(batas_atas, batas_bawah, type_integral, x)

			integral *= h
			return integral	

		if type_calc == 'stable':
			n = 1000
			h = (float(batas_atas)- float(batas_bawah)) / n
			integral = 0
			for i in range(n+1):
			    x = float(batas_bawah) + i * h
			    if i == 0 or i == n:
			        integral += self.stable(x, type_integral, fuzzyfikasi) / 2
			    else:
			        integral += self.stable(x, type_integral, fuzzyfikasi)

			integral *= h
			return integral	

		if type_calc == "linear_down":
			n = 1000
			h = (float(batas_atas)- float(batas_bawah)) / n
			integral = 0
			for i in range(n+1):
			    x = float(batas_bawah) + i * h
			    if i == 0 or i == n:
			        integral += self.linear_down(batas_atas, batas_bawah, type_integral, x) / 2
			    else:
			        integral += self.linear_down(batas_atas, batas_bawah, type_integral, x)

			integral *= h
			return integral	

class this_defuzzyfication(object):
	def __init__(self, control, implication_max):
		self.Antecendent = control.Antecendent
		self.Consequent = control.Consequent
		self.Rules = control.Rules
		self.max=  implication_max

		self.trimf = trimf(control)
		self.integral = integration(control)

	def main(self):
		total_winner = dict()
		for key_max, value_max in self.max.items():
			total_winner[key_max] = {}
			total_winner[key_max] = {'cut-area':[]}
			total_winner[key_max].update({'fuzzyfication':''})
			for key_conseq, val_conseq in self.Consequent.items():
				fuzzyfication = (self.max[key_max]['winner'])
				domain = (self.Consequent[key_conseq][key_max])
				
				left = self.trimf.left(domain,fuzzyfication)
				right = self.trimf.right(domain, fuzzyfication)
				total_winner[key_max]['cut-area'].append([domain[0], left, right, domain[-1]])
				total_winner[key_max]['fuzzyfication'] = fuzzyfication

		sum_momen = 0
		sum_area = 0
		for key, val in total_winner.items():
			momen1 = self.integral.main('linear_up', total_winner[key]['cut-area'][0][0], total_winner[key]['cut-area'][0][1], 'momen', float(total_winner[key]['fuzzyfication']))
			area1 =  self.integral.main('linear_up', total_winner[key]['cut-area'][0][0], total_winner[key]['cut-area'][0][1], 'area', float(total_winner[key]['fuzzyfication']))

			momen2 = self.integral.main('stable', total_winner[key]['cut-area'][0][1], total_winner[key]['cut-area'][0][2], 'momen', float(total_winner[key]['fuzzyfication']))
			area2 = self.integral.main('stable', total_winner[key]['cut-area'][0][1], total_winner[key]['cut-area'][0][2], 'area', float(total_winner[key]['fuzzyfication']))

			momen3 = self.integral.main('linear_down', total_winner[key]['cut-area'][0][2], total_winner[key]['cut-area'][0][3], 'momen', float(total_winner[key]['fuzzyfication']))
			area3 = self.integral.main('linear_down', total_winner[key]['cut-area'][0][2], total_winner[key]['cut-area'][0][3], 'area', float(total_winner[key]['fuzzyfication']))
			sum_momen = sum_momen + momen1 +momen2 + momen3
			sum_area = sum_area + area1 + area2 + area3

		return(sum_momen/sum_area)


class defuzzyfication_sugeno(object):
	def __init__(self, control, implication_min):
		self.Antecendent = control.Antecendent
		self.Consequent = control.Consequent
		self.Rules = control.Rules
		self.min = implication_min

	def main(self):
		"""
		filtered_data = {k: v for k, v in self.min.items() if v['winner'] != 0}
		for key,val in filtered_data.items():
			for key_, val in (self.Rules[val['RulesIntegration']]['output'].items()):
				filtered_data[key].update({'RulesIntegration':val})
		"""

		filtered_data = self.min
		#{'5': {'CH': {'Sedang': 1.0}, 'S': {'Normal': 1.0}, 'G': {'Sedang': 1}, 'T': {'Dingin': 0.6}, 'P': {'Rendah': 0.4}, 'RulesIntegration': 'Rendah', 'winner': 0.4}
		#'7': {'CH': {'Sedang': 1.0}, 'S': {'Normal': 1.0}, 'G': {'Sedang': 1}, 'T': {'Hangat': 0.4}, 'P': {'Rendah': 0.4}, 'RulesIntegration': 'Rendah', 'winner': 0.4}}
		ehe = dict()
		for key, val in filtered_data.items():
			ehe[key] = {}
			fuzzy_number = (filtered_data[key]['winner'])
			for mo in filtered_data[key]:
				if mo == 'RulesIntegration' or mo == 'winner':
					pass
				else:
					for y in (filtered_data[key][mo]):		
						if (filtered_data[key][mo][y]) == fuzzy_number:
							ehe[key].update({f'{mo}':fuzzy_number})
							break

		ehe = {key: {next(iter(value)) : value[next(iter(value))]} if len(value) > 1 else value for key, value in ehe.items()}
		atas = []
		bawah = []
		for key,value in ehe.items():
			for key2,value2 in value.items():
				cal = float(self.Antecendent[key2]['input_value'])*float(value2)
				bawah.append(value2)
				atas.append(cal)
				
		return (sum(atas)/sum(bawah))

