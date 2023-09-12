import numpy as np

"""
STEP TO USE:
[1] Add Antecendent: control.Antecendent('raindrop', np.arange(0, 1024, 0.1))
[2] Add type line [Trapmf or Trimf]
----> ctrl.trapmf('Antecendent', 'curah_hujan', 'tidak_hujan', [800, 900, 1024, 1200])
----> ctrl.trapmf('Consequent', 'curah_hujan', 'tidak_hujan', [800, 900, 1024, 1200])
		or
----> ctrl.trimf('Antecendent', 'curah_hujan', 'tidak_hujan', [800, 900, 1024, 1200])
----> ctrl.trimf('Consequent', 'curah_hujan', 'tidak_hujan', [800, 900, 1024, 1200])
"""


"""
self.antecendent = {
	'curah_hujan': {
		'range_domain':[np.arange(0, 1024, 0.1)],
		'variabel':{
				'tidak_hujan':[],
				'rintik':[],
				'hujan':[]
			},
		'Type-Plot':'Trimf'
	}
	'soil':{
		'range_domain':[np.arange(0, 1024, 0.1)]
		'variabel':{
			'kering':[],
			'normal':[],
			'basah'
		}
		'Type-Plot':'Trapmf'
	}
}
"""
"""
''''
add rules
''''
self.rules = {
	'1':{'condition':[('curah_hujan', 'tidak_hujan',
					   'soil', 'kering'), 
					'output':('tingkat_keparahan', 'rendah')]}

	###how to use
	ctrl.rule([('name_mf', 'variabel')], ('name_mf', 'variabel'))
	ctrl.rule([('curah_hujan', 'tidak_hujan'), ('soil', 'kering')], ('tingkat_keparahan', 'rendah'))
}

"""



class control:
	def __init__(self):
		self.Antecendent = dict()
		self.Consequent = dict()
		self.Rules = dict()

	def validation_trapmf(self, domain):
		if len(domain)>3:
			return True
		else:
			return False

	def trapmf(self, type_mf,name_mf, variabel, domain):
		if type_mf == 'Antecendent':
			if self.validation_trapmf(domain):
				self.Antecendent[name_mf].update({f'{variabel}':domain})
				self.Antecendent[name_mf].update({f'Type-Plot':'Trapmf'})
				return True
			else:
				print('[+] Trapmf should a <= b and b <= c and c <= d')
				return False

		else:
			if self.validation_trapmf(domain):
				self.Consequent[name_mf].update({f'{variabel}':domain})
				self.Consequent[name_mf].update({f'Type-Plot':'Trapmf'})
				return True
			else:
				print('[+] Trapmf should a <= b and b <= c and c <= d')
				return False	


	def trimf(self, type_mf, name_mf,variabel, domain):
		if type_mf == 'Antecendent':
			try:
				self.Antecendent[name_mf].update({f'{variabel}':domain})
				self.Antecendent[name_mf].update({f'Type-Plot':'Trimf'})
				return True
			except Exception as e:
				print(e)
				return False
		else:
			try:
				self.Consequent[name_mf].update({f'{variabel}':domain})
				self.Consequent[name_mf].update({f'Type-Plot':'Trimf'})
				return True
			except Exception as e:
				print(e)
				return False

	def Antecendents(self, Antecendent, domain):
		self.Antecendent[Antecendent] = ({f'range_domain':domain})

	def Consequents(self, Consequent, domain):
		self.Consequent[Consequent] = ({f'range_domain':domain})

	def rule(self, condition, output):
		length_rule_now = len(self.Rules)
		self.Rules[str(length_rule_now+1)] = {'condition':condition, 'output':output}


	def add_rules_external(self, name_file):
		open_rules = open(name_file, 'r', encoding='utf-8').read().splitlines()
		parsed_rules = {}
		for idx, rule_text in enumerate(open_rules, start=1):
		    conditions_part, output_part = rule_text.split("//")
		    conditions = conditions_part.split("|")
		    conditions_dict = {}
		    for cond in conditions:
		        var, val = cond.split("=")
		        conditions_dict[var] = val
		    
		    output_var, output_val = output_part.split("=")
		    
		    self.Rules[str(idx)] = {**conditions_dict, 'output': {output_var: output_val}}

		#print(parsed_rules)
		"""
		for idx, rule in enumerate(open_rules, start=1): 
			conditions, output = rule.split('//') 		    
			conditions = conditions.split('|')
			conditions = [condition.split('=') for condition in conditions]
			conditions = [(var.strip(), label.strip()) for var, label in conditions]
			
			output = output.split('=')
			output = (output[0].strip(), output[1].strip())
			parsed_rule = {'conditions': conditions, 'output': output}
			self.Rules[str(idx)] = parsed_rule
		"""

		
		